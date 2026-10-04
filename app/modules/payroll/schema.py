from pydantic import BaseModel
from datetime import date


class PayrollCreate(BaseModel):
    employee_id: int
    payroll_month: date


class PayrollUpdate(BaseModel):
    status: str | None = None


class PayrollResponse(BaseModel):
    payroll_id: int
    employee_id: int
    payroll_month: date
    gross_salary: float
    total_deductions: float
    tax: float
    net_salary: float
    status: str

    class Config:
        from_attributes = True
