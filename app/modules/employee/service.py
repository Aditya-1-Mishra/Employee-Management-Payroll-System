from sqlalchemy.orm import Session
from app.modules.employee.model import Employee
from app.modules.employee.schema import EmployeeCreate, EmployeeUpdate

# CRUD operations for Employee model

## create a new employee
def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(
        name=employee.name,
        email=employee.email,
        phone=employee.phone,
        dob=employee.dob,
        password=employee.password,
        status=employee.status,
        gender=employee.gender,
        role_id=employee.role_id,
        department_id=employee.department_id,
        designation_id=employee.designation_id,
        manager_id=employee.manager_id
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

## update existing employee
def update_employee(db:Session , employee_id:int, employee:EmployeeUpdate):
    db_employee = db.query(Employee).filter(Employee.employee_id==employee_id).first()
    if not db_employee:
        return None

    update_data = employee.model_dump(exclude_unset=True)

    for key,value in update_data.items():
        setattr(db_employee,key,value)

    db.commit()
    db.refresh(db_employee)
    return db_employee

## get existing employee information
def get_employee(db:Session,employee_id:int):
    data = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if data:
        return data
    return None

## delete existing employee
def delete_employee(db:Session,employee_id:int):
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not employee:
        return None
    db.delete(employee)
    db.commit()
    return employee
