from app.modules.attendance.model import Attendance
from sqlalchemy.orm import Session
from datetime import datetime

def check_in(db:Session,employee_id:int):
    today = datetime.now().date()
    attendance = db.query(Attendance).filter(Attendance.employee_id == employee_id,
                                            Attendance.attendanceDate == today ).first()
    if attendance : 
        return None

    attendance = Attendance(employee_id=employee_id,
                            attendanceDate=today,
                            check_in = datetime.now().time())
    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    return attendance

def check_out(db:Session,employee_id:int):
    today = datetime.now().date()
    attendance = db.query(Attendance).filter(Attendance.employee_id == employee_id,
                                                Attendance.attendanceDate == today ).first()
    if not attendance or not attendance.check_in:
        return None

    if attendance.check_out:
        return None

    attendance.check_out = datetime.now().time()
    
    db.commit()
    db.refresh(attendance)

    return attendance
