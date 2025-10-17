# Completely rewritten to match the actual structure defined in models.py.
import os
from datetime import date, time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL
from app.db.models import Base, Address, Surgery, Dentist, Patient, Appointment, User, Role
from app.core.security import hash_password

# Set up the engine and session
engine = create_engine(DATABASE_URL, echo=False, future=True)
Session = sessionmaker(bind=engine, autoflush=False)

def bootstrap():
    # Drop all existing tables and recreate them
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = Session()

    # Insert sample addresses
    addr1 = Address(street="123 West Avenue", city="Phoenix", state="AZ", zip_code="85012")
    addr2 = Address(street="900 Johns Street", city="Cleveland", state="OH", zip_code="43098")
    addr3 = Address(street="45 Green Street", city="Dallas", state="TX", zip_code="75201")
    session.add_all([addr1, addr2, addr3])
    session.flush()  # Ensure addresses have primary keys

    # Insert sample surgeries (use valid fields: surgery_no, phone, address_id)
    surg1 = Surgery(surgery_no="S001", name="Bells Court Dental", phone="602-555-1234", address_id=addr1.id)
    surg2 = Surgery(surgery_no="S002", name="The Galleria Surgery", phone="216-555-5678", address_id=addr2.id)
    surg3 = Surgery(surgery_no="S003", name="Pearl Dental South", phone="214-555-9012", address_id=addr3.id)
    session.add_all([surg1, surg2, surg3])
    session.flush()

    # Insert sample roles
    role_admin = Role(name="ADMIN")
    role_dentist = Role(name="DENTIST")
    role_patient = Role(name="PATIENT")
    session.add_all([role_admin, role_dentist, role_patient])
    session.flush()

    # Insert sample users and assign roles
    user1 = User(username="admin", email="admin@ads.com", password_hash=hash_password("adminpass"), roles=[role_admin])
    user2 = User(username="tsmith", email="tsmith@ads.com", password_hash=hash_password("dentistpass"), roles=[role_dentist])
    user3 = User(username="hpearson", email="hpearson@ads.com", password_hash=hash_password("dentistpass"), roles=[role_dentist])
    user4 = User(username="rplevin", email="rplevin@ads.com", password_hash=hash_password("dentistpass"), roles=[role_dentist])
    user5 = User(username="gwhite", email="gwhite@mail.com", password_hash=hash_password("patientpass"), roles=[role_patient])
    user6 = User(username="jbell", email="jbell@mail.com", password_hash=hash_password("patientpass"), roles=[role_patient])
    user7 = User(username="ianm", email="ianm@mail.com", password_hash=hash_password("patientpass"), roles=[role_patient])
    user8 = User(username="jwalker", email="jwalker@mail.com", password_hash=hash_password("patientpass"), roles=[role_patient])
    session.add_all([user1, user2, user3, user4, user5, user6, user7, user8])
    session.flush()

    # Insert sample dentists with user_id
    d1 = Dentist(user_id=user2.id, first_name="Tony", last_name="Smith", specialization="General", phone="480-123-1111", email="tsmith@ads.com", surgery_id=surg1.id)
    d2 = Dentist(user_id=user3.id, first_name="Helen", last_name="Pearson", specialization="Orthodontics", phone="480-123-2222", email="hpearson@ads.com", surgery_id=surg2.id)
    d3 = Dentist(user_id=user4.id, first_name="Robin", last_name="Plevin", specialization="Pediatric", phone="480-123-3333", email="rplevin@ads.com", surgery_id=surg3.id)
    session.add_all([d1, d2, d3])
    session.flush()

    # Insert sample patients with user_id
    p1 = Patient(user_id=user5.id, patient_no="P001", first_name="Gillian", last_name="White", email="gwhite@mail.com", address_id=addr1.id)
    p2 = Patient(user_id=user6.id, patient_no="P002", first_name="Jill", last_name="Bell", email="jbell@mail.com", address_id=addr1.id)
    p3 = Patient(user_id=user7.id, patient_no="P003", first_name="Ian", last_name="MacKay", email="ianm@mail.com", address_id=addr2.id)
    p4 = Patient(user_id=user8.id, patient_no="P004", first_name="John", last_name="Walker", email="jwalker@mail.com", address_id=addr3.id)
    session.add_all([p1, p2, p3, p4])
    session.flush()

    # Insert sample appointments (include appointment_time, status as enum)
    appt1 = Appointment(appointment_date=date(2013,9,12), appointment_time=time(9,0), status="BOOKED", patient_id=p1.id, dentist_id=d1.id, surgery_id=surg1.id)
    appt2 = Appointment(appointment_date=date(2013,9,12), appointment_time=time(10,0), status="BOOKED", patient_id=p2.id, dentist_id=d1.id, surgery_id=surg1.id)
    appt3 = Appointment(appointment_date=date(2013,9,13), appointment_time=time(11,0), status="BOOKED", patient_id=p3.id, dentist_id=d2.id, surgery_id=surg2.id)
    appt4 = Appointment(appointment_date=date(2013,9,14), appointment_time=time(12,0), status="BOOKED", patient_id=p3.id, dentist_id=d2.id, surgery_id=surg2.id)
    appt5 = Appointment(appointment_date=date(2013,9,14), appointment_time=time(13,0), status="BOOKED", patient_id=p2.id, dentist_id=d3.id, surgery_id=surg3.id)
    appt6 = Appointment(appointment_date=date(2013,9,15), appointment_time=time(14,0), status="BOOKED", patient_id=p4.id, dentist_id=d3.id, surgery_id=surg3.id)
    session.add_all([appt1, appt2, appt3, appt4, appt5, appt6])

    # Commit and close session
    session.commit()
    session.close()

if __name__ == "__main__":
    bootstrap()