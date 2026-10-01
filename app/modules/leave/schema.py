from pydantic import BaseModel
from datetime import date


class LeaveCreate(BaseModel):
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: str | None = None


class LeaveResponse(BaseModel):
    leave_id: int
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: str | None
    status: str

    class Config:
        from_attributes = True

class LeaveUpdateStatus(BaseModel):
    status: str

    class Config:
        from_attributes = True

class LeaveHistoryResponse(BaseModel):
    leave_id: int
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: str | None
    status: str

    class Config:
        from_attributes = True
