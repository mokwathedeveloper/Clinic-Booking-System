"""
FastAPI Clinic Booking System
Main application entry point
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from database import get_db, create_tables
from models import Patient, Appointment
from schemas import (
    PatientCreate, PatientUpdate, PatientResponse, PatientListResponse,
    AppointmentCreate, AppointmentUpdate, AppointmentResponse, AppointmentListResponse,
    StatusResponse
)
from crud import patient_crud, appointment_crud

# Create database tables
create_tables()

app = FastAPI(
    title="Clinic Booking System",
    description="A FastAPI-based clinic appointment booking system with patient and appointment management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Clinic Booking System API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", response_model=StatusResponse)
async def health_check():
    """Health check endpoint"""
    return StatusResponse(message="Clinic Booking System is running healthy", success=True)


# Patient Endpoints
@app.post("/patients/", response_model=PatientResponse, status_code=201)
async def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    """Create a new patient"""
    # Check if email already exists
    existing_patient = patient_crud.get_patient_by_email(db, patient.email)
    if existing_patient:
        raise HTTPException(status_code=400, detail="Email already registered")

    return patient_crud.create_patient(db, patient)

@app.get("/patients/", response_model=PatientListResponse)
async def get_patients(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    search: Optional[str] = Query(None, description="Search term for name or email"),
    db: Session = Depends(get_db)
):
    """Get all patients with optional search and pagination"""
    if search:
        patients = patient_crud.search_patients(db, search, skip, limit)
    else:
        patients = patient_crud.get_patients(db, skip, limit)

    total = patient_crud.get_patient_count(db)

    return PatientListResponse(
        patients=patients,
        total=total,
        page=skip // limit + 1,
        size=len(patients)
    )

@app.get("/patients/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """Get a specific patient by ID"""
    patient = patient_crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.put("/patients/{patient_id}", response_model=PatientResponse)
async def update_patient(patient_id: int, patient_update: PatientUpdate, db: Session = Depends(get_db)):
    """Update a patient's information"""
    # Check if patient exists
    existing_patient = patient_crud.get_patient(db, patient_id)
    if not existing_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Check email uniqueness if email is being updated
    if patient_update.email:
        email_patient = patient_crud.get_patient_by_email(db, patient_update.email)
        if email_patient and email_patient.id != patient_id:
            raise HTTPException(status_code=400, detail="Email already registered")

    updated_patient = patient_crud.update_patient(db, patient_id, patient_update)
    return updated_patient

@app.delete("/patients/{patient_id}", response_model=StatusResponse)
async def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    """Delete a patient"""
    success = patient_crud.delete_patient(db, patient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")

    return StatusResponse(message="Patient deleted successfully", success=True)


# Appointment Endpoints
@app.post("/appointments/", response_model=AppointmentResponse, status_code=201)
async def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    """Create a new appointment"""
    # Check if patient exists
    patient = patient_crud.get_patient(db, appointment.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    created_appointment = appointment_crud.create_appointment(db, appointment)
    if not created_appointment:
        raise HTTPException(status_code=400, detail="Failed to create appointment")

    return created_appointment

@app.get("/appointments/", response_model=AppointmentListResponse)
async def get_appointments(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    patient_id: Optional[int] = Query(None, description="Filter by patient ID"),
    status: Optional[str] = Query(None, description="Filter by appointment status"),
    date: Optional[date] = Query(None, description="Filter by appointment date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get all appointments with optional filters and pagination"""
    if patient_id:
        appointments = appointment_crud.get_patient_appointments(db, patient_id, skip, limit)
    elif status:
        appointments = appointment_crud.get_appointments_by_status(db, status, skip, limit)
    elif date:
        appointments = appointment_crud.get_appointments_by_date(db, date, skip, limit)
    else:
        appointments = appointment_crud.get_appointments(db, skip, limit)

    total = appointment_crud.get_appointment_count(db)

    return AppointmentListResponse(
        appointments=appointments,
        total=total,
        page=skip // limit + 1,
        size=len(appointments)
    )

@app.get("/appointments/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """Get a specific appointment by ID"""
    appointment = appointment_crud.get_appointment(db, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@app.put("/appointments/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: int,
    appointment_update: AppointmentUpdate,
    db: Session = Depends(get_db)
):
    """Update an appointment"""
    # Check if appointment exists
    existing_appointment = appointment_crud.get_appointment(db, appointment_id)
    if not existing_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    updated_appointment = appointment_crud.update_appointment(db, appointment_id, appointment_update)
    return updated_appointment

@app.delete("/appointments/{appointment_id}", response_model=StatusResponse)
async def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """Delete an appointment"""
    success = appointment_crud.delete_appointment(db, appointment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return StatusResponse(message="Appointment deleted successfully", success=True)

@app.get("/patients/{patient_id}/appointments", response_model=AppointmentListResponse)
async def get_patient_appointments(
    patient_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    """Get all appointments for a specific patient"""
    # Check if patient exists
    patient = patient_crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    appointments = appointment_crud.get_patient_appointments(db, patient_id, skip, limit)
    total = len(appointments)  # For this specific patient

    return AppointmentListResponse(
        appointments=appointments,
        total=total,
        page=skip // limit + 1,
        size=len(appointments)
    )


# Statistics Endpoints
@app.get("/stats/", response_model=dict)
async def get_statistics(db: Session = Depends(get_db)):
    """Get system statistics"""
    total_patients = patient_crud.get_patient_count(db)
    total_appointments = appointment_crud.get_appointment_count(db)
    scheduled_appointments = appointment_crud.get_appointment_count_by_status(db, "scheduled")
    completed_appointments = appointment_crud.get_appointment_count_by_status(db, "completed")
    cancelled_appointments = appointment_crud.get_appointment_count_by_status(db, "cancelled")

    return {
        "total_patients": total_patients,
        "total_appointments": total_appointments,
        "scheduled_appointments": scheduled_appointments,
        "completed_appointments": completed_appointments,
        "cancelled_appointments": cancelled_appointments,
        "system_status": "operational"
    }
