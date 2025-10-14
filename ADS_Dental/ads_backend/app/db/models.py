# Refactored models.py to match the UML diagram (ads_uml.png)
# app/db/models.py
from enum import Enum as PyEnum
from sqlalchemy import (
    Column, Integer, String, Boolean, Date, Time, DateTime,
    ForeignKey, Table, UniqueConstraint, Enum, func
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# --- Many-to-many: User ↔ Role
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)

# --- Address ---
class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    street = Column(String(120), nullable=False)
    city = Column(String(60), nullable=False)
    state = Column(String(30), nullable=False)
    zip_code = Column(String(15), nullable=False)

    patients = relationship("Patient", back_populates="address", lazy="selectin")
    surgeries = relationship("Surgery", back_populates="address", lazy="selectin")

    def __repr__(self):
        return f"<Address(id={self.id}, street='{self.street}', city='{self.city}')>"


# --- Surgery ---
class Surgery(Base):
    __tablename__ = "surgeries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    surgery_no = Column(String(10), nullable=False, unique=True)
    name = Column(String(120), nullable=False)
    phone = Column(String(30))
    address_id = Column(Integer, ForeignKey("addresses.id", ondelete="RESTRICT"), unique=True)

    address = relationship("Address", back_populates="surgeries", lazy="selectin")
    dentists = relationship("Dentist", back_populates="surgery", lazy="selectin")
    appointments = relationship("Appointment", back_populates="surgery", lazy="selectin")

    def __repr__(self):
        return f"<Surgery(id={self.id}, surgery_no='{self.surgery_no}', name='{self.name}')>"


# --- Patient ---
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    patient_no = Column(String(20), nullable=False, unique=True)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    phone = Column(String(30))
    email = Column(String(120))
    address_id = Column(Integer, ForeignKey("addresses.id", ondelete="SET NULL"))

    address = relationship("Address", back_populates="patients", lazy="selectin")
    appointments = relationship("Appointment", back_populates="patient", lazy="selectin")
    user = relationship("User", back_populates="patient", lazy="selectin")

    def __repr__(self):
        return f"<Patient(id={self.id}, patient_no='{self.patient_no}', name='{self.first_name} {self.last_name}')>"


# --- Dentist ---
class Dentist(Base):
    __tablename__ = "dentists"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    phone = Column(String(30))
    email = Column(String(120))
    specialization = Column(String(80))
    surgery_id = Column(Integer, ForeignKey("surgeries.id", ondelete="SET NULL"))

    surgery = relationship("Surgery", back_populates="dentists", lazy="selectin")
    appointments = relationship("Appointment", back_populates="dentist", lazy="selectin")
    user = relationship("User", back_populates="dentist", lazy="selectin")

    def __repr__(self):
        return f"<Dentist(id={self.id}, name='{self.first_name} {self.last_name}')>"


# --- Appointment ---
class AppointmentStatus(str, PyEnum):
    BOOKED = "BOOKED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.BOOKED, nullable=False)

    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    dentist_id = Column(Integer, ForeignKey("dentists.id", ondelete="CASCADE"), nullable=False)
    surgery_id = Column(Integer, ForeignKey("surgeries.id", ondelete="CASCADE"), nullable=False)

    patient = relationship("Patient", back_populates="appointments", lazy="selectin")
    dentist = relationship("Dentist", back_populates="appointments", lazy="selectin")
    surgery = relationship("Surgery", back_populates="appointments", lazy="selectin")

    __table_args__ = (
        UniqueConstraint("dentist_id", "appointment_date", "appointment_time", name="uq_dentist_slot"),
    )

    def __repr__(self):
        return f"<Appointment(id={self.id}, date={self.appointment_date}, time={self.appointment_time}, status={self.status})>"


# --- Security Models ---
class RoleEnum(str, PyEnum):
    ADMIN = "ADMIN"
    DENTIST = "DENTIST"
    PATIENT = "PATIENT"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(60), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    roles = relationship("Role", secondary=user_roles, back_populates="users", lazy="selectin")
    patient = relationship("Patient", back_populates="user", lazy="selectin")
    dentist = relationship("Dentist", back_populates="user", lazy="selectin")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', enabled={self.enabled})>"


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    users = relationship("User", secondary=user_roles, back_populates="roles", lazy="selectin")

    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"

__all__ = [
    "Base", "Address", "Surgery", "Patient", "Dentist", "Appointment", "AppointmentStatus",
    "User", "Role", "RoleEnum", "user_roles",
]