from typing import Optional
from pydantic import BaseModel, EmailStr

from .address_dto import AddressCreateDTO
from .common import ORMBase

class AddressSlimDTO(ORMBase):
    id: int
    street: str
    city: str
    state: str
    zip_code: str

class PatientDTO(ORMBase):
    id: int
    patient_no: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    primaryAddress: Optional[AddressSlimDTO] = None

class CreatePatientDTO(BaseModel):
    patient_no: str
    first_name: str
    last_name: str
    phone: str
    email: EmailStr
    address: Optional[AddressCreateDTO] = None