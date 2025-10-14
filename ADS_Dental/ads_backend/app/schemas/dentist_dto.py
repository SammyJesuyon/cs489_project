from pydantic import BaseModel

class DentistCreateDTO(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    phone: str
    specialization: str
    surgery_id: int

class DentistResponseDTO(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: str
    email: str
    specialization: str
    surgery_id: int
    user_id: int

    class Config:
        orm_mode = True
