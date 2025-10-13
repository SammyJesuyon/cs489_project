from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_database
from app.db.models import Patient, Address
from app.schemas.patient_dto import PatientDTO
from app.schemas.address_dto import AddressDTO
from typing import Optional, List

router = APIRouter(prefix="/adsweb/api/v1", tags=["Patients"])

@router.post("/patients", response_model=PatientDTO, status_code=status.HTTP_201_CREATED)
async def create_patient(payload: PatientDTO, db: AsyncSession = Depends(get_database)):
    patient = Patient(**payload.model_dump())
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    return PatientDTO.model_validate(patient)

@router.put("/patient/{patient_id}", response_model=PatientDTO)
async def update_patient(patient_id: int, payload: PatientDTO, db: AsyncSession = Depends(get_database)):
    patient = await db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(patient, k, v)
    await db.commit()
    await db.refresh(patient)
    return PatientDTO.model_validate(patient)

@router.delete("/patient/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(patient_id: int, db: AsyncSession = Depends(get_database)):
    patient = await db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    await db.delete(patient)
    await db.commit()

@router.get("/patient/search/{searchString}", response_model=List[PatientDTO])
async def search_patient(searchString: str, db: AsyncSession = Depends(get_database)):
    like = f"%{searchString.strip()}%"
    stmt = select(Patient).where(
        Patient.first_name.ilike(like) |
        Patient.last_name.ilike(like) |
        Patient.patient_no.ilike(like) |
        Patient.email.ilike(like) |
        Patient.phone.ilike(like)
    )
    patients = (await db.execute(stmt)).scalars().all()
    return [PatientDTO.model_validate(p) for p in patients]

@router.get("/patients", response_model=List[PatientDTO])
async def list_patients(db: AsyncSession = Depends(get_database)):
    stmt = select(Patient)
    patients = (await db.execute(stmt)).scalars().all()
    return [PatientDTO.model_validate(p) for p in patients]

@router.get("/addresses", response_model=List[AddressDTO])
async def list_addresses(db: AsyncSession = Depends(get_database)):
    stmt = select(Address)
    addresses = (await db.execute(stmt)).scalars().all()
    return [AddressDTO.model_validate(a) for a in addresses]
