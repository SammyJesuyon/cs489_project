from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class AppointmentStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"

class AppointmentCreateDTO(BaseModel):
    dentist_id: int
    surgery_id: int
    appointment_date: datetime

class AppointmentDTO(BaseModel):
    id: int
    appointment_date: datetime
    status: AppointmentStatus

    class Config:
        from_attributes = True