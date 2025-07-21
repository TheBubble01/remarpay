# PENDING-TASKS.md – RemarPay

## 🚧 HIGH PRIORITY

- [ ] **Client New Request Form**: Fully implement the form (frontend), submission logic (backend is ready), and response formatting for receipt.
- [ ] **Agent Payment Flow**: Next major feature after cashier flow is complete.
- [ ] **Dark Mode Toggle in User Settings**: Currently uses system preference only.
- [ ] **User Notification System**: Still needs full implementation.
- [ ] **Transaction Filtering/Search**: UI + Backend filtering logic.
- [ ] **Receipt Styling (Frontend)**: Beautiful downloadable slip based on returned backend data.

## 🔧 MEDIUM PRIORITY

- [ ] **Country Timezone Preference**: Allow user to pick preferred timezone for logs and display.
- [ ] **Manager Assignment Dashboard**: Assign agents to managers.
- [ ] **Profile Picture Upload**: Not implemented yet.
- [ ] **User Edit Flow (Tech-admin)**: Allow tech-admin to edit users.
- [ ] **Mobile Header UI Fixes**: Ensure topbar adapts better on small screens.

## 📝 LOW PRIORITY / STRETCH GOALS

- [ ] **Export to CSV** (future consideration)
- [ ] **Live Agent Status (Online/Offline)**
- [ ] **Theming System with Multiple Palettes**
- [ ] **Audit Logs per Action**

_Last updated: July 15, 2025_

Pending Tasks
✅ Implement New Request Form (Cashier) – UI is done; backend working; scroll + logo issues fixed

⏳ Dynamic payment fields by country – Ensure fields render conditionally based on selected destination (Nigeria, Niger, Cameroon)

⏳ Submit payment request to backend – Form needs to send correctly structured POST to /payments/request/

⏳ Success confirmation page / toast – Display confirmation + receipt preview after submission

⏳ Receipt Preview Styling (Frontend) – Render RemarPay-branded receipt with client + transaction details

⏳ Search/filter past requests (Cashier History) – Table layout; filters by date, country, status

⏳ Timezone and Country Preference – Add API + setting to save user’s preferred timezone and apply it to timestamps

⏳ Dark mode toggle in settings page – Currently device-based; allow manual override and store preference

⏳ Manager Approval Dashboard – Build interface for viewing and approving pending requests

⏳ Notification System – Show alerts for new requests, approvals, etc.

⏳ Final backend cleanup + documentation