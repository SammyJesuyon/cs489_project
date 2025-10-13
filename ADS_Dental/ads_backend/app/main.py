# from fastapi import FastAPI, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy import select, or_, asc
# from sqlalchemy.orm import joinedload
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
# from app.db.models import Base, Patient, Address
# from app.schemas.patient_dto import PatientDTO, CreatePatientDTO, AddressSlimDTO
# from app.schemas.address_dto import AddressDTO
# from app.exceptions.http_exceptions import NotFoundException, ConflictException
# from typing import AsyncGenerator, Optional
#
# # 🧩 MySQL async connection string
# DB_URL = "mysql+aiomysql://root:password@localhost:3306/ADSDentalSurgeryDB"
#
# # ⚙️ Async engine and session
# engine = create_async_engine(
#     DB_URL,
#     pool_pre_ping=True, # Verify connections before use
#     pool_recycle=300, # Recycle connections every 5 minutes
# )
# AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False
# )
#
# async def get_database() -> AsyncGenerator[AsyncSession, None]:
#     """
#     FastAPI dependency that yields an AsyncSession.
#     The async context manager ensures the session is closed automatically.
#     """
#     async with AsyncSessionLocal() as session:
#         try:
#             yield session
#         except Exception as e:
#             print(f"Error: {e}")
#             await session.rollback()
#             raise
#
# # async def close_engine() -> None:
# #     """
# #     Dispose the engine and its connection pool.
# #     Call this on application shutdown to ensure all DB connections are released.
# #     """
# #     try:
# #         await engine.dispose()
# #         print("Engine disposed.")
# #     except Exception as e:
# #         print(f"Error: {e}")
#
# # 🧠 Create database tables
# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
# # Helper function to create or get address
# async def create_or_get_address(db: AsyncSession, address_data: Optional[dict]) -> Optional[Address]:
#     if not address_data:
#         return None
#     # Try to find existing address matching all fields
#     stmt = select(Address).filter_by(**address_data)
#     existing_address = (await db.execute(stmt)).scalars().first()
#     if existing_address:
#         return existing_address
#     # Create new address
#     new_address = Address(**address_data)
#     db.add(new_address)
#     await db.flush()  # flush to assign id
#     return new_address
#
# # 🚀 FastAPI app setup
# app = FastAPI(title="ADS Dental Surgeries API", version="2.0")
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], allow_credentials=True,
#     allow_methods=["*"], allow_headers=["*"]
# )
#
# API_PREFIX = "/adsweb/api/v1"
#
# @app.on_event("startup")
# async def startup_event():
#     await init_models()
#
# @app.get("/")
# async def root():
#     return {"message": "ADS Dental Surgeries API (MySQL) is running 🎯"}
#
# # 1️⃣ GET all patients
# @app.get(f"{API_PREFIX}/patients", response_model=list[PatientDTO])
# async def list_patients(db: AsyncSession = Depends(get_database)):
#     stmt = select(Patient).options(joinedload(Patient.address)).order_by(asc(Patient.last_name))
#     patients = (await db.execute(stmt)).scalars().all()
#     result = []
#     for p in patients:
#         dto = PatientDTO.from_orm(p)
#         dto.primaryAddress = AddressSlimDTO.from_orm(p.address) if p.address else None
#         result.append(dto)
#     return result
#
# # 2️⃣ GET patient by ID
# @app.get(f"{API_PREFIX}/patients/{{patient_id}}", response_model=PatientDTO)
# async def get_patient(patient_id: int, db: AsyncSession = Depends(get_database)):
#     patient = await db.get(Patient, patient_id, options=[joinedload(Patient.address)])
#     if not patient:
#         raise NotFoundException("Patient", patient_id)
#     dto = PatientDTO.from_orm(patient)
#     dto.primaryAddress = AddressSlimDTO.from_orm(patient.address) if patient.address else None
#     return dto
#
# # 3️⃣ POST create patient
# @app.post(f"{API_PREFIX}/patients", response_model=PatientDTO, status_code=201)
# async def create_patient(payload: CreatePatientDTO, db: AsyncSession = Depends(get_database)):
#     exists = (await db.execute(select(Patient).where(Patient.patient_no == payload.patient_no))).scalar_one_or_none()
#     if exists:
#         raise ConflictException("Patient number already exists.")
#     address_data = payload.address.dict() if payload.address else None
#     address = await create_or_get_address(db, address_data)
#     patient_data = payload.model_dump(exclude={"address"})
#     patient = Patient(**patient_data)
#     if address:
#         patient.address = address
#     db.add(patient)
#     await db.commit()
#     await db.refresh(patient)
#     dto = PatientDTO.model_validate(patient)
#     dto.primaryAddress = AddressSlimDTO.model_validate(patient.address) if patient.address else None
#     return dto
#
# # 4️⃣ PUT update patient
# @app.put(f"{API_PREFIX}/patient/{{patient_id}}", response_model=PatientDTO)
# async def update_patient(patient_id: int, payload: CreatePatientDTO, db: AsyncSession = Depends(get_database)):
#     patient = await db.get(Patient, patient_id, options=[joinedload(Patient.address)])
#     if not patient:
#         raise NotFoundException("Patient", patient_id)
#     address_data = payload.address.dict() if payload.address else None
#     if address_data:
#         address = await create_or_get_address(db, address_data)
#         patient.address = address
#     else:
#         patient.address = None
#     for k, v in payload.dict(exclude={"address"}).items():
#         setattr(patient, k, v)
#     await db.commit()
#     await db.refresh(patient)
#     dto = PatientDTO.from_orm(patient)
#     dto.primaryAddress = AddressSlimDTO.from_orm(patient.address) if patient.address else None
#     return dto
#
# # 5️⃣ DELETE patient
# @app.delete(f"{API_PREFIX}/patient/{{patient_id}}", status_code=204)
# async def delete_patient(patient_id: int, db: AsyncSession = Depends(get_database)):
#     patient = await db.get(Patient, patient_id)
#     if not patient:
#         raise NotFoundException("Patient", patient_id)
#     await db.delete(patient)
#     await db.commit()
#
# # 6️⃣ SEARCH patient
# @app.get(f"{API_PREFIX}/patient/search/{{searchString}}", response_model=list[PatientDTO])
# async def search_patient(searchString: str, db: AsyncSession = Depends(get_database)):
#     like = f"%{searchString.strip()}%"
#     stmt = (
#         select(Patient)
#         .options(joinedload(Patient.address))
#         .where(or_(
#             Patient.first_name.ilike(like),
#             Patient.last_name.ilike(like),
#             Patient.patient_no.ilike(like),
#             Patient.email.ilike(like),
#             Patient.phone.ilike(like),
#         ))
#         .order_by(asc(Patient.last_name))
#     )
#     patients = (await db.execute(stmt)).scalars().all()
#     result = []
#     for p in patients:
#         dto = PatientDTO.from_orm(p)
#         dto.primaryAddress = AddressSlimDTO.from_orm(p.address) if p.address else None
#         result.append(dto)
#     return result
#
# # 7️⃣ GET addresses with patients
# @app.get(f"{API_PREFIX}/addresses", response_model=list[AddressDTO])
# async def list_addresses(db: AsyncSession = Depends(get_database)):
#     stmt = select(Address).options(joinedload(Address.patients)).order_by(asc(Address.city))
#     addresses = (await db.execute(stmt)).scalars().all()
#     return [AddressDTO.from_orm(a) for a in addresses]

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.endpoints import patients, auth, appointments


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Place your async startup code here
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "ADS Dental Surgeries API is running 🚀"}

app.include_router(patients.router)
app.include_router(auth.router)
app.include_router(appointments.router)