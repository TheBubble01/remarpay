# remarpay

### Project Name

**RemarPay Backend**

### Description

Django-based backend for RemarPay, supporting multi-role users (cashiers, agents, managers, tech-admins), transaction flows, rate management, user preferences, and more.

### Tech Stack

- Python 3.11+
- Django 4+
- Django REST Framework
- SimpleJWT for Authentication

### Key Features

- JWT Authentication
- Role-based permissions
- Currency exchange transaction logic
- Auto-calculated conversions + fee deduction
- Receipt generation (for frontend rendering)
- Agent payment confirmations
- User management + suspension
- Rate control and versioning
- Dark mode and timezone preferences
- Notification system
- Search & Filter system

### Setup Instructions

```bash
# Create and activate virtualenv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Migrate DB
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run dev server
python manage.py runserver
```

---

