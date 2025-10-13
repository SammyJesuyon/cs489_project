from pydantic import BaseModel, EmailStr
from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    DENTIST = "DENTIST"
    PATIENT = "PATIENT"

class UserDTO(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: RoleEnum

    class Config:
        from_attributes = True