from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.auth.schema import LoginRequest, LoginResponse
from app.modules.auth.service import LoginUser
from app.core.database import get_db


router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
    )

@router.post("/Login",response_model=LoginResponse)
def Login_user(LoginRequest:LoginRequest,db:Session=Depends(get_db)):
    user = LoginUser(db,LoginRequest)
    if not user:
        raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Invalid email or password"
        )
    return user 
# here user is an instance of LoginResponse which is returned as a response to the client. Which contains the access_token and token_type.
