from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from app.modules.employee.schema import (EmployeeCreate,EmployeeUpdate,EmployeeResponse)
from app.modules.employee.model import Employee
from app.core.database import get_db
from app.modules.employee import service

router = APIRouter(
    prefix="/api/employee",
    tags=["Employee"]
)

@router.post("/",response_model=EmployeeResponse)
def create_employee(employee:EmployeeCreate,db:Session=Depends(get_db)):
    db_employee = service.create_employee(db,employee)
    return db_employee


## used to get a single employee information
@router.get("/{employee_id}",response_model=EmployeeResponse)
def get_employee(employee_id:int,db:Session=Depends(get_db)):
    db_employee = service.get_employee(db,employee_id)
    if not db_employee:
        raise HTTPException(status_code=404,detail="Employee not found")
    return db_employee

## used to get information for all employees
@router.get("/",response_model=list[EmployeeResponse])
def get_employees(db:Session=Depends(get_db)):
    return service.get_employee(db,None)

@router.put("/{employee_id}",response_model=str)
def update_employee(employee_id:int,employee:EmployeeUpdate,db:Session=Depends(get_db)):
    db_employee = service.update_employee(db,employee_id,employee)
    if not db_employee:
        raise HTTPException(status_code=404,detail="Employee not exist")
    return f"Employee with employee_id:{employee_id} Updated Successfully"

@router.delete("/{employee_id}",response_model=str)
def delete_employee(employee_id:int,db:Session=Depends(get_db)):
    db_employee=service.delete_employee(employee_id,db)
    if not db_employee:
        raise HTTPException(status_code=404,detail="Employee not exist")
    return "Employee Deleted Successfully"
