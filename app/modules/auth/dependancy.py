# here we just validate whether the user is allowed to access those services or not
# such as employee is not allowed to create another new employee.
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/Login")

def get_current_user(token:str=Depends(oauth2_scheme)):
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or expired token"
        )

    return payload

def require_roles(*allowed_roles):
    def role_checker(current_user = Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not permitted to use following services"
            )
        return current_user
    return role_checker
