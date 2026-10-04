from sqlalchemy.orm import Session
from app.modules.salary_structure.model import SalaryStructure
from app.modules.salary_structure.schema import SalaryStructureCreate, SalaryStructureUpdate


def create_salary_structure(db: Session, data: SalaryStructureCreate):
    salary = SalaryStructure(
        employee_id=data.employee_id,
        component_name=data.component_name,
        component_type=data.component_type,
        amount=data.amount,
        effective_from=data.effective_from,
        effective_to=data.effective_to
    )

    db.add(salary)
    db.commit()
    db.refresh(salary)

    return salary


def get_salary_structures(db: Session):
    return db.query(SalaryStructure).all()


def get_salary_structure(db: Session, salary_structure_id: int):
    return db.query(SalaryStructure).filter(
        SalaryStructure.salary_structure_id == salary_structure_id
    ).first()


def update_salary_structure(
    db: Session,
    salary_structure_id: int,
    data: SalaryStructureUpdate
):
    salary = get_salary_structure(db, salary_structure_id)

    if salary is None:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(salary, key, value)

    db.commit()
    db.refresh(salary)

    return salary


def delete_salary_structure(db: Session, salary_structure_id: int):
    salary = get_salary_structure(db, salary_structure_id)

    if salary is None:
        return None

    db.delete(salary)
    db.commit()

    return salary
