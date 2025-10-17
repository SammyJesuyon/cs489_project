from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.rbac import require_role
from app.db.session import get_database
from app.schemas.surgery_dto import SurgeryDTO
from app.services.surgery_service import list_surgeries_service

router = APIRouter(prefix="/adsweb/api/v1", tags=["Surgeries"])

@router.get("/surgeries", response_model=SurgeryDTO, dependencies=[Depends(require_role(["PATIENT", "ADMIN"]))])
async def list_surgeries(db : AsyncSession = Depends(get_database)):
    return await list_surgeries_service(db)