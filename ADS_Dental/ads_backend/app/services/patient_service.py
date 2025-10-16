from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import User, Patient, Address, Role
from app.core.security import hash_password
from app.schemas.patient_dto import PatientDTO, PatientCreateDTO
from fastapi import HTTPException
import random
from datetime import datetime
from sqlalchemy.orm import selectinload

async def list_patients_service(db: AsyncSession):
    result = await db.execute(
        select(Patient)
        .options(selectinload(Patient.address))
        .order_by(Patient.last_name.asc())
    )
    patients = result.scalars().all()
    return patients

async def get_patient_by_id_service(db: AsyncSession, patient_id: int):
    patient = await db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

async def create_patient_service(db: AsyncSession, payload: PatientDTO) -> PatientDTO:
    patient = Patient(**payload.model_dump())
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    return PatientDTO.model_validate(patient)

async def update_patient_service(db: AsyncSession, patient_id: int, payload: PatientDTO) -> PatientDTO:
    patient = await db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(patient, k, v)
    await db.commit()
    await db.refresh(patient)
    return PatientDTO.model_validate(patient)

async def delete_patient_service(db: AsyncSession, patient_id: int):
    patient = await db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    await db.delete(patient)
    await db.commit()

async def search_patient_service(db: AsyncSession, searchString: str):
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

async def list_addresses_service(db: AsyncSession):
    result = await db.execute(
        select(Address)
        .options(selectinload(Address.patients))
        .order_by(Address.city.asc())
    )
    addresses = result.scalars().all()
    return addresses

async def register_patient_service(db: AsyncSession, payload: PatientCreateDTO):
    from sqlalchemy.exc import SQLAlchemyError
    patient_no = f"P{datetime.now().strftime('%Y%m%d')}{random.randint(100,999)}"
    try:
        # Save Patient first
        address = None
        if payload.address:
            address = Address(**payload.address.model_dump())
            db.add(address)
            await db.flush()
            await db.refresh(address)
        patient = Patient(
            patient_no=patient_no,
            first_name=payload.first_name,
            last_name=payload.last_name,
            phone=payload.phone,
            email=payload.email,
            address_id=address.id if address else None
        )
        db.add(patient)
        await db.flush()
        await db.refresh(patient)
        # Save User and link to Patient only if Patient was added
        username = str(payload.email).split("@")[0]
        user = User(
            email=payload.email,
            username=username,
            password_hash=hash_password(payload.password),
        )
        db.add(user)
        await db.flush()
        await db.refresh(user)
        # Assign PATIENT role
        role_patient = await db.execute(select(Role).where(Role.name == "PATIENT"))
        role_obj = role_patient.scalar_one_or_none()
        if role_obj:
            user.roles.append(role_obj)
            await db.flush()
            await db.refresh(user)
        # Link patient to user
        patient.user_id = user.id
        await db.flush()
        await db.refresh(patient)
        await db.commit()
        return patient
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")