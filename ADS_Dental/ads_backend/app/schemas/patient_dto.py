from pydantic import BaseModel, EmailStr
from typing import Optional
from app.schemas.address_dto import AddressCreateDTO, AddressDTO

class PatientCreateDTO(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: EmailStr
    password: str
    address: Optional[AddressCreateDTO] = None

class PatientDTO(BaseModel):
    id: int
    patient_no: str
    first_name: str
    last_name: str
    phone: Optional[str]
    email: str
    address: Optional[AddressDTO] = None

    class Config:
        from_attributes = True