# README – Backend

## Overview
RemarPay is a role-based currency exchange management platform. The backend is built with Django and Django REST Framework (DRF), with JWT authentication and modular apps for accounts, payments, and utilities. The system supports cashiers, payment agents, managers, and tech-admins with distinct privileges and workflows.

### Key Features
- Custom user model with email login
- JWT-based authentication with custom payload
- Role-based permission logic (cashier, agent, manager, tech-admin)
- Dynamic payment request forms based on selected country
- Suspensions and user management
- Timezone-aware timestamps

---

## Setup Instructions

### Requirements
- Python 3.10+
- Django 4.x
- PostgreSQL (or SQLite for local testing)
- Virtualenv recommended

### Installation
```bash
git clone https://github.com/your-org/remarpay-backend.git
cd remarpay-backend
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

### Local Dev DB (SQLite)
Update `.env` or settings to use SQLite for quick testing.

---

## Environment Variables
Create a `.env` file in the root:
```ini
DEBUG=True
SECRET_KEY=your-django-secret
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://user:pass@localhost:5432/remarpay
TIMEZONE=Africa/Lagos
JWT_SECRET_KEY=your-jwt-secret
```

---

## Common Commands

### Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser
```bash
python manage.py createsuperuser
```

---

## Authentication

### JWT Setup
- Uses `djangorestframework-simplejwt`
- Custom `MyTokenObtainPairSerializer` returns:
  ```json
  {
    "access": "...",
    "refresh": "...",
    "user": {
      "user_id": 1,
      "name": "Ali Ibrahim",
      "role": "cashier"
    }
  }
  ```

---

## Role-Based Access Logic
- Permissions are enforced using DRF permission classes and logic in views.
- Each role is limited to specific endpoints:
  - Cashier: Can create payment requests, view receipts
  - Agent: Can confirm requests assigned to them
  - Manager: Can assign agents, suspend users
  - Tech-admin: Full access to all features

---

## API Versioning
None implemented yet — planned for future phase.

---

## Deployment Readiness
- Code modular and well-commented
- All secrets are .env-driven
- DB-ready for production (PostgreSQL preferred)
- Static/media file handling pending
- CORS and HTTPS enforced in production settings (not enabled in dev)

