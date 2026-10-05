from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.roles.schema import (
    RoleCreate,
    RoleUpdate,
    RoleResponse
)
from app.modules.roles import service
from app.modules.auth.dependancy import require_roles


router = APIRouter(
    prefix="/api/role",
    tags=["Role"]
)


@router.post(
    "/",
    response_model=RoleResponse,
    dependencies=[Depends(require_roles("Admin"))]
)
def create_role(
    data: RoleCreate,
    db: Session = Depends(get_db)
):
    return service.create_role(db, data)


@router.get(
    "/",
    response_model=list[RoleResponse],
    dependencies=[Depends(require_roles("Admin", "HR", "Manager"))]
)
def get_roles(
    db: Session = Depends(get_db)
):
    return service.get_roles(db)


@router.get(
    "/{role_id}",
    response_model=RoleResponse,
    dependencies=[Depends(require_roles("Admin", "HR", "Manager"))]
)
def get_role(
    role_id: int,
    db: Session = Depends(get_db)
):
    role = service.get_role(db, role_id)

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    return role


@router.put(
    "/{role_id}",
    response_model=RoleResponse,
    dependencies=[Depends(require_roles("Admin"))]
)
def update_role(
    role_id: int,
    data: RoleUpdate,
    db: Session = Depends(get_db)
):
    role = service.update_role(
        db,
        role_id,
        data
    )

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    return role


@router.delete(
    "/{role_id}",
    dependencies=[Depends(require_roles("Admin"))]
)
def delete_role(
    role_id: int,
    db: Session = Depends(get_db)
):
    role = service.delete_role(
        db,
        role_id
    )

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )

    return {
        "message": "Role deleted successfully"
    }
