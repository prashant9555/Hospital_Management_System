# StepToCreate.md — Logic behind the Hospital Management System

This document explains the reasoning and creation order behind every file in the project. Follow the steps top-to-bottom to build a similar system from scratch.

## Step 1 — Identify the domain entities

A hospital's day-to-day operations revolve around four core entities:

1. **Patients** — people receiving care
2. **Doctors** — service providers, grouped by specialization
3. **Appointments** — the link between a patient and a doctor on a given date
4. **Billing** — the money side: what the patient owes, what is collected

Everything else (reports, graphs, dashboards) is derived from these four.

## Step 2 — Design the database schema

Each entity becomes a table. Foreign-key-style columns (`patient_id`, `doctor_id`) are used to join across tables — kept as plain `INT` for simplicity in a student project.

- `patients(patient_id PK, name, age, gender, phone, address, blood_group, admit_date)`
- `doctors(doctor_id PK, name, specialization, phone, fees)`
- `appointments(appt_id PK, patient_id, doctor_id, appt_date, status)`
- `billing(bill_id PK, patient_id, amount, bill_date, status)`

## Step 3 — Create `blank_table.py`

A one-shot bootstrap script. It:

- Connects to MySQL as `root`
- Creates the `hospital_2026` database if it does not exist
- Creates all four tables with `CREATE TABLE IF NOT EXISTS`

Why programmatic: a new user can spin up the whole schema by running one Python file — no manual SQL required.

## Step 4 — Build each functional module

Each module has the same shape:

- A private `_connect()` helper returning a MySQL connection to `hospital_2026`
- Feature functions (add / view / search / update / delete)
- A `menu()` function that offers those features in a loop

### `patients.py`
Standard CRUD. Search is by primary key. Update focuses on phone/address because those change most often.

### `doctors.py`
CRUD plus a **specialization search** using `LIKE '%…%'` — a hospital's most common query is "which cardiologists do we have?"

### `appointments.py`
Booking creates a row with status `Scheduled`. A JOIN across `patients` and `doctors` produces a human-readable list. Status can be moved to `Completed` or `Cancelled`.

### `billing.py`
Bills default to `Paid` or `Pending`. Business rules:
- **Pending list** sums all outstanding dues so the front desk sees total exposure at a glance
- **Collection summary** groups by status to compare income vs receivables

### `graphs.py`
Matplotlib charts derived directly from `GROUP BY` queries. No new data — just visualization.

## Step 5 — Wire up `mainmenu.py`

The main menu imports all module files and dispatches based on the user's numeric choice. Two features make it robust:

- **`safe_call(func)`** — wraps any module call. If the module raises, it prints the error class and message, then calls `restart_program()`.
- **`restart_program()`** — uses `os.execl(sys.executable, sys.executable, *sys.argv)` to relaunch the same script cleanly, after a 3-second delay so the user can read the error.

Non-numeric input is caught with `str.isdigit()` before conversion.

## Step 6 — Seed data (`seed_data.sql`)

Reproducible sample data drives the demo:
- 100 patients with realistic Indian names, mixed genders, ages 1–85
- 10 doctors, one per specialization
- ~40 appointments in mixed statuses
- ~50 bills with a 2:1 Paid:Pending ratio to make the summary meaningful

## Step 7 — Documentation

- **`README.md`** — install + run instructions and feature list
- **`StepToCreate.md`** — this file (the "why")
- **`Output.md`** — what each function does and a sample output

## Recommended creation order

1. `blank_table.py` (schema)
2. `patients.py`, `doctors.py` (base data)
3. `appointments.py`, `billing.py` (transactional data)
4. `graphs.py` (reporting)
5. `mainmenu.py` (glue + error handling)
6. `seed_data.sql`
7. Docs (`README`, `StepToCreate`, `Output`)

---

_Created for SRM CEM Lucknow._
