from sqlalchemy.orm import Session
from app.modules.employee.model import Employee
from app.modules.employee.schema import EmployeeCreate, EmployeeUpdate
from app.core.security import hash_password
from app.modules.roles.model import Role
from app.modules.department.model import Department
from app.modules.designation.model import Designation

# CRUD operations for Employee model

## create a new employee
def create_employee(db: Session, employee: EmployeeCreate):
    existing_employee = db.query(Employee).filter(
        (Employee.email == employee.email) | (Employee.phone == employee.phone)
    ).first()

    if existing_employee:
        return None  # Employee with the same email or phone already exists

    # here we check if the provided ids exist or not
    role = db.query(Role).filter(
    Role.role_id == employee.role_id
    ).first()

    department = db.query(Department).filter(
        Department.department_id == employee.department_id
    ).first()

    designation = db.query(Designation).filter(
        Designation.designation_id == employee.designation_id
    ).first()

    if not role:
        return None, "role_not_found"

    if not department:
        return None, "department_not_found"

    if not designation:
        return None, "designation_not_found"

    if employee.manager_id is not None:
        manager = db.query(Employee).filter(
            Employee.employee_id == employee.manager_id
        ).first()

        if not manager:
            return None, "manager_not_found"

    hashed_password = hash_password(employee.password)
    db_employee = Employee(
        name=employee.name,
        email=employee.email,
        phone=employee.phone,
        dob=employee.dob,
        password_hash=hashed_password,
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
def update_employee(db: Session, employee_id: int, employee: EmployeeUpdate):
    db_employee = db.query(Employee).filter(
        Employee.employee_id == employee_id
    ).first()

    if not db_employee:
        return None, "not_found"

    update_data = employee.model_dump(exclude_unset=True)

    if "email" in update_data:
        existing_email = db.query(Employee).filter(
            Employee.email == update_data["email"],
            Employee.employee_id != employee_id
        ).first()

        if existing_email:
            return None, "duplicate_email"

    if "phone" in update_data and update_data["phone"] is not None:
        existing_phone = db.query(Employee).filter(
            Employee.phone == update_data["phone"],
            Employee.employee_id != employee_id
        ).first()

        if existing_phone:
            return None, "duplicate_phone"

    if "password" in update_data:
        db_employee.password_hash = hash_password(
            update_data.pop("password")
        )

    if "role_id" in update_data:
        role = db.query(Role).filter(
            Role.role_id == update_data["role_id"]
        ).first()

        if not role:
            return None, "role_not_found"

    if "department_id" in update_data:
        department = db.query(Department).filter(
            Department.department_id == update_data["department_id"]
        ).first()

        if not department:
            return None, "department_not_found"

    if "designation_id" in update_data:
        designation = db.query(Designation).filter(
            Designation.designation_id == update_data["designation_id"]
        ).first()

        if not designation:
            return None, "designation_not_found"

    if "manager_id" in update_data and update_data["manager_id"] == employee_id:
        return None, "self_manager"

    if "manager_id" in update_data and update_data["manager_id"] is not None:
        manager = db.query(Employee).filter(
            Employee.employee_id == update_data["manager_id"]
        ).first()

        if not manager:
            return None, "manager_not_found"

    for key, value in update_data.items():
        setattr(db_employee, key, value)

    db.commit()
    db.refresh(db_employee)

    return db_employee, None

## get existing employee information
def get_employee(db:Session,employee_id:int|None):
    if employee_id is None: ## if employee_id is None, return all employees
        return db.query(Employee).all()
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
