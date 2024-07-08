from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from db.db import get_db
from db import models
from db.hash import Hash
from utils import create_access_token 
from schemas import LoginModel, UserModel

router = APIRouter(
    tags=["Authentication"],
    prefix="/auth"
    )

@router.post("/register", status_code=201)
async def register_user(user_info: UserModel, db:Session = Depends(get_db)):
    
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
    
    get_new_user = db.query(models.User).filter(models.User.email == user_info.email)
    user_dict = get_new_user.__dict__

    new_organisation = models.Organisation(
        name = f"{user_info.firstName}'s Organisation",
        description =  f"{user_info.firstName}'s new Organisation",
        user_id = [user_dict.get("userId")]
    )

    db.add(new_organisation)
    db.commit()
    db.refresh(new_organisation)

    user_organisation = db.query(models.Organisation).filter(models.Organisation.name == f"{user_info.firstName}'s Organisation").first()

    get_new_user.update({models.User.organisation_id: [user_organisation.__dict__.get("orgId")]})
    db.commit()

    format_user = UserModel(**get_new_user.first().__dict__)

    access_token = create_access_token(data={'sub': format_user.model_dump()})

    public_user = get_new_user.first().__dict__
    public_user.pop("password")

    return {
        "status": "success",
        "message": "Registration successful",
        "data": {
            "accessToken": access_token,
            "user": {**public_user}
        }
    }

@router.post("/login", status_code=200)
async def login_user(user_info: LoginModel, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_info.email).first()
    error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=
                          {"status": "Bad request",
                           "message": "Authentication Failed",
                           "statusCode": 401})
    
    if not user:
        raise error
    if not Hash.verify(str(user.password), user_info.password):
        raise error
    
    format_user = UserModel(**user.__dict__)
    access_token = create_access_token(data={'sub': format_user.model_dump()})

    public_user = user.__dict__
    public_user.pop("password")

    return {
        "status": "success",
        "message": "Login successful",
        "data": {
            "accessToken": access_token,
            "user": {**public_user}
        }
    }