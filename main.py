"""
FastAPI Clinic Booking System
Main application entry point
"""

from fastapi import FastAPI

app = FastAPI(
    title="Clinic Booking System",
    description="A FastAPI-based clinic appointment booking system",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to Clinic Booking System API"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
