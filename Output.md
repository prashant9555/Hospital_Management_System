# Output.md — Function reference with sample outputs

Sample outputs below assume the database has been seeded from `seed_data.sql`.

---

## `mainmenu.py`

### `mainmenu()`
Displays the top-level menu.
```
========= HOSPITAL MANAGEMENT SYSTEM =========
1. Patients
2. Doctors
3. Appointments
4. Billing
5. Graphs / Reports
6. Exit
Enter choice:
```

### `safe_call(func)`
Runs a module menu inside a try/except. On error:
```
[ERROR] ValueError: invalid literal for int() with base 10: 'abc'
Reason: The module could not complete due to the error above.

Restarting the program in 3 seconds...
```

### `restart_program()`
Uses `os.execl` to relaunch the app cleanly.

---

## `blank_table.py`

### `create_database_and_tables()`
Creates the `hospital_2026` database and all four tables.
```
Database `hospital_2026` and all tables created successfully.
```

---

## `patients.py`

### `add_patient()`
Prompts for and inserts a new patient.
```
Patient ID: 101
Name: Rahul Sharma
Age: 34
Gender (M/F/O): M
Phone: 9876543210
Address: Lucknow
Blood Group: B+
Admit Date (YYYY-MM-DD): 2026-05-14
Patient added successfully.
```

### `view_patients()`
Lists all patients.
```
ID   Name                     Age  Gender  Phone          Blood  Admitted
--------------------------------------------------------------------------------
1    Aarav Sharma             27   M       9123456789     O+     2026-03-11
2    Diya Verma               45   F       9234567890     A+     2026-07-22
...
```

### `search_patient()`
Looks up a patient by ID.
```
Enter Patient ID to search: 1
ID: 1
Name: Aarav Sharma
Age: 27
Gender: M
Phone: 9123456789
Address: Lucknow
Blood: O+
Admitted: 2026-03-11
```

### `update_patient()`
Updates phone/address by patient ID.
```
Patient ID to update: 1
New Phone: 9999999999
New Address: Kanpur
Patient updated.
```

### `delete_patient()`
Removes a patient.
```
Patient ID to delete: 1
Patient deleted.
```

---

## `doctors.py`

### `add_doctor()`
```
Doctor ID: 11
Name: Dr. Rakesh Nair
Specialization: Cardiology
Phone: 9812345670
Consultation Fees: 800
Doctor added successfully.
```

### `view_doctors()`
```
ID   Name                     Specialization      Phone          Fees
---------------------------------------------------------------------------
1    Dr. Ramesh Sharma        Cardiology          9812345671     800
2    Dr. Anita Verma          Neurology           9812345672     1000
...
```

### `search_by_specialization()`
```
Specialization to search: Cardio
1 | Dr. Ramesh Sharma | Cardiology | Fees: Rs.800
```

### `update_doctor()`
Updates the doctor's consultation fees.
```
Doctor ID to update: 1
New Fees: 900
Doctor updated.
```

### `delete_doctor()`
```
Doctor ID to delete: 11
Doctor deleted.
```

---

## `appointments.py`

### `book_appointment()`
```
Appointment ID: 41
Patient ID: 5
Doctor ID: 2
Appointment Date (YYYY-MM-DD): 2026-08-01
Appointment booked successfully.
```

### `view_appointments()`
```
AID  Patient                  Doctor                   Date        Status
--------------------------------------------------------------------------------
1    Aarav Sharma             Dr. Anita Verma          2026-01-15  Scheduled
2    Diya Verma               Dr. Vikram Singh         2026-02-03  Completed
...
```

### `update_status()`
```
Appointment ID: 1
New Status (Scheduled/Completed/Cancelled): Completed
Status updated.
```

### `appointments_by_doctor()`
```
Doctor ID: 1
AID 5 | Patient: Aarav Sharma | Date: 2026-04-11 | Scheduled
AID 18 | Patient: Meera Yadav | Date: 2026-06-02 | Completed
```

---

## `billing.py`

### `add_bill()`
```
Bill ID: 51
Patient ID: 7
Amount: 2500
Bill Date (YYYY-MM-DD): 2026-05-20
Status (Paid/Pending): Pending
Bill added.
```

### `view_bills()`
```
BID  Patient                  Amount    Date        Status
----------------------------------------------------------------------
1    Aarav Sharma             1500      2026-01-10  Paid
2    Diya Verma               3000      2026-02-14  Pending
...
```

### `pending_bills()`
```
BID 2 | Diya Verma | Rs.3000 | 2026-02-14
BID 7 | Ishaan Singh | Rs.2000 | 2026-03-22
Total Pending: Rs.5000
```

### `mark_paid()`
```
Bill ID to mark Paid: 2
Bill marked as Paid.
```

### `collection_summary()`
```
--- Collection Summary ---
Paid: Rs.180000
Pending: Rs.45000
```

---

## `graphs.py`

### `patients_by_gender()`
Opens a pie chart with slices for M / F (and O if present), e.g. `M: 54.0% | F: 46.0%`.

### `doctors_by_specialization()`
Opens a bar chart, one bar per specialization (Cardiology, Neurology, Orthopedics, …) — each height = 1 for the seeded data.

### `appointment_status_chart()`
Opens a pie chart of Scheduled / Completed / Cancelled proportions.

### `billing_status_chart()`
Opens a bar chart comparing total `Paid` (green) vs `Pending` (red) amounts in rupees.

---

_Created for SRM CEM Lucknow._
