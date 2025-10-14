from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import User, Dentist, Role
from app.core.security import hash_password
from app.schemas.dentist_dto import DentistCreateDTO, DentistResponseDTO
from fastapi import HTTPException

async def register_dentist_service(db: AsyncSession, payload: DentistCreateDTO):
    existing = await db.execute(select(User).where(User.email == str(payload.email)))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    username = str(payload.email).split("@")[0]
    user = User(
        email=payload.email,
        username=username,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    # Assign DENTIST role
    role_dentist = await db.execute(select(Role).where(Role.name == "DENTIST"))
    role_obj = role_dentist.scalar_one_or_none()
    if role_obj:
        user.roles.append(role_obj)
        await db.commit()
        await db.refresh(user)
    dentist = Dentist(
        user_id=user.id,
        first_name=payload.first_name,
        last_name=payload.last_name,
        phone=payload.phone,
        email=payload.email,
        specialization=payload.specialization,
        surgery_id=payload.surgery_id
    )
    db.add(dentist)
    await db.commit()
    await db.refresh(dentist)
