# DEVELOPER-NOTES.md – RemarPay

## Common Commands

### Backend

```bash
# Run dev server
python manage.py runserver

# Migrate
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Reset admin password
python manage.py changepassword <email>

# Load shell
python manage.py shell
```

### Frontend

```bash
# Start dev
npm run dev

# Build for production
npm run build
```

---

## Useful Tips

- Backend uses **JWT Auth**: Login returns access + refresh tokens
- Store token in `localStorage`, decode it on login to get: `user_id`, `name`, `role`
- All role-based checks can be done using `role` value in frontend
- `axios` has interceptor for token auth

---

## Testing User Accounts (suggested values)

| Role       | Email                                                | Password    |
| ---------- | ---------------------------------------------------- | ----------- |
| Tech-Admin | [admin@remarpay.com](mailto\:admin@remarpay.com)     | password123 |
| Cashier    | [cashier@remarpay.com](mailto\:cashier@remarpay.com) | password123 |
| Agent      | [agent@remarpay.com](mailto\:agent@remarpay.com)     | password123 |
| Manager    | [manager@remarpay.com](mailto\:manager@remarpay.com) | password123 |

These can be modified via Django admin or API endpoints.

---

## Known Endpoints

- `/api/login/` → Login (JWT)
- `/api/accounts/register/` → Tech-admin only
- `/api/accounts/profile/` → View logged-in user
- `/api/accounts/suspend/` → Tech-admin + Chief Manager
- `/api/payments/request/` → Cashiers initiate payments

---

## Notes

- Don’t forget to restart the server after model changes.
- Use `devtools` in browser to inspect network requests.
- Frontend is **100% responsive**.
- Top bar + sidebar layouts are consistent across views.
- Dark mode is based on system preference, but user setting will override.

*Last updated: July 15, 2025*

