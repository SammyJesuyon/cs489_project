from pydantic import BaseModel
from datetime import datetime, time
from enum import Enum

from app.schemas.dentist_dto import DentistResponseDTO
from app.schemas.patient_dto import PatientDTO
from app.schemas.surgery_dto import SurgeryDTO


class AppointmentStatus(str, Enum):
    BOOKED = "BOOKED"
    CANCELED = "CANCELED"
    COMPLETED = "COMPLETED"

class AppointmentCreateDTO(BaseModel):
    dentist_id: int
    surgery_id: int
    appointment_date: datetime

class AppointmentDTO(BaseModel):
    id: int
    appointment_date: datetime
    appointment_time: time
    status: AppointmentStatus
    patient: PatientDTO
    dentist: DentistResponseDTO
    surgery: SurgeryDTO

    class Config:
        from_attributes = True