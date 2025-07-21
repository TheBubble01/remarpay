# ASSUMPTIONS.md – RemarPay

## General
- All users are created **manually** by tech-admins. No public signup.
- Only **cashiers** can initiate client requests.
- Each request involves a **client** and a **receiver** (based on country).

## Role Behaviors
- **Suspension** message is shown to suspended users (to be styled later on frontend).
- Only **tech-admin** and **chief manager** can suspend users.
- JWT token includes: `name`, `role`, `user_id` → used for role-based frontend rendering.

## Receipts
- Receipts are **generated on frontend**, not backend.
- Backend just returns formatted request data.
- Receipt includes: cashier name, date/time, request details, receiver info, destination country, amount, RemarPay branding.

## Conditional Fees
- If client sends **< 500 Dinar**, a **5 Dinar fee** is subtracted automatically.
- Logic handled during payment request creation.

## Country-specific Fields
- **Nigeria**:
  - Bank Name
  - Account Number
  - Account Name
  - Depositor Name
  - Depositor Phone

- **Niger/Cameroon**:
  - Receiver Full Name
  - Receiver Phone Number
  - NITA Office
  - Depositor Name
  - Depositor Phone

## Frontend
- Fully responsive.
- Dark mode based on device preference (for now).
- Sidebar + topbar layout across all pages.
- Mobile-first design assumptions.

_Last updated: July 15, 2025_

