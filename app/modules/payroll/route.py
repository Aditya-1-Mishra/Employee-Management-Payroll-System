from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.payroll.schema import (
    PayrollCreate,
    PayrollUpdate,
    PayrollResponse
)
from app.modules.payroll import service
from app.core.security import require_roles


router = APIRouter(
    prefix="/api/payroll",
    tags=["Payroll"]
)


@router.post("/", response_model=PayrollResponse,dependencies =[ Depends(require_roles("Admin", "HR"))])
def create_payroll(
    data: PayrollCreate,
    db: Session = Depends(get_db)
):
    payroll = service.create_payroll(db, data)

    if payroll is None:
        raise HTTPException(
            status_code=404,
            detail="Salary structure not found for employee"
        )

    return payroll


@router.get("/", response_model=list[PayrollResponse],dependencies =[ Depends(require_roles("Admin", "HR"))])
def get_payrolls(
    db: Session = Depends(get_db)
):
    return service.get_payrolls(db)


@router.get("/{payroll_id}", response_model=PayrollResponse,dependencies =[ Depends(require_roles("Admin", "HR"))])
def get_payroll(
    payroll_id: int,
    db: Session = Depends(get_db)
):
    payroll = service.get_payroll(db, payroll_id)

    if payroll is None:
        raise HTTPException(
            status_code=404,
            detail="Payroll not found"
        )

    return payroll


@router.put("/{payroll_id}", response_model=PayrollResponse,dependencies =[ Depends(require_roles("Admin", "HR"))])
def update_payroll(
    payroll_id: int,
    data: PayrollUpdate,
    db: Session = Depends(get_db)
):
    payroll = service.update_payroll(
        db,
        payroll_id,
        data
    )

    if payroll is None:
        raise HTTPException(
            status_code=404,
            detail="Payroll not found"
        )

    return payroll


@router.delete("/{payroll_id}",dependencies =[ Depends(require_roles("Admin", "HR"))])
def delete_payroll(
    payroll_id: int,
    db: Session = Depends(get_db)
):
    payroll = service.delete_payroll(
        db,
        payroll_id
    )

    if payroll is None:
        raise HTTPException(
            status_code=404,
            detail="Payroll not found"
        )

    return {
        "message": "Payroll deleted successfully"
    }
