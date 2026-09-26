from sqlalchemy.orm import Session
from app.modules.department.model import Department
from app.modules.department.schema import DepartmentCreate,DepartmentUpdate

def department_create(db:Session,department:DepartmentCreate):
    db_department =Department(
        departmentName = department.departmentName,
        description = department.description
    )
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def department_update(db:Session,department_id:int,department:DepartmentUpdate):
    db_department = db.query(Department).filter(
        Department.department_id == department_id
    ).first()

    if db_department is None:
        return None

    data = department.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(db_department, key, value)

    db.commit()
    db.refresh(db_department)

    return db_department

def get_departments(db:Session):
    return db.query(Department).all()

def get_department(db:Session,department_id:int):
    return db.query(Department).filter(Department.department_id == department_id).first()

def delete_department(db:Session,department_id:int):
    db_department = db.query(Department).filter(Department.department_id == department_id).first()

    if not db_department:
        return None

    db.delete(db_department)
    db.commit()

    return db_department
