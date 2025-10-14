from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_database
from app.schemas.dentist_dto import DentistCreateDTO, DentistResponseDTO
from app.db.models import Dentist
from app.services.dentist_service import register_dentist_service

router = APIRouter(prefix="/adsweb/api/v1", tags=["Dentists"])

@router.post("/dentists/register", response_model=DentistResponseDTO, status_code=status.HTTP_201_CREATED)
async def register_dentist(payload: DentistCreateDTO, db: AsyncSession = Depends(get_database)):
    return await register_dentist_service(db, payload)
