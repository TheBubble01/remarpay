# DEV-BRAIN.md – RemarPay

A chronological log of all major backend and frontend development milestones, issues solved, and implementation approaches.

---

## Backend Timeline

### ✅ June 25, 2025 – Project Foundation
- Project created: `remarpay/`
- Setup of custom `User` model using `AbstractBaseUser`
- Email used as `USERNAME_FIELD`
- JWT login integrated with custom serializer
- Roles added: `cashier`, `agent`, `manager`, `tech-admin`

### ✅ June 26, 2025 – Authentication and User Management
- Register, login, profile, suspend/unsuspend, password change endpoints
- Added role-based access control per view
- Suspended users blocked from accessing any route

### ✅ June 28, 2025 – Payment Flow Begins
- `PaymentRequest` model created
- Country-based dynamic receiver fields supported (Nigeria, Niger, Cameroon)
- Receipt generation will happen frontend-side only, backend provides all necessary data

### ✅ July 1, 2025 – Timezone & Dark Mode Preferences
- Per-user timezone/country preferences saved
- Dark mode preference stored per user (if customized)

### ✅ July 5–7, 2025 – Manager Assignment Flow
- Chief Manager can assign agents to cashiers
- All permissions role-gated with DRY logic

### ✅ July 10, 2025 – Frontend Prep & Clean API Design
- API cleaned and versioned (`/api/v1/`)
- Clear separation of auth, accounts, payments, and utilities

---

## Frontend Timeline

### ✅ July 2, 2025 – Frontend Bootstrapped
- React + Vite + TailwindCSS initialized
- PWA-ready with manifest.json and icons
- Login UI implemented with dark mode support

### ✅ July 10–12, 2025 – Full Auth Flow
- Token saved in `localStorage`
- Login UI has floating error states, animations, and accessibility
- JWT decoded to extract name, role

### ✅ July 13, 2025 – Sidebar and Layout
- Sidebar built with Lucide icons
- Sidebar auto-collapses on small screens
- Toggle works across devices
- Top bar displays user name, logout

### ✅ July 15, 2025 – Payment Request Form Begins
- `/new-request` route renders correctly
- Dynamic country-based forms implemented
- Responsiveness refined for both desktop and mobile
- Sidebar is now toggleable even on desktop
- Top bar includes logo

---

### Other Notables
- All frontend code fully respects Tailwind dark mode classes
- Developer tips, CLI commands, and environment setup handled via notes in `DEVELOPER-NOTES.md`

_Last updated: July 15, 2025_

