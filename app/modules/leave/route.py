from fastapi import Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session
from app.modules.leave.schema import LeaveCreate, LeaveResponse, LeaveHistoryResponse
from app.core.database import get_db    
from app.modules.leave import service
from app.modules.auth.dependancy import require_roles

router = APIRouter(
    prefix = "/api/leave",
    tags = ["Leave"])

@router.post('/apply_leave',dependencies=[Depends(require_roles('Employee'))],response_model=LeaveResponse)
def apply_leave(leave:LeaveCreate,db:Session=Depends(get_db)):
    db_leave = service.apply_leave(db,leave)

    if not db_leave:
        raise HTTPException(
            status_code=400,
            detail = "Leave application failed"
        )
    return db_leave

@router.put('/update_leave_status/{leave_id}',dependencies=[Depends(require_roles('Admin','Manager'))],response_model=LeaveResponse)
def update_leave_status(leave_id:int,status:str,db:Session=Depends(get_db)):

    if status not in ['Approved','Rejected']:
        raise HTTPException(
            status_code=400,
            detail = "Invalid status. Status must be either 'Approved' or 'Rejected'."
        )
    db_leave = service.update_leave_status(db,leave_id,status)

    if not db_leave:
        raise HTTPException(
            status_code=404,
            detail = "Leave not found"
        )
    return db_leave

@router.get('/leave_history/{employee_id}',dependencies=[Depends(require_roles('Employee'))],response_model=list[LeaveHistoryResponse])
def get_leave_history(employee_id:int,db:Session=Depends(get_db)):
    leave_history = service.get_leave_history(db,employee_id)

    if not leave_history:
        raise HTTPException(
            status_code=404,
            detail = "No leave history found for the employee"
        )
    return leave_history
