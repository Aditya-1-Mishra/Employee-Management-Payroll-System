from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from app.core.database import Base


class Payroll(Base):
    __tablename__ = "payrolls"

    payroll_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    payroll_month = Column(Date, nullable=False)

    gross_salary = Column(Float, nullable=False)
    total_deductions = Column(Float, nullable=False)
    tax = Column(Float, nullable=False)
    net_salary = Column(Float, nullable=False)

    status = Column(String(50), nullable=False)
