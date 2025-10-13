from datetime import date, time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Address, Surgery, Dentist, Patient, Appointment

engine = create_engine("sqlite:///ads_dental.db", echo=False, future=True)
Session = sessionmaker(bind=engine, autoflush=False)

def bootstrap():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    s = Session()

    addr1 = Address(street="123 West Avenue", city="Phoenix", state="AZ", zip_code="85012")
    addr2 = Address(street="900 Johns Street", city="Cleveland", state="OH", zip_code="43098")
    addr3 = Address(street="45 Green Street", city="Dallas", state="TX", zip_code="75201")
    s.add_all([addr1, addr2, addr3])

    surg1 = Surgery(surgery_no="S15", name="Bells Court Dental", phone="480-123-0000", address=addr1)
    surg2 = Surgery(surgery_no="S10", name="The Galleria Surgery", phone="216-222-1111", address=addr2)
    surg3 = Surgery(surgery_no="S13", name="Pearl Dental South", phone="972-333-4444", address=addr3)
    s.add_all([surg1, surg2, surg3])

    d1 = Dentist(first_name="Tony", last_name="Smith", email="tsmith@ads.com", surgery=surg1)
    d2 = Dentist(first_name="Helen", last_name="Pearson", email="hpearson@ads.com", surgery=surg2)
    d3 = Dentist(first_name="Robin", last_name="Plevin", email="rplevin@ads.com", surgery=surg3)
    s.add_all([d1, d2, d3])

    p1 = Patient(patient_no="P100", first_name="Gillian", last_name="White", email="gwhite@mail.com", address=addr1)
    p2 = Patient(patient_no="P105", first_name="Jill", last_name="Bell", email="jbell@mail.com", address=addr1)
    p3 = Patient(patient_no="P108", first_name="Ian", last_name="MacKay", email="ianm@mail.com", address=addr2)
    p4 = Patient(patient_no="P110", first_name="John", last_name="Walker", email="jwalker@mail.com", address=addr3)
    s.add_all([p1, p2, p3, p4])

    s.add_all([
        Appointment(appt_date=date(2013,9,12), appt_time=time(10,0), patient=p1, dentist=d1, surgery=surg1),
        Appointment(appt_date=date(2013,9,12), appt_time=time(12,0), patient=p2, dentist=d1, surgery=surg1),
        Appointment(appt_date=date(2013,9,13), appt_time=time(10,0), patient=p3, dentist=d2, surgery=surg2),
        Appointment(appt_date=date(2013,9,14), appt_time=time(14,0), patient=p3, dentist=d2, surgery=surg2),
        Appointment(appt_date=date(2013,9,14), appt_time=time(16,30), patient=p2, dentist=d3, surgery=surg3),
        Appointment(appt_date=date(2013,9,15), appt_time=time(18,0), patient=p4, dentist=d3, surgery=surg3),
    ])

    s.commit()
    s.close()

if __name__ == "__main__":
    bootstrap()