# PREFERENCES.md – RemarPay

## Code Style & Formatting

### Backend (Python)
- Use 4 spaces per indentation
- Snake_case for variable and function names
- PascalCase for class names
- Consistent use of docstrings on all class-based views and serializers
- Comments should clarify _why_, not just _what_

### Frontend (JavaScript/JSX)
- Use arrow functions (`const Component = () => {}`)
- Always destructure props
- Use `camelCase` for variable and function names
- Use `PascalCase` for React components
- Avoid inline styles, prefer Tailwind classes

## Component Structure
- One file per component (`ComponentName.jsx`)
- Each page lives under `src/pages/`
- Shared components go under `src/components/`
- Custom hooks go under `src/hooks/`
- Layout components under `src/layout/`
- Context providers under `src/context/`

## Naming Conventions
- All user-facing routes are lowercase, dash-separated (e.g., `/new-request`, `/profile`)
- Backend URL patterns are prefixed clearly (e.g., `/api/v1/accounts/`, `/api/v1/payments/`)
- Boolean fields: prefix with `is_` or `has_` (e.g., `is_active`, `has_receipt`)
- React state variables: `const [isOpen, setIsOpen] = useState(false)`

## Dev Tools & Setup
- Preferred editor: **PyCharm (backend)**, **VS Code or WebStorm (frontend)**
- Terminal: **Git Bash** on Windows
- Python version: `3.11.x`
- Node.js version: `18.x`
- Package manager: `npm` for now (can switch to `pnpm` later)

## General Practices
- Comment all logic-heavy blocks
- Use `.env` files for sensitive settings
- Use commit messages in the format: `feat:`, `fix:`, `chore:`
- Regularly update documentation (`README.md`, etc.) when major changes are made

## UI/UX Preferences
- No permanently open sidebar (even on desktop)
- Always use collapsible/toggleable navigation
- Primary brand color: **Forest Green (#014421)**
- Accent color: **Gold (#FFD700)**
- Prefer centered forms for auth/login
- All views should scroll on overflow
- Dark mode is always respected, even if system theme is light

---

_Last updated: July 15, 2025_

