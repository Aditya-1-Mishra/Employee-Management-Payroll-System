from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from app.modules.department import service
from app.modules.department.schema import DepartmentUpdate,DepartmentCreate,DepartmentResponse
from app.core.database import get_db
from app.modules.auth.dependancy import require_roles

router = APIRouter(
    prefix="/api/department",
    tags=['Department']
)

@router.post('/',dependencies=[Depends(require_roles("Admin"))])
def department_create(department:DepartmentCreate,db:Session=Depends(get_db)):
    db_department = service.department_create(db,department)
    return db_department

@router.get('/{department_id}',response_model=DepartmentResponse,dependencies=[Depends(require_roles("Admin","HR","Employee","Manager"))])
def get_department(department_id:int,db:Session=Depends(get_db)):
    db_department = service.get_department(db,department_id)
    if not db_department:
        raise HTTPException(status_code=404,detail="Department not found")
    return db_department

@router.get('/',response_model=list[DepartmentResponse],dependencies=[Depends(require_roles("Admin","HR","Employee","Manager"))])
def get_departments(db:Session=Depends(get_db)):
    return service.get_departments(db)

@router.put('/{department_id}',response_model=str,dependencies=[Depends(require_roles("Admin","HR","Manager"))])
def department_update(department_id:int,department:DepartmentUpdate,db:Session=Depends(get_db)):
    db_department = service.department_update(db,department_id,department)
    if not db_department:
        raise HTTPException(status_code=404,detail="Department not exist")
    return f"Department with department_id:{department_id} Updated Successfully"

@router.delete('/{department_id}',response_model=str,dependencies=[Depends(require_roles("Admin"))])
def delete_department(department_id:int,db:Session=Depends(get_db)):    
    db_department = service.delete_department(db,department_id)
    if not db_department:
        raise HTTPException(status_code=404,detail="Department not exist")
    return "Department Deleted Successfully"
