from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError
from fastapi import HTTPException, status
from db.db import get_db
from sqlalchemy.orm import Session
from db import models


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = '9cd7882c137a23457275763b226d4538f0d6272c517223771d46463b095af150'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()

  if expires_delta:
    expire = datetime.now() + expires_delta
  else:
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})

  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user: str = str(payload.get("sub"))
        if user is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    current_user = db.query(models.User).filter(models.User.email == user["email"]).first()

    if current_user is None:
        raise credentials_exception
    
    return current_user.__dict__