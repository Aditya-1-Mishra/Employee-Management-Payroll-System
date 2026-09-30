from fastapi import Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session
from app.modules.attendance.schema import AttendanceResponse
from app.core.database import get_db
from app.modules.attendance import service
from app.modules.auth.dependancy import require_roles

router = APIRouter(
    prefix = "/api/attendance",
    tags = ["attendance"]
)

@router.post('/check_in',dependencies=[Depends(require_roles('Employee'))],response_model=AttendanceResponse)
def check_in(employee_id:int,db:Session=Depends(get_db)):
    db_attendance = service.check_in(db,employee_id)

    if not db_attendance:
        raise HTTPException(
            status_code=400,
            detail = "Employee has already checked in"
        )
    return db_attendance

@router.post('/check_out',dependencies=[Depends(require_roles("Employee"))],response_model=AttendanceResponse)
def check_out(employee_id:int,db=Depends(get_db)):
    db_attendance = service.check_out(db,employee_id)

    if not db_attendance:
        raise HTTPException(
            status_code=400,
            detail ="Invalid check-out request"
        )
    return db_attendance
