-- Clinic Booking System Database Schema
-- Generated from SQLAlchemy models
-- Compatible with MySQL

CREATE DATABASE IF NOT EXISTS clinic_booking_system;
USE clinic_booking_system;

-- Patients table
CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    date_of_birth DATE NOT NULL,
    address TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_patients_email (email),
    INDEX idx_patients_id (id)
);

-- Appointments table
CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    appointment_date DATETIME NOT NULL,
    reason TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'scheduled',
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    INDEX idx_appointments_patient_id (patient_id),
    INDEX idx_appointments_date (appointment_date),
    INDEX idx_appointments_status (status),
    INDEX idx_appointments_id (id)
);

-- Sample data for testing
INSERT INTO patients (first_name, last_name, email, phone, date_of_birth, address) VALUES
('John', 'Doe', 'john.doe@email.com', '+1234567890', '1990-01-15', '123 Main St, City, State'),
('Jane', 'Smith', 'jane.smith@email.com', '+0987654321', '1985-05-20', '456 Oak Ave, Town, State'),
('Bob', 'Johnson', 'bob.johnson@email.com', '+1122334455', '1978-12-03', '789 Pine Rd, Village, State');

INSERT INTO appointments (patient_id, appointment_date, reason, status, notes) VALUES
(1, '2024-01-20 10:00:00', 'Regular checkup', 'scheduled', 'Annual physical examination'),
(1, '2024-02-15 14:30:00', 'Follow-up visit', 'scheduled', 'Blood test results review'),
(2, '2024-01-21 14:30:00', 'Consultation', 'completed', 'Initial consultation completed'),
(2, '2024-01-25 09:00:00', 'Treatment', 'scheduled', 'Scheduled treatment session'),
(3, '2024-01-18 11:15:00', 'Emergency visit', 'completed', 'Emergency consultation - resolved');

-- Constraints and additional indexes for performance
ALTER TABLE appointments ADD CONSTRAINT chk_status CHECK (status IN ('scheduled', 'completed', 'cancelled'));
ALTER TABLE patients ADD CONSTRAINT chk_email_format CHECK (email LIKE '%@%.%');
