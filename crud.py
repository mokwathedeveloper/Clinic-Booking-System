"""
CRUD operations for database entities
"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime, date

from models import Patient, Appointment
from schemas import PatientCreate, PatientUpdate, AppointmentCreate, AppointmentUpdate


# Patient CRUD Operations
class PatientCRUD:
    """CRUD operations for Patient model"""

    @staticmethod
    def create_patient(db: Session, patient: PatientCreate) -> Patient:
        """Create a new patient"""
        db_patient = Patient(**patient.dict())
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
        return db_patient

    @staticmethod
    def get_patient(db: Session, patient_id: int) -> Optional[Patient]:
        """Get a patient by ID"""
        return db.query(Patient).filter(Patient.id == patient_id).first()

    @staticmethod
    def get_patient_by_email(db: Session, email: str) -> Optional[Patient]:
        """Get a patient by email"""
        return db.query(Patient).filter(Patient.email == email).first()

    @staticmethod
    def get_patients(db: Session, skip: int = 0, limit: int = 100) -> List[Patient]:
        """Get all patients with pagination"""
        return db.query(Patient).offset(skip).limit(limit).all()

    @staticmethod
    def search_patients(db: Session, search_term: str, skip: int = 0, limit: int = 100) -> List[Patient]:
        """Search patients by name or email"""
        search_filter = or_(
            Patient.first_name.ilike(f"%{search_term}%"),
            Patient.last_name.ilike(f"%{search_term}%"),
            Patient.email.ilike(f"%{search_term}%")
        )
        return db.query(Patient).filter(search_filter).offset(skip).limit(limit).all()

    @staticmethod
    def update_patient(db: Session, patient_id: int, patient_update: PatientUpdate) -> Optional[Patient]:
        """Update a patient"""
        db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if db_patient:
            update_data = patient_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_patient, field, value)
            db_patient.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_patient)
        return db_patient

    @staticmethod
    def delete_patient(db: Session, patient_id: int) -> bool:
        """Delete a patient"""
        db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if db_patient:
            db.delete(db_patient)
            db.commit()
            return True
        return False

    @staticmethod
    def get_patient_count(db: Session) -> int:
        """Get total count of patients"""
        return db.query(Patient).count()


# Appointment CRUD Operations
class AppointmentCRUD:
    """CRUD operations for Appointment model"""

    @staticmethod
    def create_appointment(db: Session, appointment: AppointmentCreate) -> Optional[Appointment]:
        """Create a new appointment"""
        # Check if patient exists
        patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()
        if not patient:
            return None

        db_appointment = Appointment(**appointment.dict())
        db.add(db_appointment)
        db.commit()
        db.refresh(db_appointment)
        return db_appointment

    @staticmethod
    def get_appointment(db: Session, appointment_id: int) -> Optional[Appointment]:
        """Get an appointment by ID with patient information"""
        return db.query(Appointment).options(joinedload(Appointment.patient)).filter(
            Appointment.id == appointment_id
        ).first()

    @staticmethod
    def get_appointments(db: Session, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """Get all appointments with pagination"""
        return db.query(Appointment).options(joinedload(Appointment.patient)).offset(skip).limit(limit).all()

    @staticmethod
    def get_patient_appointments(db: Session, patient_id: int, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """Get all appointments for a specific patient"""
        return db.query(Appointment).options(joinedload(Appointment.patient)).filter(
            Appointment.patient_id == patient_id
        ).offset(skip).limit(limit).all()

    @staticmethod
    def get_appointments_by_date(db: Session, target_date: date, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """Get appointments for a specific date"""
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = datetime.combine(target_date, datetime.max.time())

        return db.query(Appointment).options(joinedload(Appointment.patient)).filter(
            and_(
                Appointment.appointment_date >= start_datetime,
                Appointment.appointment_date <= end_datetime
            )
        ).offset(skip).limit(limit).all()

    @staticmethod
    def get_appointments_by_status(db: Session, status: str, skip: int = 0, limit: int = 100) -> List[Appointment]:
        """Get appointments by status"""
        return db.query(Appointment).options(joinedload(Appointment.patient)).filter(
            Appointment.status == status
        ).offset(skip).limit(limit).all()

    @staticmethod
    def update_appointment(db: Session, appointment_id: int, appointment_update: AppointmentUpdate) -> Optional[Appointment]:
        """Update an appointment"""
        db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
        if db_appointment:
            update_data = appointment_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_appointment, field, value)
            db_appointment.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_appointment)
        return db_appointment

    @staticmethod
    def delete_appointment(db: Session, appointment_id: int) -> bool:
        """Delete an appointment"""
        db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
        if db_appointment:
            db.delete(db_appointment)
            db.commit()
            return True
        return False

    @staticmethod
    def get_appointment_count(db: Session) -> int:
        """Get total count of appointments"""
        return db.query(Appointment).count()

    @staticmethod
    def get_appointment_count_by_status(db: Session, status: str) -> int:
        """Get count of appointments by status"""
        return db.query(Appointment).filter(Appointment.status == status).count()


# Convenience instances
patient_crud = PatientCRUD()
appointment_crud = AppointmentCRUD()
