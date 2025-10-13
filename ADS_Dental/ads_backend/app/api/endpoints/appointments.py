from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_database
from app.schemas.appointment_dto import AppointmentCreateDTO, AppointmentDTO
from app.services.appointment_service import create_appointment_service
from app.core.security import require_patient
from app.db.models import Patient

router = APIRouter(prefix="/api/v1/appointments", tags=["Appointments"])

@router.post("/", response_model=AppointmentDTO)
async def create_appointment(
    payload: AppointmentCreateDTO,
    current_user = Depends(require_patient),
    db: AsyncSession = Depends(get_database)
):
    # Fix SQLAlchemy where clause type issue
    result = await db.execute(select(Patient).where(Patient.user_id == int(current_user.id)))
    # Ensure Patient.user_id is a Column and current_user.id is an int
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")

    return await create_appointment_service(db, payload, patient.id)