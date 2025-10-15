from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_database
from app.schemas.appointment_dto import AppointmentCreateDTO, AppointmentDTO
from app.services.appointment_service import create_appointment_service, list_appointments_service
from app.core.security import require_patient, get_current_user
from app.db.models import Patient, Appointment, Dentist

router = APIRouter(prefix="/adsweb/api/v1/appointments", tags=["Appointments"])

@router.post("/", response_model=AppointmentDTO)
async def create_appointment(
    payload: AppointmentCreateDTO,
    current_user = Depends(require_patient),
    db: AsyncSession = Depends(get_database)
):
    result = await db.execute(select(Patient).where(Patient.user_id == int(current_user.id)))
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")

    return await create_appointment_service(db, payload, patient.id)

@router.get("/", response_model=List[AppointmentDTO])
async def list_appointments(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_database)
):
    return await list_appointments_service(db, current_user)