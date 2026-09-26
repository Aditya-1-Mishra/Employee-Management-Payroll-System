from sqlalchemy.orm import Session

from app.modules.designation.model import Designation
from app.modules.designation.schema import ( DesignationCreate, DesignationUpdate )


def create_designation(db: Session, designation: DesignationCreate):
    db_designation = Designation(
        name=designation.name,
        description=designation.description,
        status=designation.status
    )

    db.add(db_designation)
    db.commit()
    db.refresh(db_designation)

    return db_designation


def get_designations(db: Session):
    return db.query(Designation).all()


def get_designation(db: Session, designation_id: int):
    return db.query(Designation).filter(
        Designation.designation_id == designation_id
    ).first()


def update_designation(
    db: Session,
    designation_id: int,
    designation: DesignationUpdate
):
    db_designation = db.query(Designation).filter(
        Designation.designation_id == designation_id
    ).first()

    if not db_designation:
        return None

    data = designation.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(db_designation, key, value)

    db.commit()
    db.refresh(db_designation)

    return db_designation


def delete_designation(db: Session, designation_id: int):
    db_designation = db.query(Designation).filter(
        Designation.designation_id == designation_id
    ).first()

    if not db_designation:
        return None

    db.delete(db_designation)
    db.commit()

    return db_designation
