from pydantic import BaseModel
from datetime import date ,time

class AttendanceResponse(BaseModel):
    attendanceDate : date
    attendance_id : int
    check_in : time | None
    check_out : time | None
    employee_id :int

    class Config:
        from_attributes=True

class MonthlyAttendanceSummary(BaseModel):
    employee_id : int
    month : int
    year : int
    present_days : int

    class Config:
        from_attributes=True
