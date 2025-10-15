from pydantic import BaseModel
from typing import List, Optional

from app.schemas.address_dto import AddressDTO
from app.schemas.dentist_dto import DentistResponseDTO


class SurgeryDTO(BaseModel):
    id: int
    surgery_no: Optional[str]
    name: Optional[str]
    phone: Optional[str]
    address: Optional[AddressDTO]
    dentists: List[DentistResponseDTO] = []

    class Config:
        from_attributes = True
