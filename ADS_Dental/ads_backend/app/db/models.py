from datetime import date, time
from sqlalchemy import (
    Column, Integer, String, Boolean, Date, Time, ForeignKey, Table, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Many-to-many: users ↔ roles
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    street = Column(String(120), nullable=False)
    city = Column(String(60), nullable=False)
    state = Column(String(30), nullable=False)
    zip_code = Column(String(15), nullable=False)

    patients = relationship("Patient", back_populates="address")

    def __repr__(self):
        return f"<Address(id={self.id}, street='{self.street}', city='{self.city}', state='{self.state}', zip_code='{self.zip_code}')>"

class Surgery(Base):
    __tablename__ = "surgeries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    surgery_no = Column(String(10), nullable=False, unique=True)
    name = Column(String(120), nullable=False)
    phone = Column(String(30))
    address_id = Column(Integer, ForeignKey("addresses.id", ondelete="RESTRICT"), unique=True)
    address = relationship("Address")

    dentists = relationship("Dentist", back_populates="surgery")
    appointments = relationship("Appointment", back_populates="surgery")

    def __repr__(self):
        return f"<Surgery(id={self.id}, surgery_no='{self.surgery_no}', name='{self.name}')>"

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_no = Column(String(20), nullable=False, unique=True)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    phone = Column(String(30))
    email = Column(String(120))
    address_id = Column(Integer, ForeignKey("addresses.id", ondelete="SET NULL"))
    address = relationship("Address", back_populates="patients")

    appointments = relationship("Appointment", back_populates="patient")

    def __repr__(self):
        return f"<Patient(id={self.id}, patient_no='{self.patient_no}', first_name='{self.first_name}', last_name='{self.last_name}')>"

class Dentist(Base):
    __tablename__ = "dentists"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    phone = Column(String(30))
    email = Column(String(120))
    specialization = Column(String(80))
    surgery_id = Column(Integer, ForeignKey("surgeries.id", ondelete="SET NULL"))
    surgery = relationship("Surgery", back_populates="dentists")

    appointments = relationship("Appointment", back_populates="dentist")

    def __repr__(self):
        return f"<Dentist(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}')>"

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    appt_date = Column(Date, nullable=False)
    appt_time = Column(Time, nullable=False)
    status = Column(String(20), default="booked")

    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    dentist_id = Column(Integer, ForeignKey("dentists.id", ondelete="CASCADE"), nullable=False)
    surgery_id = Column(Integer, ForeignKey("surgeries.id", ondelete="CASCADE"), nullable=False)

    patient = relationship("Patient", back_populates="appointments")
    dentist = relationship("Dentist", back_populates="appointments")
    surgery = relationship("Surgery", back_populates="appointments")

    __table_args__ = (
        UniqueConstraint("dentist_id", "appt_date", "appt_time", name="uq_dentist_slot"),
    )

    def __repr__(self):
        return f"<Appointment(id={self.id}, appt_date={self.appt_date}, appt_time={self.appt_time}, status='{self.status}')>"

from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(60), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    enabled = Column(Boolean, default=True)
    created_at = Column(Date, server_default=func.current_date(), nullable=False)
    updated_at = Column(Date, server_default=func.current_date(), onupdate=func.current_date(), nullable=False)
    roles = relationship("Role", secondary=user_roles, back_populates="users")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', enabled={self.enabled})>"

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False, unique=True)
    created_at = Column(Date, server_default=func.current_date(), nullable=False)
    updated_at = Column(Date, server_default=func.current_date(), onupdate=func.current_date(), nullable=False)
    users = relationship("User", secondary=user_roles, back_populates="roles")

    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"