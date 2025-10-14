from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_database
from app.db.models import User, Role
from app.schemas.user_dto import UserDTO, UserCreateDTO, UserUpdateDTO
from typing import List
from app.services.user_service import (
    create_user_service,
    list_users_service,
    get_user_service,
    update_user_service,
    delete_user_service
)

router = APIRouter(prefix="/adsweb/api/v1/users", tags=["Users"])

@router.post("/", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreateDTO, db: AsyncSession = Depends(get_database)):
    return await create_user_service(db, payload)

@router.get("/", response_model=List[UserDTO])
async def list_users(db: AsyncSession = Depends(get_database)):
    return await list_users_service(db)

@router.get("/{user_id}", response_model=UserDTO)
async def get_user(user_id: int, db: AsyncSession = Depends(get_database)):
    return await get_user_service(db, user_id)

@router.put("/{user_id}", response_model=UserDTO)
async def update_user(user_id: int, payload: UserUpdateDTO, db: AsyncSession = Depends(get_database)):
    return await update_user_service(db, user_id, payload)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_database)):
    await delete_user_service(db, user_id)

@router.put("/{user_id}/roles", response_model=dict)
async def update_user_roles(user_id: int, roles: list[str], db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Get all valid roles in one query
    role_objs = (await db.execute(select(Role).where(Role.name.in_(roles)))).scalars().all()
    if not role_objs:
        raise HTTPException(status_code=400, detail="No valid roles provided")
    user.roles = role_objs
    await db.commit()
    await db.refresh(user)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "roles": [r.name for r in user.roles]
    }
