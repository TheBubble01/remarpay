# README – Frontend

## Overview

The RemarPay frontend is built using **React (with Vite)**, **TailwindCSS**, and **React Router**. It supports responsive layouts, dynamic role-based views, and full dark mode compatibility. The app is structured to function as a **Progressive Web App (PWA)** with clean component design and authentication via JWT.

---

## Tech Stack

- React 18+
- Vite (fast dev server and optimized build)
- TailwindCSS
- React Router DOM (v6)
- JWT (from backend)
- Zustand (or React Context) for global state

---

## Folder Structure

```bash
src/
├── assets/              # Logos, images
├── components/          # Shared UI components (Sidebar, Topbar, Forms, etc.)
├── pages/               # Route-level views (Dashboard, Login, NewRequest, etc.)
├── layout/              # App shell, sidebar layout
├── services/            # Axios config and API calls
├── store/               # Auth and global state (Zustand/Context)
├── utils/               # Theme handlers, date utils, helpers
├── App.jsx              # Root app routing
└── main.jsx             # Vite entry
```

---

## Setup Instructions

```bash
git clone https://github.com/your-org/remarpay-frontend.git
cd remarpay-frontend
npm install
npm run dev
```

For build:

```bash
npm run build
```

---

## PWA Support

- Manifest and service worker setup via Vite plugins
- Fully installable on desktop/mobile

---

## Authentication

- Login form sends credentials to backend `/api/token/`
- On success, stores `access` + `refresh` + user info
- Token auto-attached to all Axios requests
- Auto-logout on expiration (handled via interceptors)

---

## Responsive Design & Dark Mode

- Uses Tailwind responsive utilities (`md:`, `lg:`)
- Sidebar is **always collapsible**, even on desktop
- Dark mode auto-detected from device, but user can override manually
- Theme persists via `localStorage`

---

## Dev Tips

- Components follow atomic, reusable structure
- Always use `src/services/api.js` for backend calls
- Global state lives in `store/`
- Use `aria-*` attributes and semantic HTML where possible
- Testing JWT? Use browser DevTools → Application → Local Storage

