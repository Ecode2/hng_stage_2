
from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, Field, field_validator

class UserModel(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str
    phone: str | None = None


class LoginModel(BaseModel):
    email: EmailStr
    password: str

class OrganisationModel(BaseModel):
    name: str
    description: str | None = None
