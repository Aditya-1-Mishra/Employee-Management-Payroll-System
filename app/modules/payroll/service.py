from sqlalchemy.orm import Session

from app.modules.payroll.model import Payroll
from app.modules.salary_structure.model import SalaryStructure


def calculate_tax(gross_salary: float):
    if gross_salary <= 25000:
        return 0

    if gross_salary <= 50000:
        return gross_salary * 0.05

    if gross_salary <= 100000:
        return gross_salary * 0.10

    return gross_salary * 0.20


def calculate_salary(db: Session, employee_id: int):
    salary_structures = db.query(SalaryStructure).filter(
        SalaryStructure.employee_id == employee_id
    ).all()

    if not salary_structures:
        return None

    gross_salary = 0
    total_deductions = 0

    for salary in salary_structures:
        if salary.component_type == "Earning":
            gross_salary += salary.amount

        elif salary.component_type == "Deduction":
            total_deductions += salary.amount

    tax = calculate_tax(gross_salary)

    net_salary = gross_salary - total_deductions - tax

    return {
        "gross_salary": gross_salary,
        "total_deductions": total_deductions,
        "tax": tax,
        "net_salary": net_salary
    }


def create_payroll(db: Session, data):
    salary = calculate_salary(db, data.employee_id)

    if salary is None:
        return None

    payroll = Payroll(
        employee_id=data.employee_id,
        payroll_month=data.payroll_month,
        gross_salary=salary["gross_salary"],
        total_deductions=salary["total_deductions"],
        tax=salary["tax"],
        net_salary=salary["net_salary"],
        status="Generated"
    )

    db.add(payroll)
    db.commit()
    db.refresh(payroll)

    return payroll


def get_payrolls(db: Session):
    return db.query(Payroll).all()


def get_payroll(db: Session, payroll_id: int):
    return db.query(Payroll).filter(
        Payroll.payroll_id == payroll_id
    ).first()


def update_payroll(db: Session, payroll_id: int, data):
    payroll = get_payroll(db, payroll_id)

    if payroll is None:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(payroll, key, value)

    db.commit()
    db.refresh(payroll)

    return payroll


def delete_payroll(db: Session, payroll_id: int):
    payroll = get_payroll(db, payroll_id)

    if payroll is None:
        return None

    db.delete(payroll)
    db.commit()

    return payroll
