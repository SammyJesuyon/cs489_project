from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_database
from app.schemas.patient_dto import PatientCreateDTO, PatientDTO
from app.schemas.auth_dto import LoginDTO, TokenDTO
from app.services.auth_service import register_patient_service, login_service

router = APIRouter(prefix="/api/v1", tags=["Auth"])

@router.post("/register", response_model=PatientDTO)
async def register_patient(payload: PatientCreateDTO, db: AsyncSession = Depends(get_database)):
    return await register_patient_service(db, payload)

@router.post("/login", response_model=TokenDTO)
async def login(payload: LoginDTO, db: AsyncSession = Depends(get_database)):
# Convert EmailStr to str before passing
    return await login_service(db, str(payload.email), payload.password)
