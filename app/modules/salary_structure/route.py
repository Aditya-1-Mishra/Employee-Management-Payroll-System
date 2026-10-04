from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.salary_structure.schema import (
    SalaryStructureCreate,
    SalaryStructureUpdate,
    SalaryStructureResponse
)
from app.modules.salary_structure import service
from app.modules.auth.dependancy import require_roles


router = APIRouter(
    prefix="/api/salary-structure",
    tags=["Salary Structure"]
)


@router.post("/", response_model=SalaryStructureResponse, dependencies=[Depends(require_roles('Admin', 'Manager'))])
def create_salary_structure(
    data: SalaryStructureCreate,
    db: Session = Depends(get_db)
):
    return service.create_salary_structure(db, data)


@router.get("/", response_model=list[SalaryStructureResponse], dependencies=[Depends(require_roles('Admin', 'Manager'))])
def get_salary_structures(db: Session = Depends(get_db)):
    return service.get_salary_structures(db)


@router.get("/{salary_structure_id}", response_model=SalaryStructureResponse, dependencies=[Depends(require_roles('Admin', 'Manager'))])
def get_salary_structure(
    salary_structure_id: int,
    db: Session = Depends(get_db)
):
    salary = service.get_salary_structure(db, salary_structure_id)

    if salary is None:
        raise HTTPException(status_code=404, detail="Salary structure not found")

    return salary


@router.put("/{salary_structure_id}", response_model=SalaryStructureResponse, dependencies=[Depends(require_roles('Admin', 'Manager'))])
def update_salary_structure(
    salary_structure_id: int,
    data: SalaryStructureUpdate,
    db: Session = Depends(get_db)
):
    salary = service.update_salary_structure(
        db,
        salary_structure_id,
        data
    )

    if salary is None:
        raise HTTPException(status_code=404, detail="Salary structure not found")

    return salary


@router.delete("/{salary_structure_id}", dependencies=[Depends(require_roles('Admin', 'Manager'))])
def delete_salary_structure(
    salary_structure_id: int,
    db: Session = Depends(get_db)
):
    salary = service.delete_salary_structure(
        db,
        salary_structure_id
    )

    if salary is None:
        raise HTTPException(status_code=404, detail="Salary structure not found")

    return {"message": "Salary structure deleted successfully"}
