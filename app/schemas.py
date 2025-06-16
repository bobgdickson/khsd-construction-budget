from pydantic import BaseModel, Field, field_validator
from typing import Optional
from app.constants import (
    ALLOWED_RESOURCES,
    ALLOWED_FLOW_TYPES,
    ALLOWED_FISCAL_YEARS,
    ALLOWED_FLOW_SOURCES,
)

class ConstructionSourceBase(BaseModel):
    resource: str
    flow_type: str
    fiscal_year: str
    flow_source: str
    amount: float


class ConstructionSourceCreate(ConstructionSourceBase):
    pass


class ConstructionSource(ConstructionSourceBase):
    id: Optional[int] = None  # in case you later add a primary key
    class Config:
        orm_mode = True


class ConstructionBudgetBase(BaseModel):
    budget_period: int
    fund_code: str
    program_code: str
    project_id: str
    activity_id: str
    line_descr: Optional[str]
    monetary_amount: float


class ConstructionBudgetCreate(ConstructionBudgetBase):
    pass


class ConstructionBudget(ConstructionBudgetBase):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class ConstructionStaticRowBase(BaseModel):
    resource: str
    flow_type: str
    fiscal_year: str
    flow_source: str
    amount: float

    @field_validator("resource")
    def validate_resource(cls, v):
        if v not in ALLOWED_RESOURCES:
            raise ValueError(f"Invalid resource: {v}")
        return v

    @field_validator("flow_type")
    def validate_flow_type(cls, v):
        if v not in ALLOWED_FLOW_TYPES:
            raise ValueError(f"Invalid flow type: {v}")
        return v

    @field_validator("fiscal_year")
    def validate_fiscal_year(cls, v):
        if v not in ALLOWED_FISCAL_YEARS:
            raise ValueError(f"Invalid fiscal year: {v}")
        return v

    @field_validator("flow_source")
    def validate_flow_source(cls, v):
        if v not in ALLOWED_FLOW_SOURCES:
            raise ValueError(f"Invalid flow source: {v}")
        return v

class ConstructionStaticRowCreate(ConstructionStaticRowBase):
    pass

class ConstructionStaticRowUpdate(ConstructionStaticRowBase):
    pass

class ConstructionStaticRowRead(ConstructionStaticRowBase):
    id: int

    class Config:
        orm_mode = True


class ConstructionSettingBase(BaseModel):
    name: str
    value: str


class ConstructionSettingCreate(ConstructionSettingBase):
    pass


class ConstructionSettingUpdate(ConstructionSettingBase):
    pass


class ConstructionSettingRead(ConstructionSettingBase):
    class Config:
        orm_mode = True