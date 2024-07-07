from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from db.db import get_db
from db import models
from db.hash import Hash
from utils import create_access_token 
from schemas import UserModel

router = APIRouter(
    tags=["Authentication"],
    prefix="/auth"
    )

@router.post("register", status_code=201)
async def register_user(user_info: UserModel = Depends(), db:Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_info.email).first()
    error = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=
                          {"status": "Bad request",
                           "message": "Registration unsuccessful",
                           "statusCode": 400})
    if user:
        raise error
    
    try:
        new_user = models.User(
            firstName = user_info.firstName,
            lastName = user_info.lastName,
            email = user_info.email,
            password = Hash.bcrypt(user_info.password),
            phone = user_info.phone
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to store in DB. error {e}")
    
    get_new_user = db.query(models.User).filter(models.User.email == user_info.email).first()
    format_user = UserModel(**get_new_user)

    access_token = create_access_token(data={'sub': format_user.model_dump()})

    return {
        "status": "success",
        "message": "Registration successful",
        "data": {
            "accessToken": access_token,
            "user": {**format_user.model_dump()}
        }
    }, 201