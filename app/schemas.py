from pydantic import BaseModel, Field
from typing import Optional


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