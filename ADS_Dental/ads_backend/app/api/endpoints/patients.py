from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_database
from app.schemas.patient_dto import PatientDTO, PatientCreateDTO
from app.schemas.address_dto import AddressDTO
from typing import List
from app.services.patient_service import (
    update_patient_service,
    delete_patient_service,
    search_patient_service,
    list_patients_service,
    list_addresses_service,
    register_patient_service, get_patient_by_id_service
)
from app.api.dependencies.rbac import require_role

router = APIRouter(prefix="/adsweb/api/v1", tags=["Patients"])

@router.post("/patients", response_model=PatientDTO, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role(["PATIENT", "ADMIN"]))])
async def register_patient(payload: PatientCreateDTO, db: AsyncSession = Depends(get_database)):
    return await register_patient_service(db, payload)

@router.put("/patient/{patient_id}", response_model=PatientDTO, dependencies=[Depends(require_role(["ADMIN", "PATIENT"]))])
async def update_patient(patient_id: int, payload: PatientDTO, db: AsyncSession = Depends(get_database)):
    return await update_patient_service(db, patient_id, payload)

@router.delete("/patient/{patient_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role(["ADMIN"]))])
async def delete_patient(patient_id: int, db: AsyncSession = Depends(get_database)):
    await delete_patient_service(db, patient_id)

@router.get("/patient/search/{searchString}", response_model=List[PatientDTO], dependencies=[Depends(require_role(["ADMIN", "DENTIST"]))])
async def search_patient(searchString: str, db: AsyncSession = Depends(get_database)):
    return await search_patient_service(db, searchString)

@router.get("/patients", response_model=List[PatientDTO], dependencies=[Depends(require_role(["ADMIN", "DENTIST"]))])
async def list_patients(db: AsyncSession = Depends(get_database)):
    return await list_patients_service(db)

@router.get("/patient/{patient_id}", response_model=PatientDTO, dependencies=[Depends(require_role(["ADMIN", "DENTIST"]))])
async def get_patient(patient_id: int, db: AsyncSession = Depends(get_database)):
    return await get_patient_by_id_service(db, patient_id)

@router.get("/addresses", response_model=List[AddressDTO], dependencies=[Depends(require_role(["ADMIN"]))])
async def list_addresses(db: AsyncSession = Depends(get_database)):
    return await list_addresses_service(db)
