# Hospital Management System

A Python + MySQL based Hospital Management System built with a modular architecture. Handles patients, doctors, appointments, billing, and visual reports — with graceful error handling and auto-restart in the main menu.

## Features

1. **Patients** — Register, view, search, update, and delete patient records (with age, gender, phone, address, blood group, admit date).
2. **Doctors** — Manage doctors with specialization, phone, and consultation fees. Search doctors by specialization.
3. **Appointments** — Book appointments linking a patient to a doctor, update appointment status (Scheduled / Completed / Cancelled), and list appointments per doctor.
4. **Billing** — Create bills, mark them Paid, list pending bills with total dues, and view a Paid vs Pending collection summary.
5. **Graphs / Reports** — Matplotlib-powered charts:
   - Patients by gender (pie)
   - Doctors by specialization (bar)
   - Appointment status distribution (pie)
   - Billing paid vs pending (bar)
6. **Error handling & auto-restart** — Every module call is wrapped in `safe_call`. On error, the program prints the error type and reason, then automatically restarts after 3 seconds.

## Project Structure

```
hospital_management_system/
├── mainmenu.py        # Central menu with error handling & auto-restart
├── blank_table.py     # Creates the hospital_2026 DB and all tables
├── patients.py        # Patient CRUD
├── doctors.py         # Doctor CRUD + specialization search
├── appointments.py    # Appointment booking & tracking
├── billing.py         # Bills, payments, collection summary
├── graphs.py          # Matplotlib visualizations
├── seed_data.sql      # 100 patients, 10 doctors, ~40 appts, ~50 bills
├── README.md
├── StepToCreate.md
└── Output.md
```

## Database Schema

Database: **`hospital_2026`**

| Table | Columns |
|-------|---------|
| `patients` | patient_id, name, age, gender, phone, address, blood_group, admit_date |
| `doctors` | doctor_id, name, specialization, phone, fees |
| `appointments` | appt_id, patient_id, doctor_id, appt_date, status |
| `billing` | bill_id, patient_id, amount, bill_date, status |

## Setup

1. Install MySQL Server and set the root password to `root` (or edit the `_connect()` calls in each module).
2. Install Python dependencies:
   ```sh
   pip install mysql-connector-python matplotlib
   ```
3. Create the database and tables:
   ```sh
   python blank_table.py
   ```
4. Load the seed data:
   ```sh
   mysql -u root -p hospital_2026 < seed_data.sql
   ```
5. Run the application:
   ```sh
   python mainmenu.py
   ```

## Sample Data

- **100 patients** with varied age, gender, blood group, and admit date
- **10 doctors** across 10 specializations
- **~40 appointments** with mixed statuses
- **~50 bills** with Paid / Pending status

## Notes

- Change MySQL credentials by editing the `_connect()` function in each module.
- If a module errors out (invalid input, missing record, DB issue), the main menu will explain the reason and restart automatically.

---

_Created for SRM CEM Lucknow._
