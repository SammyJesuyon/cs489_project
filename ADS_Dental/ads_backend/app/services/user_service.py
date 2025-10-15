from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.db.models import User, Role, Dentist
from app.schemas.user_dto import UserDTO, UserCreateDTO, UserUpdateDTO, RoleEnum
from app.core.security import hash_password
from typing import List

def user_to_dto(user: User) -> UserDTO:
    # Map the first role (if any) to the DTO
    role_name = user.roles[0].name if user.roles else None
    role_enum = RoleEnum(role_name) if role_name in RoleEnum.__members__ else None
    return UserDTO(
        id=user.id,
        email=user.email,
        username=user.username,
        role=role_enum
    )

async def create_user_service(db: AsyncSession, payload: UserCreateDTO) -> UserDTO:
    existing = await db.execute(select(User).where(User.email == str(payload.email) or User.username == payload.username))
    user_exists = existing.scalar_one_or_none()
    if user_exists:
        raise HTTPException(status_code=400, detail="User already registered")
    user = User(
        email=payload.email,
        username=payload.username,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    # Assign role
    role = await db.execute(select(Role).where(Role.name == payload.role.value))
    role_obj = role.scalar_one_or_none()
    if role_obj:
        user.roles.append(role_obj)
        await db.commit()
        await db.refresh(user)
    return user_to_dto(user)

async def list_users_service(db: AsyncSession) -> List[UserDTO]:
    stmt = select(User)
    users = (await db.execute(stmt)).scalars().all()
    return [user_to_dto(u) for u in users]

async def get_user_service(db: AsyncSession, user_id: int) -> UserDTO:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_to_dto(user)

async def update_user_service(db: AsyncSession, user_id: int, payload: UserUpdateDTO) -> UserDTO:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = payload.model_dump(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        update_data["password_hash"] = hash_password(update_data.pop("password"))
    for k, v in update_data.items():
        setattr(user, k, v)
    # Update role if provided
    if "role" in update_data and update_data["role"]:
        role = await db.execute(select(Role).where(Role.name == update_data["role"].value))
        role_obj = role.scalar_one_or_none()
        if role_obj:
            user.roles = [role_obj]
    await db.commit()
    await db.refresh(user)
    return user_to_dto(user)

async def delete_user_service(db: AsyncSession, user_id: int):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()

async def register_dentist_service(db: AsyncSession, payload: UserCreateDTO):
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
    return dentist
