-- =========================================================
-- STEP 1: Create and use database
-- =========================================================
CREATE DATABASE IF NOT EXISTS ADSDentalSurgeryDB;
USE ADSDentalSurgeryDB;

-- =========================================================
-- STEP 2: Create Tables
-- =========================================================

-- Table: Surgery
CREATE TABLE Surgery (
    surgeryId INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    locationAddress VARCHAR(255) NOT NULL,
    telephone VARCHAR(20) NOT NULL
);

-- Table: Dentist
CREATE TABLE Dentist (
    dentistId INT PRIMARY KEY AUTO_INCREMENT,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    phoneNumber VARCHAR(20),
    email VARCHAR(100),
    specialization VARCHAR(100),
    surgeryId INT,
    CONSTRAINT fk_dentist_surgery
        FOREIGN KEY (surgeryId)
        REFERENCES Surgery(surgeryId)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- Table: Patient
CREATE TABLE Patient (
    patientId INT PRIMARY KEY AUTO_INCREMENT,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    phoneNumber VARCHAR(20),
    email VARCHAR(100),
    address VARCHAR(255),
    dateOfBirth DATE
);

-- Table: Appointment
CREATE TABLE Appointment (
    appointmentId INT PRIMARY KEY AUTO_INCREMENT,
    appointmentDate DATE NOT NULL,
    appointmentTime TIME NOT NULL,
    status VARCHAR(20) DEFAULT 'booked',
    dentistId INT,
    patientId INT,
    surgeryId INT,
    CONSTRAINT fk_appointment_dentist
        FOREIGN KEY (dentistId)
        REFERENCES Dentist(dentistId)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_appointment_patient
        FOREIGN KEY (patientId)
        REFERENCES Patient(patientId)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_appointment_surgery
        FOREIGN KEY (surgeryId)
        REFERENCES Surgery(surgeryId)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- =========================================================
-- STEP 3: Insert Sample Data
-- =========================================================

-- Surgeries
INSERT INTO Surgery (name, locationAddress, telephone) VALUES
('Smile Dental Center', '123 Main St, Dallas, TX', '214-555-9821'),
('Happy Teeth Clinic', '890 Maple Ave, Chicago, IL', '312-555-4412');

-- Dentists
INSERT INTO Dentist (firstName, lastName, phoneNumber, email, specialization, surgeryId) VALUES
('Robert', 'Lanskov', '214-555-4444', 'rlanskov@smile.com', 'Orthodontist', 1),
('Anna', 'Smith', '312-555-8899', 'asmith@happyteeth.com', 'Pediatric Dentist', 2);

-- Patients
INSERT INTO Patient (firstName, lastName, phoneNumber, email, address, dateOfBirth) VALUES
('James', 'Turner', '214-555-1212', 'jturner@mail.com', '125 Oak St, Dallas, TX', '1988-07-12'),
('Emily', 'Johnson', '312-555-4447', 'ejohnson@mail.com', '450 Pine Ave, Chicago, IL', '1993-03-09');

-- Appointments
INSERT INTO Appointment (appointmentDate, appointmentTime, status, dentistId, patientId, surgeryId) VALUES
('2025-10-10', '09:00:00', 'booked', 1, 1, 1),
('2025-10-11', '10:30:00', 'booked', 2, 2, 2),
('2025-10-12', '11:00:00', 'completed', 1, 1, 1);

-- =========================================================
-- STEP 4: Queries
-- =========================================================

-- 1. List all dentists sorted by last name
SELECT dentistId, firstName, lastName, phoneNumber, email, specialization
FROM Dentist
ORDER BY lastName ASC;

-- 2. List all appointments for a given dentist, including patient info
SELECT 
    a.appointmentId,
    a.appointmentDate,
    a.appointmentTime,
    p.firstName AS patientFirstName,
    p.lastName AS patientLastName,
    s.name AS surgeryName
FROM Appointment a
JOIN Patient p ON a.patientId = p.patientId
JOIN Surgery s ON a.surgeryId = s.surgeryId
WHERE a.dentistId = 1;

-- 3. List all appointments scheduled at a specific surgery
SELECT 
    a.appointmentId,
    a.appointmentDate,
    a.appointmentTime,
    d.firstName AS dentistFirstName,
    d.lastName AS dentistLastName
FROM Appointment a
JOIN Dentist d ON a.dentistId = d.dentistId
WHERE a.surgeryId = 1;

-- 4. List appointments for a given patient on a given date
SELECT 
    a.appointmentId,
    a.appointmentDate,
    a.appointmentTime,
    d.firstName AS dentistFirstName,
    d.lastName AS dentistLastName,
    s.name AS surgeryName
FROM Appointment a
JOIN Dentist d ON a.dentistId = d.dentistId
JOIN Surgery s ON a.surgeryId = s.surgeryId
WHERE a.patientId = 1 AND a.appointmentDate = '2025-10-10';

-- 5. Display all appointments with dentist and patient details
SELECT 
    a.appointmentId,
    a.appointmentDate,
    a.appointmentTime,
    d.firstName AS dentistName,
    p.firstName AS patientName,
    s.name AS surgeryName,
    a.status
FROM Appointment a
JOIN Dentist d ON a.dentistId = d.dentistId
JOIN Patient p ON a.patientId = p.patientId
JOIN Surgery s ON a.surgeryId = s.surgeryId
ORDER BY a.appointmentDate;
