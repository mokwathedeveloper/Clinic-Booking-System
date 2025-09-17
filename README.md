# Clinic Booking System

A comprehensive FastAPI-based clinic appointment booking system with patient management and appointment scheduling capabilities.

## 🏥 Features

### Patient Management
- Create, read, update, and delete patient records
- Email uniqueness validation
- Search patients by name or email
- Pagination support for large datasets

### Appointment Management
- Schedule, update, and cancel appointments
- Filter appointments by patient, status, or date
- Appointment status tracking (scheduled, completed, cancelled)
- Patient-appointment relationship management

### API Features
- RESTful API design with proper HTTP status codes
- Automatic API documentation with Swagger/OpenAPI
- Input validation using Pydantic schemas
- Comprehensive error handling
- Database session management
- System statistics and health monitoring

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI 0.104.1
- **Database**: MySQL with SQLAlchemy ORM
- **Validation**: Pydantic schemas
- **Server**: Uvicorn ASGI server
- **Database Driver**: PyMySQL
- **Environment Management**: python-dotenv

## 📋 Requirements

- Python 3.8+
- MySQL 5.7+ or MySQL 8.0+
- pip (Python package manager)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/mokwathedeveloper/Clinic-Booking-System.git
cd Clinic-Booking-System
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup

#### Create MySQL Database
```sql
CREATE DATABASE clinic_booking_system;
CREATE USER 'clinic_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON clinic_booking_system.* TO 'clinic_user'@'localhost';
FLUSH PRIVILEGES;
```

#### Environment Configuration
1. Copy the environment template:
```bash
cp .env.example .env
```

2. Edit `.env` file with your database credentials:
```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=clinic_user
DB_PASSWORD=your_password
DB_NAME=clinic_booking_system

# Application Configuration
APP_HOST=127.0.0.1
APP_PORT=8000
DEBUG=True
```

### 5. Run the Application
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

The application will be available at:
- **API**: http://127.0.0.1:8000
- **Interactive API Documentation**: http://127.0.0.1:8000/docs
- **Alternative API Documentation**: http://127.0.0.1:8000/redoc

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:8000
```

### Authentication
Currently, the API does not require authentication. This is suitable for development and testing purposes.

### Core Endpoints

#### System Endpoints
- `GET /` - API welcome message and links
- `GET /health` - Health check endpoint
- `GET /stats/` - System statistics

#### Patient Endpoints
- `POST /patients/` - Create a new patient
- `GET /patients/` - List all patients (with search and pagination)
- `GET /patients/{patient_id}` - Get specific patient
- `PUT /patients/{patient_id}` - Update patient information
- `DELETE /patients/{patient_id}` - Delete patient

#### Appointment Endpoints
- `POST /appointments/` - Create a new appointment
- `GET /appointments/` - List all appointments (with filters)
- `GET /appointments/{appointment_id}` - Get specific appointment
- `PUT /appointments/{appointment_id}` - Update appointment
- `DELETE /appointments/{appointment_id}` - Delete appointment
- `GET /patients/{patient_id}/appointments` - Get patient's appointments

### Query Parameters

#### Pagination
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 100, max: 1000)

#### Filtering
- `search`: Search term for patient name or email
- `patient_id`: Filter appointments by patient
- `status`: Filter appointments by status (scheduled, completed, cancelled)
- `date`: Filter appointments by date (YYYY-MM-DD format)

## 🧪 Testing the API

### Using curl

#### Create a Patient
```bash
curl -X POST "http://127.0.0.1:8000/patients/" \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "John",
       "last_name": "Doe",
       "email": "john.doe@email.com",
       "phone": "+1234567890",
       "date_of_birth": "1990-01-15",
       "address": "123 Main St, City, State"
     }'
```

#### Create an Appointment
```bash
curl -X POST "http://127.0.0.1:8000/appointments/" \
     -H "Content-Type: application/json" \
     -d '{
       "patient_id": 1,
       "appointment_date": "2024-01-20T10:00:00",
       "reason": "Regular checkup",
       "notes": "Annual physical examination"
     }'
```

#### Get All Patients
```bash
curl "http://127.0.0.1:8000/patients/"
```

#### Search Patients
```bash
curl "http://127.0.0.1:8000/patients/?search=john"
```

### Using the Interactive Documentation
Visit http://127.0.0.1:8000/docs to use the built-in Swagger UI for testing all endpoints interactively.

## 📁 Project Structure

```
Clinic-Booking-System/
├── main.py              # FastAPI application and routes
├── database.py          # Database configuration and connection
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic validation schemas
├── crud.py              # Database CRUD operations
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # Project documentation
```

## 🗃️ Database Schema

The system uses two main entities with a one-to-many relationship:

### Patients Table
- `id` (Primary Key)
- `first_name`
- `last_name`
- `email` (Unique)
- `phone`
- `date_of_birth`
- `address`
- `created_at`
- `updated_at`

### Appointments Table
- `id` (Primary Key)
- `patient_id` (Foreign Key)
- `appointment_date`
- `reason`
- `status` (scheduled/completed/cancelled)
- `notes`
- `created_at`
- `updated_at`

## 🔧 Development

### Code Structure
- **models.py**: SQLAlchemy ORM models defining database structure
- **schemas.py**: Pydantic models for request/response validation
- **crud.py**: Database operations organized in classes
- **main.py**: FastAPI application with all API endpoints
- **database.py**: Database connection and session management

### Adding New Features
1. Update models in `models.py` if database changes are needed
2. Add corresponding Pydantic schemas in `schemas.py`
3. Implement CRUD operations in `crud.py`
4. Create API endpoints in `main.py`
5. Update documentation

## 🚨 Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request (validation errors, conflicts)
- `404`: Not Found
- `500`: Internal Server Error

Error responses include descriptive messages to help with debugging.

## 📝 Assignment Requirements

This project fulfills the Week 8 Final Project requirements:

✅ **Entities**: Patient and Appointment models with proper relationships  
✅ **FastAPI**: Complete REST API implementation  
✅ **MySQL**: Database integration with SQLAlchemy  
✅ **CRUD Operations**: Full Create, Read, Update, Delete functionality  
✅ **Validation**: Pydantic schemas for input validation  
✅ **Documentation**: Comprehensive README and API docs  
✅ **Environment**: Proper configuration management  
✅ **Requirements**: All dependencies listed in requirements.txt  

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is created for educational purposes as part of a FastAPI learning assignment.

## 👨‍💻 Author

**Mokwa The Developer**  
GitHub: [@mokwathedeveloper](https://github.com/mokwathedeveloper)

---

For questions or support, please refer to the API documentation at `/docs` or create an issue in the repository.
