from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.modules.designation.schema import (
    DesignationCreate,
    DesignationUpdate,
    DesignationResponse
)

from app.modules.designation import service


router = APIRouter(
    prefix="/api/designations",
    tags=["Designations"]
)


@router.post("/", response_model=DesignationResponse)
def create_designation(
    designation: DesignationCreate,
    db: Session = Depends(get_db)
):
    return service.create_designation(db, designation)


@router.get("/", response_model=list[DesignationResponse])
def get_designations(
    db: Session = Depends(get_db)
):
    return service.get_designations(db)


@router.get("/{designation_id}", response_model=DesignationResponse)
def get_designation(
    designation_id: int,
    db: Session = Depends(get_db)
):
    designation = service.get_designation(db, designation_id)

    if not designation:
        raise HTTPException(
            status_code=404,
            detail="Designation not found"
        )

    return designation


@router.put("/{designation_id}", response_model=DesignationResponse)
def update_designation(
    designation_id: int,
    designation: DesignationUpdate,
    db: Session = Depends(get_db)
):
    updated_designation = service.update_designation(
        db,
        designation_id,
        designation
    )

    if not updated_designation:
        raise HTTPException(
            status_code=404,
            detail="Designation not found"
        )

    return updated_designation


@router.delete("/{designation_id}")
def delete_designation(
    designation_id: int,
    db: Session = Depends(get_db)
):
    deleted_designation = service.delete_designation(
        db,
        designation_id
    )

    if not deleted_designation:
        raise HTTPException(
            status_code=404,
            detail="Designation not found"
        )

    return {
        "message": "Designation deleted successfully"
    }
