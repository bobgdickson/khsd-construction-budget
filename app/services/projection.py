from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func, delete
from app.models import ConstructionSource, ConstructionBudget

# Constants
INT_RATE = 0.03
PRIOR_YEAR = "2024"

# Static rows previously hardcoded in your script
STATIC_ROWS = [
    ["0916", "PROCEEDS", "2025", "PROJECTED", 80000000.00],
    ["0905", "JPALEASE", "2025", "PROJECTED", 56000000.00],
    ["0920", "JPALEASE", "2025", "PROJECTED", 500000.00],
    ["0920", "JPALEASE", "2026", "PROJECTED", 500000.00],
    ["0920", "JPALEASE", "2027", "PROJECTED", 500000.00],
    ["0920", "JPALEASE", "2025", "PROJECTED", -30000000.00],
    ["0930", "DEVFEES", "2025", "PROJECTED", 4000000.00],
    ["0930", "DEVFEES", "2026", "PROJECTED", 4000000.00],
    ["0930", "DEVFEES", "2027", "PROJECTED", 4000000.00],
    ["0930", "DEVFEES", "2028", "PROJECTED", 4000000.00],
    ["0930", "DEVFEES", "2029", "PROJECTED", 4000000.00],
    ["0930", "DEVFEES", "2030", "PROJECTED", 4000000.00],
    ["0935", "STABILIZE", "2025", "PROJECTED", -0.00],
    ["0935", "STABILIZE", "2026", "PROJECTED", -0.00],
    ["0935", "STABILIZE", "2027", "PROJECTED", -20000000.00],
]


def clear_sources(db: Session):
    db.execute(delete(ConstructionSource).where(ConstructionSource.flow_source == "PROJECTED"))
    db.commit()


def insert_rows(db: Session, rows: List[List]):
    for r in rows:
        db.add(ConstructionSource(
            resource=r[0],
            flow_type=r[1],
            fiscal_year=r[2],
            flow_source=r[3],
            amount=r[4],
        ))
    db.commit()


def get_budget_rows(db: Session, after_year: str) -> List[List]:
    return db.query(
        ConstructionBudget.budget_period,
        ConstructionBudget.program_code,
        func.sum(ConstructionBudget.monetary_amount)
    ).filter(
        ConstructionBudget.budget_period > int(after_year),
        ConstructionBudget.program_code.in_([
            '0905', '0910', '0915', '0916', '0917',
            '0920', '0925', '0930', '0935', '0940', '0945'
        ])
    ).group_by(
        ConstructionBudget.budget_period,
        ConstructionBudget.program_code
    ).all()


def clean_project_costs(rows: List[List]) -> List[List]:
    return [
        [r[1], "COSTS", str(r[0]), "PROJECTED", r[2]]
        for r in rows if r[2] != 0
    ]


def list_years(budget_rows, static_rows):
    return sorted(set(
        [str(int(r[0])) for r in budget_rows] +
        [r[2] for r in static_rows]
    ))


def list_resources(budget_rows, static_rows):
    return sorted(set(
        [r[1] for r in budget_rows] +
        [r[0] for r in static_rows]
    ))


def get_amount(db: Session, flow_type: str, year: str, resource: str) -> float:
    row = db.query(ConstructionSource.amount).filter_by(
        flow_type=flow_type, fiscal_year=year, resource=resource
    ).first()
    return row[0] if row else 0.0


def calc_interest(db: Session, year: str, resource: str, rate: float = INT_RATE):
    cost = get_amount(db, "COSTS", year, resource)
    beg = get_amount(db, "END_EQUITY", str(int(year) - 1), resource)
    proceeds = get_amount(db, "PROCEEDS", year, resource)
    interest = round((((beg + cost + proceeds) + beg) / 2) * rate, -2)
    if interest > 0:
        insert_rows(db, [[resource, "INTEREST", year, "PROJECTED", interest]])


def calc_balance(db: Session, year: str, resource: str):
    beg = get_amount(db, "END_EQUITY", str(int(year) - 1), resource)
    insert_rows(db, [[resource, "BEG_EQUITY", year, "PROJECTED", beg]])

    total = db.query(func.sum(ConstructionSource.amount)).filter_by(
        resource=resource, fiscal_year=year
    ).scalar() or 0.0
    insert_rows(db, [[resource, "END_EQUITY", year, "PROJECTED", total]])


def run_projection(db: Session, prior_year: str = PRIOR_YEAR, rate: float = INT_RATE) -> str:
    try:
        clear_sources(db)
        insert_rows(db, STATIC_ROWS)
        budget_rows = get_budget_rows(db, prior_year)
        insert_rows(db, clean_project_costs(budget_rows))

        years = list_years(budget_rows, STATIC_ROWS)
        resources = list_resources(budget_rows, STATIC_ROWS)

        for res in resources:
            for yr in years:
                calc_interest(db, yr, res, rate)
                calc_balance(db, yr, res)

        return "Success"
    except Exception as e:
        return f"Failed: {str(e)}"
