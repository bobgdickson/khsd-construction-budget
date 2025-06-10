from sqlalchemy import Column, String, Integer, Float
from app.db import Base


class ConstructionSource(Base):
    __tablename__ = "CONSTRUCTION_SOURCES"

    resource = Column(String(10), primary_key=True)
    flow_type = Column(String(50), primary_key=True)
    fiscal_year = Column(String(10), primary_key=True)
    flow_source = Column(String(50), primary_key=True)
    amount = Column(Float)


class ConstructionBudget(Base):
    __tablename__ = "CONSTRUCTION_BUDGET"

    budget_period = Column(Integer, primary_key=True)
    fund_code = Column(String(10), primary_key=True)
    program_code = Column(String(10), primary_key=True)
    project_id = Column(String(10), primary_key=True)
    activity_id = Column(String(10), primary_key=True)
    line_descr = Column(String(255), nullable=True)
    monetary_amount = Column(Float)

class ConstructionStaticRow(Base):
    __tablename__ = "CONSTRUCTION_STATIC_ROWS"

    id = Column(Integer, primary_key=True, index=True)
    resource = Column(String(10))
    flow_type = Column(String(50))
    fiscal_year = Column(String(10))
    flow_source = Column(String(50))
    amount = Column(Float)