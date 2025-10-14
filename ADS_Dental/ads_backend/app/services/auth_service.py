from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.db.models import User, Patient, Address, Role
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.patient_dto import PatientCreateDTO
from app.schemas.auth_dto import TokenDTO
from passlib.exc import UnknownHashError

async def register_patient_service(db: AsyncSession, payload: PatientCreateDTO):
    # Fix SQLAlchemy where clause type issue
    existing = await db.execute(select(User).where(User.email == str(payload.email)))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Convert EmailStr to str before splitting
    username = str(payload.email).split("@")[0]

    user = User(
        email=payload.email,
        username=username,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Assign PATIENT role
    role_patient = await db.execute(select(Role).where(Role.name == "PATIENT"))
    role_obj = role_patient.scalar_one_or_none()
    if role_obj:
        user.roles.append(role_obj)
        await db.commit()
        await db.refresh(user)

    address = None
    if payload.address:
        # Use model_dump instead of dict
        address = Address(**payload.address.model_dump())
        db.add(address)
        await db.commit()
        await db.refresh(address)

    patient = Patient(
        user_id=user.id,
        first_name=payload.first_name,
        last_name=payload.last_name,
        phone=payload.phone,
        address_id=address.id if address else None
    )
    db.add(patient)
    await db.commit()
    await db.refresh(patient)

    return patient

async def login_service(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(User).where(User.email == str(email)))
    user = result.scalar_one_or_none()
    try:
        valid = user and verify_password(password, user.password_hash)
    except UnknownHashError:
        valid = False
    if not valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    role_name = user.roles[0].name if user.roles else None
    token = create_access_token({"sub": user.email, "role": role_name})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "roles": [r.name for r in user.roles]
        }
    }
