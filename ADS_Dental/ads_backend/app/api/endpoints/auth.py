from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_database
from app.schemas.auth_dto import LoginDTO, TokenDTO
from app.services.auth_service import login_service

router = APIRouter(prefix="/api/v1", tags=["Auth"])

@router.post("/login")
async def login(payload: LoginDTO, db: AsyncSession = Depends(get_database)):
    return await login_service(db, str(payload.email), payload.password)
