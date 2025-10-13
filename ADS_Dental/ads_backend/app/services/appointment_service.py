from app.db.models import Appointment
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

async def create_appointment_service(db: AsyncSession, payload, patient_id: int):
    try:
        appointment = Appointment(
            appointment_date=payload.appointment_date,
            dentist_id=payload.dentist_id,
            surgery_id=payload.surgery_id,
            patient_id=patient_id
        )
        db.add(appointment)
        await db.commit()
        await db.refresh(appointment)
        return appointment
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")