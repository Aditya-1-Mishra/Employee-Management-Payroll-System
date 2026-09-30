from sqlalchemy import Column,Integer,Date,Time,ForeignKey
from app.core.database import Base

class Attendance(Base):
    __tablename__ = "Attendance"

    attendance_id = Column(Integer,primary_key=True,index=True)
    attendanceDate = Column(Date,nullable=False)
    check_in = Column(Time,nullable=True)
    check_out = Column(Time,nullable=True)

    employee_id = Column(Integer,ForeignKey("Employees.employee_id"),nullable=False)
