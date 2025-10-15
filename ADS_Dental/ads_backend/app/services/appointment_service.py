from app.db.models import Appointment
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

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

async def get_appointment_by_id_service(db: AsyncSession, appointment_id: int):
    appointment = await db.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

async def delete_appointment_service(db: AsyncSession, appointment_id: int):
    appointment = await db.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    await db.delete(appointment)
    await db.commit()

async def list_appointments_service(db: AsyncSession, current_user):
    # Extract all role names as lowercase strings
    role_names = [r.name.lower() for r in current_user.roles]

    if "admin" in role_names:
        result = await db.execute(select(Appointment))
        return result.scalars().all()

    elif "dentist" in role_names:
        if not hasattr(current_user, "dentist_id") or current_user.dentist_id is None:
            raise HTTPException(status_code=404, detail="Dentist profile not found")
        result = await db.execute(
            select(Appointment).where(Appointment.dentist_id == current_user.dentist_id)
        )
        return result.scalars().all()

    elif "patient" in role_names:
        if not hasattr(current_user, "patient_id") or current_user.patient_id is None:
            raise HTTPException(status_code=404, detail="Patient profile not found")
        result = await db.execute(
            select(Appointment).where(Appointment.patient_id == current_user.patient_id)
        )
        return result.scalars().all()

    else:
        raise HTTPException(status_code=403, detail="Not authorized to view appointments")
