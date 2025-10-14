from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    DENTIST = "DENTIST"
    PATIENT = "PATIENT"

class UserDTO(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: Optional[RoleEnum]

    class Config:
        from_attributes = True

class UserCreateDTO(BaseModel):
    email: EmailStr
    username: str
    password: str
    role: RoleEnum

class UserUpdateDTO(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    password: str | None = None
    role: RoleEnum | None = None
