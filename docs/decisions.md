# DECISIONS.md – RemarPay

## Overview
This document captures all major product, technical, and UX decisions made during the development of RemarPay (backend + frontend).

---

### 1. **Custom User Model with Email Login**
- **Decision**: Use `AbstractBaseUser` and set email as `USERNAME_FIELD`.
- **Reason**: Email is more universal than username and reduces errors.

### 2. **Role-Based Access Control (RBAC)**
- **Roles**: `tech-admin`, `chief-manager`, `cashier`, `agent`
- **Decision**: Permissions enforced at the view level with custom logic.
- **Trade-Off**: No third-party RBAC library used for simplicity.

### 3. **JWT Auth**
- **Library**: `djangorestframework-simplejwt`
- **Decision**: Custom serializer to include name and role in token response.
- **Reason**: Enables UI to adapt based on role and user identity.

### 4. **Frontend Stack: React + Vite + Tailwind**
- **Decision**: Fast build times, easy Tailwind theming, full control.

### 5. **Responsive Sidebar with Toggle**
- **Decision**: Sidebar is collapsible even on desktop, hidden by default on mobile.
- **Reason**: Prevents UI clutter.

### 6. **Auto-Generated Client Receipts**
- **Decision**: Generated via frontend, not backend.
- **Reason**: More control over design + avoids server image handling.

### 7. **Country-Based Dynamic Forms**
- **Decision**: Frontend controls form fields based on selected country.
- **Reason**: Keeps backend schema clean and API consistent.

### 8. **Dark Mode + Brand Priority**
- **Decision**: Dark mode respects brand colors (forest green background, gold/white text).
- **Fallback**: If system theme conflicts with brand, brand wins.

### 9. **Single Admin Registration Entry Point**
- **Decision**: No public registration page. Only tech-admins create accounts.
- **Reason**: Security, internal tool model.

### 10. **Modular Django App Structure**
- **Apps**: `accounts`, `payments`, etc.
- **Reason**: Easier to maintain logic separation.

---

### Libraries & Tools
| Tool | Purpose | Why Chosen |
|------|---------|------------|
| Django | Backend Framework | Batteries-included, secure |
| DRF | API Layer | Easy serialization & permissions |
| SimpleJWT | Auth | JWT support with custom payloads |
| React + Vite | Frontend | Speed, flexibility |
| Tailwind CSS | Styling | Rapid theming, responsive design |
| Git Bash + PyCharm | Dev Tools | Stable and productive setup |

---

_This file is meant to be updated as more decisions are made._

