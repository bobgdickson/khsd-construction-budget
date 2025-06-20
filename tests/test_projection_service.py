import pytest
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.models import ConstructionSetting, ConstructionSource, ConstructionBudget
from app.services.projection import (
    get_setting,
    clear_sources,
    insert_rows,
    get_budget_rows,
    clean_project_costs,
    list_years,
    list_resources,
    get_amount,
    calc_interest,
    calc_balance,
    run_projection,
    STATIC_ROWS,
)


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def test_get_setting_default_and_existing(db_session):
    # Default returned when setting does not exist
    assert get_setting(db_session, "NON_EXISTENT", "default") == "default"
    # Existing setting overrides default
    setting = ConstructionSetting(name="TEST", value="value123")
    db_session.add(setting)
    db_session.commit()
    assert get_setting(db_session, "TEST", "default") == "value123"


def test_clear_and_insert_rows(db_session):
    rows = [["R1", "T1", "2025", "PROJECTED", 100.0], ["R2", "T2", "2026", "PROJECTED", 200.0]]
    insert_rows(db_session, rows)
    assert db_session.query(ConstructionSource).count() == 2
    clear_sources(db_session)
    assert db_session.query(ConstructionSource).count() == 0


def test_get_budget_rows(db_session):
    # Create sample budget entries
    budgets = [
        ConstructionBudget(
            budget_period=2025,
            fund_code="F",
            program_code="0916",
            project_id="P",
            activity_id="A",
            line_descr="",
            monetary_amount=100.0,
        ),
        ConstructionBudget(
            budget_period=2025,
            fund_code="F",
            program_code="0916",
            project_id="P",
            activity_id="B",
            line_descr="",
            monetary_amount=50.0,
        ),
        ConstructionBudget(
            budget_period=2024,
            fund_code="F",
            program_code="0916",
            project_id="P",
            activity_id="C",
            line_descr="",
            monetary_amount=30.0,
        ),
        ConstructionBudget(
            budget_period=2025,
            fund_code="F",
            program_code="0930",
            project_id="P",
            activity_id="D",
            line_descr="",
            monetary_amount=200.0,
        ),
    ]
    db_session.add_all(budgets)
    db_session.commit()
    result = get_budget_rows(db_session, "2024")
    # Only entries for 2025 aggregated by program_code
    expected = {(2025, "0916", 150.0), (2025, "0930", 200.0)}
    assert set(result) == expected


def test_clean_project_costs():
    budget_rows = [(2025, "0916", 0.0), (2026, "0917", 100.0)]
    cleaned = clean_project_costs(budget_rows)
    assert cleaned == [["0917", "COSTS", "2026", "PROJECTED", 100.0]]


def test_list_years_and_resources():
    budget_rows = [(2025, "0916", 100.0)]
    static_rows = [["0905", "X", "2024", "PROJECTED", 0.0]]
    years = list_years(budget_rows, static_rows)
    resources = list_resources(budget_rows, static_rows)
    assert years == ["2024", "2025"]
    assert resources == ["0905", "0916"]


def test_get_amount_and_calculations(db_session):
    # Seed previous ending equity and cost/proceeds for testing
    db_session.add(
        ConstructionSource(
            resource="R", flow_type="END_EQUITY", fiscal_year="2024", flow_source="PROJECTED", amount=100.0
        )
    )
    db_session.add(
        ConstructionSource(
            resource="R", flow_type="COSTS", fiscal_year="2025", flow_source="PROJECTED", amount=200.0
        )
    )
    db_session.add(
        ConstructionSource(
            resource="R", flow_type="PROCEEDS", fiscal_year="2025", flow_source="PROJECTED", amount=50.0
        )
    )
    db_session.commit()
    # Verify get_amount
    assert get_amount(db_session, "COSTS", "2025", "R") == 200.0
    # Test interest calculation
    calc_interest(db_session, "2025", "R", rate=0.1)
    interest = db_session.query(ConstructionSource).filter_by(
        flow_type="INTEREST", fiscal_year="2025", resource="R"
    ).first()
    assert interest is not None and interest.amount > 0
    # Test balance calculation
    calc_balance(db_session, "2025", "R")
    beg_eq = db_session.query(ConstructionSource).filter_by(
        flow_type="BEG_EQUITY", fiscal_year="2025", resource="R"
    ).first()
    end_eq = db_session.query(ConstructionSource).filter_by(
        flow_type="END_EQUITY", fiscal_year="2025", resource="R"
    ).first()
    assert beg_eq.amount == 100.0
    total = db_session.query(func.sum(ConstructionSource.amount)).filter_by(
        fiscal_year="2025", resource="R"
    ).scalar()
    assert abs(end_eq.amount - total) < 1e-6


def test_run_projection_creates_sources(db_session):
    result = run_projection(db_session)
    assert result == "Success"
    # There should be at least the static rows inserted
    count = db_session.query(ConstructionSource).count()
    assert count >= len(STATIC_ROWS)