# API Reference – RemarPay

## Base URL

```
/api/
```

All endpoints are prefixed with `/api/`

## Auth Endpoints

### POST `/token/`

Obtain access + refresh tokens. **Body:**

```json
{
  "email": "cashier@example.com",
  "password": "pass1234"
}
```

**Response:**

```json
{
  "access": "...",
  "refresh": "...",
  "name": "Ali Ibrahim",
  "role": "cashier"
}
```

### POST `/token/refresh/`

Refresh access token.

---

## User Management

### POST `/register/`

Only tech-admins can register users.

### GET `/users/profile/`

Returns authenticated user profile.

### POST `/users/suspend/`

Suspend or unsuspend a user. **Body:**

```json
{
  "user_id": 3,
  "is_suspended": true
}
```

### POST `/users/change-password/`

Change own password (must be authenticated).

---

## Payment Requests

### POST `/payments/request/`

Cashier submits a new payment request. **Body:** (varies based on country)

```json
{
  "client_name": "John Doe",
  "amount": 300,
  "destination_country": "Nigeria",
  "payment_details": {
    "bank_name": "GTB",
    "account_number": "0123456789",
    "account_name": "Doe John",
    "depositor_name": "Ali Ibrahim",
    "depositor_phone": "+2348012345678"
  }
}
```

### GET `/payments/request/{id}/`

View a specific payment request.

### GET `/payments/history/`

Lists all requests submitted by the authenticated cashier.

---

## Notes

- Token required on all non-auth routes
- Role-based access enforced:
  - Only cashiers can submit requests
  - Only managers can approve payments
- Country-specific dynamic fields handled on frontend
- JWT returns user name + role for conditional UI rendering

