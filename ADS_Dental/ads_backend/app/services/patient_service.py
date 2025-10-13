from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Patient
from fastapi import HTTPException

async def list_patients_service(db: AsyncSession):
    result = await db.execute(select(Patient))
    return result.scalars().all()

async def get_patient_by_id_service(db: AsyncSession, patient_id: int):
    patient = await db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient