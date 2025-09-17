"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Optional, List


# Patient Schemas
class PatientBase(BaseModel):
    """Base patient schema with common fields"""
    first_name: str = Field(..., min_length=1, max_length=50, description="Patient's first name")
    last_name: str = Field(..., min_length=1, max_length=50, description="Patient's last name")
    email: EmailStr = Field(..., description="Patient's email address")
    phone: str = Field(..., min_length=10, max_length=20, description="Patient's phone number")
    date_of_birth: date = Field(..., description="Patient's date of birth")
    address: Optional[str] = Field(None, max_length=500, description="Patient's address")


class PatientCreate(PatientBase):
    """Schema for creating a new patient"""
    pass


class PatientUpdate(BaseModel):
    """Schema for updating patient information"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    date_of_birth: Optional[date] = None
    address: Optional[str] = Field(None, max_length=500)


class PatientResponse(PatientBase):
    """Schema for patient response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Appointment Schemas
class AppointmentBase(BaseModel):
    """Base appointment schema with common fields"""
    appointment_date: datetime = Field(..., description="Date and time of the appointment")
    reason: str = Field(..., min_length=1, max_length=1000, description="Reason for the appointment")
    notes: Optional[str] = Field(None, max_length=2000, description="Additional notes")


class AppointmentCreate(AppointmentBase):
    """Schema for creating a new appointment"""
    patient_id: int = Field(..., gt=0, description="ID of the patient")


class AppointmentUpdate(BaseModel):
    """Schema for updating appointment information"""
    appointment_date: Optional[datetime] = None
    reason: Optional[str] = Field(None, min_length=1, max_length=1000)
    status: Optional[str] = Field(None, regex="^(scheduled|completed|cancelled)$")
    notes: Optional[str] = Field(None, max_length=2000)


class AppointmentResponse(AppointmentBase):
    """Schema for appointment response"""
    id: int
    patient_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    patient: Optional[PatientResponse] = None

    class Config:
        from_attributes = True


# List Response Schemas
class PatientListResponse(BaseModel):
    """Schema for paginated patient list response"""
    patients: List[PatientResponse]
    total: int
    page: int
    size: int


class AppointmentListResponse(BaseModel):
    """Schema for paginated appointment list response"""
    appointments: List[AppointmentResponse]
    total: int
    page: int
    size: int


# Status Response Schema
class StatusResponse(BaseModel):
    """Schema for status responses"""
    message: str
    success: bool = True
