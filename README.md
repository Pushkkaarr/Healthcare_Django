# Healthcare Django Backend API

A production-ready Django REST Framework application for managing healthcare operations with JWT authentication, patient management, doctor profiles, and patient-doctor assignments.

## Features

- **User Authentication**: JWT-based authentication with secure registration and login
- **Patient Management**: Complete CRUD operations for patient profiles
- **Doctor Management**: Comprehensive doctor profile management with specializations
- **Patient-Doctor Mapping**: Assign doctors to patients and manage relationships
- **PostgreSQL Database**: Using PostgreSQL for reliable data persistence
- **API Documentation**: RESTful API with DRF integrated filtering and searching
- **Permission System**: Role-based access control and ownership validation
- **Error Handling**: Comprehensive error handling with meaningful messages

```

## Prerequisites

- Python 3.8+
- PostgreSQL 10+
- pip or conda

## Installation and Setup

### 1. Clone the Repository

```bash
cd Healthcare_Django
```

### 2. Create Virtual Environment

**Using venv:**
```bash
python -m venv myenv
source myenv/bin/activate      # On Windows: myenv\Scripts\activate
```

**Using conda:**
```bash
conda create --name myenv python=3.10
conda activate myenv
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy the `.env.example` to `.env` and update the values:

Edit `.env` with your configuration:
```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 5. Create PostgreSQL Database

```bash
# Use psql or your PostgreSQL client
CREATE DATABASE healthcare_db;
CREATE USER postgres WITH PASSWORD 'your_postgres_password';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET default_transaction_deferrable TO on;
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE healthcare_db TO postgres;
```

### 6. Run Migrations

```bash
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 8. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication Endpoints

#### Register User
```
POST /api/auth/register/
Content-Type: application/json

{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "password_confirm": "SecurePass123"
}
```

**Response (201):**
```json
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "email": "john@example.com",
        "name": "John Doe",
        "created_at": "2024-02-16T10:00:00Z",
        "updated_at": "2024-02-16T10:00:00Z"
    }
}
```

#### Login User
```
POST /api/auth/login/
Content-Type: application/json

{
    "email": "john@example.com",
    "password": "SecurePass123"
}
```

**Response (200):**
```json
{
    "message": "Login successful",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
        "id": 1,
        "email": "john@example.com",
        "name": "John Doe",
        "created_at": "2024-02-16T10:00:00Z",
        "updated_at": "2024-02-16T10:00:00Z"
    }
}
```

#### Get User Profile (Authenticated)
```
GET /api/auth/profile/
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
    "id": 1,
    "email": "john@example.com",
    "name": "John Doe",
    "created_at": "2024-02-16T10:00:00Z",
    "updated_at": "2024-02-16T10:00:00Z"
}
```

#### Refresh Token
```
POST /api/auth/token/refresh/
Content-Type: application/json

{
    "refresh": "<refresh_token>"
}
```

### Patient Endpoints

All patient endpoints require JWT authentication. Users can only access their own patient records.

#### Create Patient
```
POST /api/patients/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane@example.com",
    "phone": "+1234567890",
    "date_of_birth": "1990-05-15",
    "gender": "F",
    "blood_type": "O+",
    "address": "123 Main Street",
    "city": "New York",
    "state": "NY",
    "postal_code": "10001",
    "medical_history": "No major illnesses",
    "allergies": "Penicillin",
    "emergency_contact": "John Doe",
    "emergency_phone": "+1234567891"
}
```

**Response (201):**
```json
{
    "message": "Patient created successfully",
    "data": {
        "id": 1,
        "user": {...},
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com",
        ...
    }
}
```

#### List Patients
```
GET /api/patients/
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
    "count": 1,
    "patients": [
        {
            "id": 1,
            "user": {...},
            "first_name": "Jane",
            "last_name": "Doe",
            ...
        }
    ]
}
```

#### Get Patient Details
```
GET /api/patients/<id>/
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
    "id": 1,
    "user": {...},
    "first_name": "Jane",
    "last_name": "Doe",
    ...
}
```

#### Update Patient
```
PUT /api/patients/<id>/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "phone": "+1234567892",
    ...
}
```

**Response (200):**
```json
{
    "message": "Patient updated successfully",
    "data": {...}
}
```

#### Delete Patient
```
DELETE /api/patients/<id>/
Authorization: Bearer <access_token>
```

**Response (204):** No content

### Doctor Endpoints

All doctor endpoints require JWT authentication.

#### Create Doctor
```
POST /api/doctors/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "first_name": "Michael",
    "last_name": "Smith",
    "email": "dr.smith@example.com",
    "phone": "+1234567890",
    "gender": "M",
    "specialization": "CARD",
    "license_number": "MD123456",
    "hospital_affiliation": "City Hospital",
    "experience_years": 10,
    "consultation_fee": "100.00",
    "bio": "Expert Cardiologist with 10 years of experience",
    "office_address": "456 Medical Street",
    "office_phone": "+1234567890",
    "available_days": "Mon, Tue, Wed, Thu, Fri",
    "available_hours": "9AM-5PM"
}
```

**Response (201):**
```json
{
    "message": "Doctor created successfully",
    "data": {...}
}
```

#### List Doctors
```
GET /api/doctors/
Authorization: Bearer <access_token>

Query Parameters:
- specialization: CARD, DERM, NEURO, etc.
- is_active: true/false
- search: search by name or specialization
- ordering: first_name, experience_years, etc.
```

**Response (200):**
```json
{
    "count": 5,
    "doctors": [...]
}
```

#### Get Doctor Details
```
GET /api/doctors/<id>/
Authorization: Bearer <access_token>
```

#### Update Doctor
```
PUT /api/doctors/<id>/
Authorization: Bearer <access_token>
Content-Type: application/json
```

#### Delete Doctor
```
DELETE /api/doctors/<id>/
Authorization: Bearer <access_token>
```

#### Get Specializations
```
GET /api/doctors/specializations/
Authorization: Bearer <access_token>
```

**Response (200):**
```json
[
    {"id": "GP", "name": "General Practitioner"},
    {"id": "CARD", "name": "Cardiologist"},
    ...
]
```

### Patient-Doctor Mapping Endpoints

#### Create Mapping (Assign Doctor to Patient)
```
POST /api/mappings/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "patient_id": 1,
    "doctor_id": 1,
    "status": "ACTIVE",
    "notes": "Primary care physician"
}
```

**Response (201):**
```json
{
    "message": "Doctor assigned to patient successfully",
    "data": {...}
}
```

#### List All Mappings
```
GET /api/mappings/
Authorization: Bearer <access_token>

Query Parameters:
- patient: <patient_id>
- doctor: <doctor_id>
- status: ACTIVE, INACTIVE, SUSPENDED
- search: search by patient or doctor name
```

**Response (200):**
```json
{
    "count": 3,
    "mappings": [...]
}
```

#### Get Doctors for a Specific Patient
```
GET /api/mappings/by_patient/?patient_id=<id>
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
    "patient_id": 1,
    "doctor_count": 2,
    "doctors": [...]
}
```

#### Update Mapping
```
PUT /api/mappings/<id>/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "status": "INACTIVE",
    "notes": "Updated notes"
}
```

#### Delete Mapping
```
DELETE /api/mappings/<id>/
Authorization: Bearer <access_token>
```

#### Get Mapping Statuses
```
GET /api/mappings/statuses/
Authorization: Bearer <access_token>
```

## Security Features

- JWT-based stateless authentication
- Password hashing using Django's built-in functions
- CORS protection
- Permission classes for endpoint access control
- Input validation at serializer level
- Ownership checks for user data
- Environment variable-based configuration

This project is provided as-is for healthcare management purposes.

---

**Last Updated:** February 16, 2024
