from sqlalchemy.orm import Session
from app.modules.leave.model import Leave
from app.modules.leave.schema import LeaveCreate,LeaveUpdateStatus
from app.modules.employee.model import Employee


def apply_leave(db: Session, leave: LeaveCreate):
    db_leave = Leave(
        employee_id=leave.employee_id,
        leave_type=leave.leave_type,
        start_date=leave.start_date,
        end_date=leave.end_date,
        reason=leave.reason,
        status="Pending"
    )

    number_of_days = (leave.end_date - leave.start_date).days + 1
    employee = db.query(Employee).filter(Employee.employee_id == leave.employee_id).first()

    if not employee:
        return None

    if number_of_days > employee.remaining_leave_days:
        return None

    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)

    return db_leave

## No need to add that remaining day leave calculation here cause if the leave is applied it means 
## that the mployee still has remaining leave days and that is why leave is applied successffully.
def update_leave_status(db:Session,leave_id:int,status:str):
    leave = db.query(Leave).filter(Leave.leave_id == leave_id).first()

    if not leave :
        return None

    if status == "Approved" and leave.status == "Approved":
        return None
    leave.status = status

    if status == "Approved":
        number_of_days = (leave.end_date - leave.start_date).days + 1
        employee = db.query(Employee).filter(Employee.employee_id == leave.employee_id).first()
        employee.remaining_leave_days -= number_of_days
        db.refresh(employee)

    db.commit() 
    db.refresh(leave)

    return leave

# leave update service is also present in this file which is used to update the leave status by admin or manager.

def get_leave_history(db: Session, employee_id: int):
    leave_history = db.query(Leave).filter(Leave.employee_id == employee_id).all()
    return leave_history
