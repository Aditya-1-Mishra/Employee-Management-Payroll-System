from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from app.core.database import Base


class SalaryStructure(Base):
    __tablename__ = "salary_structures"

    salary_structure_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    component_name = Column(String(100), nullable=False)
    component_type = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)
