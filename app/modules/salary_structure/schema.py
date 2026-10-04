from pydantic import BaseModel
from datetime import date


class SalaryStructureCreate(BaseModel):
    employee_id: int
    component_name: str
    component_type: str
    amount: float
    effective_from: date
    effective_to: date | None = None


class SalaryStructureUpdate(BaseModel):
    component_name: str | None = None
    component_type: str | None = None
    amount: float | None = None
    effective_from: date | None = None
    effective_to: date | None = None


class SalaryStructureResponse(BaseModel):
    salary_structure_id: int
    employee_id: int
    component_name: str
    component_type: str
    amount: float
    effective_from: date
    effective_to: date | None

    class Config:
        from_attributes = True
