from pydantic import BaseModel
from typing import Optional, List


class PatientNameOnlyDTO(BaseModel):
    id: int
    patient_no: str
    first_name: str
    last_name: str

class AddressDTO(BaseModel):
    id: int
    street: str
    city: str
    state: str
    zip_code: str
    patients: List[PatientNameOnlyDTO] = []

class AddressCreateDTO(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str