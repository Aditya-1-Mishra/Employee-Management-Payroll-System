import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hasher = PasswordHash((Argon2Hasher(),))

def hash_password(password: str) -> str:
    return password_hasher.hash(password)

def verify_password(password:str, user_password:str)->bool:
    return password_hasher.verify(password,user_password)

def create_access_token(data:dict, expires_delta:timedelta=None):
    to_encode = data.copy()
    if not expires_delta: # when no information is provided realted to the expiring of session 
        expires_delta = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    else : # this here will explicitly provide the duration through which employee session stay active
        expires_delta = datetime.now(timezone.utc)+expires_delta
    to_encode.update({"exp":expires_delta})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)




# print(SECRET_KEY)
