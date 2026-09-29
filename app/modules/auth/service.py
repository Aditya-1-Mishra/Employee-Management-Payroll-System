from app.modules.auth.schema import LoginRequest, LoginResponse
from sqlalchemy.orm import Session
from app.modules.employee.model import Employee
from app.core.security import verify_password, create_access_token

def authenticate_user(db:Session, email:str, password:str):
    user = db.query(Employee).filter(Employee.email == email).first() # here .first() return the first result of the query response.
    if not user :
        return None
    if not verify_password(password,user_password=user.password_hash):
        return None

    return user

def LoginUser(db:Session, LoginRequest:LoginRequest):
    user = authenticate_user(db, LoginRequest.email, LoginRequest.password)
    if not user:
        return None
    access_token = create_access_token(
        data={
            "sub":str(user.employee_id),
            "role":user.role_id
            }
        )
    return LoginResponse(access_token=access_token, token_type="bearer")
