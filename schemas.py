
from pydantic import BaseModel, EmailStr, Field

class UserModel(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str
    phone: str | None = None

class OrganisationModel(BaseModel):
    name: str = Field(...)
    description: str | None
    