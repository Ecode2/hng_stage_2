
from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, Field, field_validator

class UserModel(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str
    phone: str | None = None

    @field_validator('firstName')
    def check_firstName(cls, v):
        if not v and not isinstance(v, str):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                        detail={"errors":[
                            {"field":"string",
                             "message": "string"}
                        ]})
        return v
    @field_validator('lastName')
    def check_lastName(cls, v):
        if not v and not isinstance(v, str):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                        detail={"errors":[
                            {"field":"string",
                             "message": "string"}
                        ]})
        return v
    @field_validator('email')
    def check_email(cls, v):
        if not v and not isinstance(v, EmailStr):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                        detail={"errors":[
                            {"field":"string",
                             "message": "string"}
                        ]})
        return v
    @field_validator('password')
    def check_firstName(cls, v):
        if not v and not isinstance(v, str):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                        detail={"errors":[
                            {"field":"string",
                             "message": "string"}
                        ]})
        return v

class LoginModel(BaseModel):
    email: EmailStr
    password: str

    @field_validator('email')
    def check_email(cls, v):
        if not v and not isinstance(v, EmailStr):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                        detail={"errors":[
                            {"field":"string",
                             "message": "string"}
                        ]})
        return v
    
    @field_validator('password')
    def check_password(cls, v):
        if not v and not isinstance(v, str):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                        detail={"errors":[
                            {"field":"string",
                             "message": "string"}
                        ]})
        return v

class OrganisationModel(BaseModel):
    name: str
    description: str | None = None
    
    @field_validator('name')
    def check_name(cls, v):
        if not v and not isinstance(v, str):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                        detail={"errors":[
                            {"field":"string",
                             "message": "string"}
                        ]})
        return v