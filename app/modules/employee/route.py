from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from app.modules.employee.schema import (EmployeeCreate,EmployeeUpdate,EmployeeResponse)
from app.core.database import get_db
from app.modules.employee import service
from app.modules.auth.dependancy import require_roles,get_current_user

router = APIRouter(
    prefix="/api/employee",
    tags=["Employee"]
)

@router.post("/",response_model=EmployeeResponse,dependencies=[Depends(require_roles("Admin","HR"))])
def create_employee(employee:EmployeeCreate,db:Session=Depends(get_db)):
    db_employee, error = service.create_employee(db, employee)

    if error == "role_not_found":
        raise HTTPException(404, "Role not found")

    if error == "department_not_found":
        raise HTTPException(404, "Department not found")

    if error == "designation_not_found":
        raise HTTPException(404, "Designation not found")

    if error == "self_manager":
        raise HTTPException(
        status_code=400,
        detail="Employee cannot be their own manager"
    )

    if error == "manager_not_found":
        raise HTTPException(404, "Manager not found")

    if error == "duplicate":
        raise HTTPException(400, "Email or phone already exists")

    return employee_response(db_employee)


## used to get a single employee information
@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
    dependencies=[Depends(require_roles("Admin", "HR", "Employee", "Manager"))]
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] == "Employee":
        if int(current_user["sub"]) != employee_id:
            raise HTTPException(
                status_code=403,
                detail="Employee can only access their own information"
            )

    db_employee = service.get_employee(db, employee_id)

    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee_response(db_employee)

## used to get information for all employees
@router.get(
    "/",
    response_model=list[EmployeeResponse],
    dependencies=[Depends(require_roles("Admin", "HR", "Employee", "Manager"))]
)
def get_employees(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] == "Employee":
        employee = service.get_employee(db, int(current_user["sub"]))

        if not employee:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        return [employee_response(employee)]

    return [
        employee_response(employee)
        for employee in service.get_employee(db, None)
    ]



@router.put("/{employee_id}",response_model=str,dependencies=[Depends(require_roles("Admin","HR"))])
def update_employee(employee_id:int,employee:EmployeeUpdate,db:Session=Depends(get_db)):
    db_employee, error = service.update_employee(
    db, employee_id, employee
)

    if error == "not_found":
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    if error == "duplicate_email":
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    if error == "duplicate_phone":
        raise HTTPException(
            status_code=400,
            detail="Phone already exists"
        )

    return f"Employee with employee_id:{employee_id} Updated Successfully"

@router.delete("/{employee_id}",response_model=str,dependencies=[Depends(require_roles("Admin","HR"))])
def delete_employee(employee_id:int,db:Session=Depends(get_db)):
    db_employee=service.delete_employee(db,employee_id)
    if not db_employee:
        raise HTTPException(status_code=404,detail="Employee not exist")
    return "Employee Deleted Successfully"

def employee_response(employee):
    return {
        "employee_id": employee.employee_id,
        "name": employee.name,
        "email": employee.email,
        "phone": employee.phone,
        "dob": employee.dob,
        "gender": employee.gender,
        "role": employee.role.name,
        "department": employee.department.departmentName,
        "designation": employee.designation.name,
        "manager_id": employee.manager_id,
        "manager": employee.manager.name if employee.manager else None,
        "remaining_leave_days": employee.remaining_leave_days,
        "status": employee.status
    }
