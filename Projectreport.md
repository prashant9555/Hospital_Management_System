
**PROJECT REPORT**

**Hospital Management System**

*A Python & MySQL Based Console Application*

Submitted in partial fulfilment of the requirements for the

**Bachelor of Technology Degree**

Submitted by: Prashant

Roll No: 2501220100173

**SRM CEM Lucknow**

Department of Computer Science & Engineering

2026

Table of Contents

1\. Abstract

The Hospital Management System (HMS) is a console-based application built with Python and MySQL that digitizes core front-desk operations of a small hospital or clinic. It manages four central entities --- patients, doctors, appointments, and billing --- through a modular set of Python scripts, each exposing create, read, update, and delete (CRUD) operations against a normalized relational schema. A dedicated reporting module uses Matplotlib to render visual summaries such as patient demographics, doctor distribution by specialization, appointment status breakdown, and billing collections. The system emphasizes resilience: every module call is wrapped in a centralized error handler that logs the failure and automatically restarts the application, ensuring the front desk is never blocked by an unhandled exception. This report documents the motivation, feasibility, requirements, design, implementation, and testing of the system, along with its database schema, its current limitations, and possible directions for future enhancement.

2\. Acknowledgement

I would like to express my sincere gratitude to the Department of Computer Science & Engineering, SRM CEM Lucknow, for providing the opportunity, guidance, and resources needed to undertake this project. Building the Hospital Management System from the ground up --- from schema design through to a working, resilient console application --- has been a valuable exercise in translating a real-world workflow into a structured software solution, and in learning to anticipate and handle the failure modes that come with any data-driven application.

3\. Introduction

3.1 Background

Hospitals and clinics, particularly smaller ones, often rely on paper registers or disconnected spreadsheets to track patients, doctor schedules, appointments, and billing. This approach is error-prone, difficult to search, and provides no aggregate view of operations --- for instance, answering "how much revenue is still outstanding" requires manually totalling a ledger.

3.2 Problem with the Existing (Manual) System

A paper- or spreadsheet-based workflow has several concrete drawbacks that motivate this project. Records are duplicated across registers with no single source of truth, so a patient's phone number or a doctor's fee can drift out of sync between the file where it was first written and wherever it was copied. Cross-referencing is entirely manual --- linking a bill to the correct patient, or an appointment to the right doctor, depends on a human reading and matching names by eye. There is no running total of collections versus dues, so financial exposure is only visible after someone manually adds up a stack of receipts. And because none of this data lives in a queryable form, there is no way to generate even a simple chart of, say, appointment outcomes without re-entering everything into a spreadsheet by hand.

3.3 Proposed System

The Hospital Management System addresses this gap with a lightweight, dependency-minimal application that any front-desk operator can run from a terminal, backed by a proper relational database rather than flat files. It was designed as a learning project to demonstrate practical database-backed application development: schema design with foreign-key-style relationships, parameterized SQL queries from Python, modular program structure, defensive error handling, and basic data visualization --- all without the overhead of a web framework or GUI toolkit. Every entity a front desk actually touches --- a patient record, a doctor's profile, a booked appointment, an outstanding bill --- becomes a row in a table that can be searched, updated, and aggregated instantly.

4\. Objectives

-   Maintain accurate, centralized records for patients and doctors.

-   Allow appointments to be booked, tracked, and updated through a defined status lifecycle.

-   Track billing per patient, distinguishing paid from pending amounts, and summarize collections.

-   Provide at-a-glance visual reports for demographic, operational, and financial data.

-   Ensure the application degrades gracefully on bad input or database errors instead of crashing outright.

-   Keep the codebase simple enough to be understood, extended, and taught to other students.

5\. Feasibility Study

5.1 Technical Feasibility

The system is built entirely on freely available, well-documented technology: Python 3, MySQL Server, and the mysql-connector-python and Matplotlib libraries. All of these run comfortably on a standard desktop or laptop, install with a single pip command, and are cross-platform, so there is no specialized hardware or proprietary tooling required to build, run, or extend the project.

5.2 Operational Feasibility

Because the interface is a numbered text menu with clearly labeled prompts, an operator with basic computer literacy can learn the system in minutes without formal training. The auto-restart behavior on error further reduces the operational burden, since a mistaken entry does not require anyone to know how to relaunch the program manually.

5.3 Economic Feasibility

Every component of the stack is open source and free to use, so the only real cost is development time. This makes the system economically viable even for a small clinic with no dedicated IT budget, and it avoids the recurring licensing fees associated with many commercial hospital management products.

6\. System Requirements

6.1 Hardware Requirements

-   Processor: Intel i3 / equivalent or higher

-   RAM: 4 GB minimum (8 GB recommended)

-   Storage: 200 MB free disk space

6.2 Software Requirements

-   Operating System: Windows / Linux / macOS

-   Python 3.8 or later

-   MySQL Server 8.0 or later

-   Python packages: mysql-connector-python, matplotlib

-   A terminal / command-line interface

7\. System Design

7.1 Architecture Overview

The application follows a modular, function-based architecture rather than an object-oriented or MVC pattern, which keeps the codebase approachable for a student project. Each domain entity --- patients, doctors, appointments, billing --- is implemented as an independent Python module with its own private database connection helper (\_connect()) and a menu() loop that exposes its features. A single entry point, mainmenu.py, imports every module and dispatches to the appropriate one based on numeric user input, wrapping each call in a shared safe_call() error boundary.

This design mirrors a simple layered architecture: mainmenu.py acts as the presentation/dispatch layer, each domain module acts as both business logic and data-access layer (queries are embedded directly in the module rather than behind a separate repository layer), and MySQL serves as the persistence layer. graphs.py sits alongside the domain modules as a read-only reporting layer that queries aggregated data and renders it with Matplotlib.

7.2 Data Flow

At the highest level, the system has a single external entity --- the front-desk Operator --- interacting with one central process, and four data stores it reads from and writes to:

+\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--+\
Operator \-\-\--\> \| Hospital Management \| \-\-\--\> Console Output\
(menu choice, \| System (mainmenu.py) \| (tables, charts,\
form input) +\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--+ confirmations)\
\| \| \| \|\
v v v v\
patients doctors appts billing\
(DB) (DB) (DB) (DB)

At the next level of detail, the single process decomposes into the five module-level processes described in Section 7.4 --- Patients, Doctors, Appointments, Billing, and Graphs/Reports --- each of which reads and/or writes its own table, with Appointments and Graphs additionally reading across tables (Appointments joins patients and doctors; Graphs aggregates from all four).

7.3 Error Handling & Resilience

A recurring risk in console applications is that any unhandled exception --- a malformed date, a duplicate primary key, a lost database connection --- terminates the whole program. The HMS addresses this with two cooperating functions in mainmenu.py:

def safe_call(func):\
try:\
func()\
except Exception as e:\
print(f"\[ERROR\] {type(e).\_\_name\_\_}: {e}")\
restart_program()\
\
def restart_program():\
time.sleep(3)\
os.execl(sys.executable, sys.executable, \*sys.argv)

safe_call() wraps every module invocation from the main menu. On failure it reports the exception type and message to the operator, then restart_program() uses os.execl() to relaunch the same Python process cleanly --- the running process image is replaced in place, so the application returns to a known-good state without residual corrupted state in memory. A short delay gives the operator time to read the error before the screen resets.

7.4 Module Responsibilities

  ------------------- ---------------------------------------------------------------------------------
  **Module**          **Responsibility**

  mainmenu.py         Top-level menu, dispatch, and centralized error handling / auto-restart.

  blank_table.py      One-shot bootstrap: creates the hospital_2026 database and all four tables.

  patients.py         Patient CRUD: add, view, search by ID, update phone/address, delete.

  doctors.py          Doctor CRUD plus specialization search using a LIKE query.

  appointments.py     Books appointments, joins patient and doctor names for display, updates status.

  billing.py          Creates bills, marks them paid, lists pending dues, summarizes collections.

  graphs.py           Matplotlib visualizations built from GROUP BY aggregate queries.
  ------------------- ---------------------------------------------------------------------------------

8\. Database Design

The schema uses four tables joined by plain integer identifiers (patient_id, doctor_id) rather than declared foreign key constraints, which is a deliberate simplification appropriate for a student-scale project. The database is named hospital_2026 and is created idempotently via CREATE TABLE IF NOT EXISTS statements in blank_table.py.

8.1 patients

  ----------------- ----------------- ------------------------------------
  **Column**        **Type**          **Description**

  patient_id        INT (PK)          Unique patient identifier

  name              VARCHAR           Patient full name

  age               INT               Patient age

  gender            CHAR              M / F / O

  phone             VARCHAR           Contact number

  address           VARCHAR           Residential address

  blood_group       VARCHAR           e.g. O+, A-

  admit_date        DATE              Date of admission
  ----------------- ----------------- ------------------------------------

8.2 doctors

  ----------------- ----------------- ------------------------------------
  **Column**        **Type**          **Description**

  doctor_id         INT (PK)          Unique doctor identifier

  name              VARCHAR           Doctor full name

  specialization    VARCHAR           Medical specialty

  phone             VARCHAR           Contact number

  fees              DECIMAL           Consultation fee
  ----------------- ----------------- ------------------------------------

8.3 appointments

  ----------------- ----------------- ------------------------------------
  **Column**        **Type**          **Description**

  appt_id           INT (PK)          Unique appointment identifier

  patient_id        INT               References patients.patient_id

  doctor_id         INT               References doctors.doctor_id

  appt_date         DATE              Scheduled date

  status            VARCHAR           Scheduled / Completed / Cancelled
  ----------------- ----------------- ------------------------------------

8.4 billing

  ----------------- ----------------- ------------------------------------
  **Column**        **Type**          **Description**

  bill_id           INT (PK)          Unique bill identifier

  patient_id        INT               References patients.patient_id

  amount            DECIMAL           Bill amount

  bill_date         DATE              Date billed

  status            VARCHAR           Paid / Pending
  ----------------- ----------------- ------------------------------------

8.5 Entity Relationships

Conceptually, a patient can have many appointments and many bills (one-to-many in both cases), and a doctor can likewise be linked to many appointments (one-to-many). No patient or doctor row is ever owned by more than one such parent, so the relationships are strictly one-to-many rather than many-to-many. These relationships are not enforced by declared FOREIGN KEY constraints in the current schema --- patient_id and doctor_id in the appointments and billing tables are plain INT columns --- so referential integrity (e.g. preventing a bill for a patient_id that does not exist) is currently the application's responsibility rather than the database's. This trade-off is discussed further in Section 11.2 (Limitations).

9\. Implementation Details

9.1 Technology Stack

-   Language: Python 3

-   Database: MySQL, accessed via mysql-connector-python

-   Visualization: Matplotlib (pie and bar charts)

-   Interface: Command-line (text menus, input() prompts)

9.2 Database Bootstrap (blank_table.py)

blank_table.py is a one-shot script that provisions the entire schema before first use. It connects to the local MySQL server, creates the hospital_2026 database if absent, and issues four CREATE TABLE IF NOT EXISTS statements --- one per entity --- so the script can be safely re-run without erroring on tables that already exist:

def create_database_and_tables():\
con = sql.connect(host="localhost", user="root", passwd="\<your_mysql_password\>")\
cur = con.cursor()\
cur.execute("CREATE DATABASE IF NOT EXISTS hospital_2026")\
cur.execute("USE hospital_2026")\
\
cur.execute("""CREATE TABLE IF NOT EXISTS patients (\
patient_id INT PRIMARY KEY,\
name VARCHAR(60) NOT NULL,\
age INT,\
gender VARCHAR(10),\
phone VARCHAR(15),\
address VARCHAR(120),\
blood_group VARCHAR(5),\
admit_date DATE\
)""")\
\# doctors, appointments, and billing tables follow the same pattern\
\
con.commit()\
print("Database \`hospital_2026\` and all tables created successfully.")

Note: the MySQL credentials in \_connect() are hardcoded per module in the source repository, which is acceptable for a local student demo but should never be committed as plain text in a real deployment --- see Section 12 (Future Scope) for a recommended fix (environment variables or a config file excluded from version control).

9.3 Patient Module

patients.py implements standard CRUD operations. Records are added with an explicit patient_id supplied by the operator rather than an auto-increment key, keeping the schema simple for classroom use. Updates are intentionally narrow in scope --- only phone and address can be changed --- reflecting the reasoning documented in the project's own design notes that these are the fields most likely to change day to day, while identity fields (name, age, blood group) are treated as fixed at admission.

9.4 Doctor Module

doctors.py mirrors the patient module's CRUD shape and adds a specialization search using a SQL LIKE '%...%' query, since looking up all doctors in a given specialty (e.g. "which cardiologists do we have?") is described as the most common lookup a front desk performs on doctor records.

9.5 Appointments Module

Booking an appointment inserts a row with status defaulted to Scheduled, linking an existing patient_id and doctor_id. Listing appointments performs a JOIN across patients and doctors so the operator sees names rather than raw numeric IDs. Status transitions (to Completed or Cancelled) are applied through a dedicated update function, and appointments can be filtered by doctor to review a single doctor's schedule.

9.6 Billing Module

billing.py creates bills tied to a patient with a status of Paid or Pending. Two reporting functions built into the module give the front desk quick financial visibility: pending_bills() lists every unpaid bill and sums the total outstanding exposure, while collection_summary() groups all bills by status to compare total collected revenue against total receivables.

9.7 Reporting Module

graphs.py performs no new data collection; it issues GROUP BY aggregate queries against the existing tables and renders the results with Matplotlib: a pie chart of patients by gender, a bar chart of doctors by specialization, a pie chart of appointment status distribution, and a bar chart contrasting paid versus pending billing totals in green and red respectively.

9.8 Sample Data

seed_data.sql populates the schema with 100 patients spanning ages 1 to 85 with mixed gender and blood group, 10 doctors covering 10 distinct specializations, 40 appointments in mixed statuses (Scheduled / Completed / Cancelled), and 50 bills split roughly two-to-one between Paid and Pending so that the collection summary chart is meaningful rather than trivial. The seeded doctor roster, which anchors the specialization search and the doctors-by-specialization chart, is as follows:

  -------------------- -------------------- ---------------- ----------------
  **Name**             **Specialization**   **Phone**        **Fees (Rs.)**

  Dr. Ramesh Sharma    Cardiology           9696865256       300

  Dr. Anita Verma      Neurology            9442832606       400

  Dr. Vikram Singh     Orthopedics          9495464842       500

  Dr. Priya Gupta      Pediatrics           9969042008       800

  Dr. Suresh Yadav     Dermatology          9317048149       300

  Dr. Neha Mishra      General              9904938723       600

  Dr. Rajesh Tiwari    ENT                  9511069044       600

  Dr. Kavita Pandey    Gynecology           9900840190       800

  Dr. Amit Shukla      Oncology             9325491082       600

  Dr. Sunita Agarwal   Psychiatry           9390167827       500
  -------------------- -------------------- ---------------- ----------------

10\. Sample Output

The application is entirely console-driven. A representative session looks as follows:

========= HOSPITAL MANAGEMENT SYSTEM =========\
1. Patients\
2. Doctors\
3. Appointments\
4. Billing\
5. Graphs / Reports\
6. Exit\
Enter choice: 4\
\
\-\-- Collection Summary \-\--\
Paid: Rs.180000\
Pending: Rs.45000

If an operator enters invalid data --- for example, a non-numeric appointment ID --- the safe_call() handler intercepts the exception, reports its type and message, and the program automatically restarts after a short delay rather than crashing to the terminal prompt.

11\. Testing

11.1 Test Cases

Testing was carried out manually against the seeded dataset, covering the following categories:

  --------------------- ------------------------------------------------ ----------------------------------------------------
  **Test Area**         **Scenario**                                     **Expected Result**

  Patient CRUD          Add, search, update, delete a patient            Record correctly reflected in all subsequent views

  Doctor search         Partial specialization match (e.g. "Cardio")   All matching doctors returned via LIKE query

  Appointment booking   Book with valid patient/doctor IDs               Row inserted with status Scheduled

  Appointment booking   Book with a non-existent patient/doctor ID       Error caught by safe_call, program restarts

  Appointment status    Update status to Completed / Cancelled           Status reflected in appointments-by-doctor view

  Billing               Mark a pending bill as paid                      Status updates; reflected in collection summary

  Billing               List pending bills                               Total outstanding dues sums correctly

  Invalid menu input    Non-numeric main menu choice                     Rejected via str.isdigit() check, re-prompted

  Invalid menu input    Out-of-range numeric choice (e.g. 9)             "Invalid choice" message, menu re-displayed

  Graphs                Generate each of the four charts                 Matplotlib window opens with correct proportions

  Bootstrap             Re-run blank_table.py on an existing database    No error; existing tables left untouched
  --------------------- ------------------------------------------------ ----------------------------------------------------

11.2 Limitations

The current implementation has known limitations, mostly stemming from choices made to keep it approachable as a learning project rather than production software:

-   No authentication or role-based access --- any operator with terminal access has full read/write control over every table.

-   No declared foreign key constraints, so the database itself will not reject an appointment or bill referencing a non-existent patient or doctor.

-   Database credentials are hardcoded in each module's \_connect() function rather than loaded from an environment variable or secrets file.

-   No automated unit or integration tests --- all verification described in Section 11.1 was performed manually.

-   Console-only interface, which is fast for a trained operator but is not accessible to non-technical staff the way a graphical or web interface would be.

12\. Conclusion and Future Scope

The Hospital Management System meets its stated objectives: it replaces manual record-keeping with a structured relational database, exposes that data through simple, reliable CRUD workflows, and gives the front desk immediate financial and operational visibility through both tabular summaries and charts. Its centralized error-handling strategy makes it noticeably more robust than a naive script-based approach, since a single bad input cannot bring the whole application down.

As a foundation, the system leaves clear room for growth. A graphical or web-based front end (for example, built with Tkinter or a lightweight web framework) would make the tool accessible to non-technical staff. Introducing proper foreign-key constraints and transactions would strengthen data integrity across the patient, appointment, and billing tables. Authentication and role-based access would be necessary before any real deployment, since the current version assumes a single trusted operator. Moving database credentials out of source code and into environment variables or a gitignored config file would close an immediate security gap. Finally, exporting reports to PDF, adding date-range filtering to the graphing module, and introducing an automated test suite would extend both the usefulness and the reliability of the system for periodic hospital administration reviews.

13\. Development Process

The project's own design notes (StepToCreate.md) lay out a deliberate, bottom-up build order --- schema first, then data-owning modules, then transactional modules, then reporting, then the glue code that ties everything together, and finally documentation. This sequencing means each step only ever depends on pieces that already exist and have been verified, rather than on code still to be written:

  ---------- --------------------------------------- -------------------------------------------------------------------------------
  **Step**   **Artifact**                            **Purpose**

  1          blank_table.py                          Establish the schema before any module needs it.

  2          patients.py, doctors.py                 Build the two base entities with no dependencies on other tables.

  3          appointments.py, billing.py             Build transactional entities that reference the base entities.

  4          graphs.py                               Add reporting once there is data across all four tables to visualize.

  5          mainmenu.py                             Wire every module together behind a single dispatch loop with error handling.

  6          seed_data.sql                           Generate reproducible sample data to exercise every module and chart.

  7          README.md, StepToCreate.md, Output.md   Document install/run steps, design reasoning, and sample output.
  ---------- --------------------------------------- -------------------------------------------------------------------------------

Following this order in practice meant every module could be run and manually tested in isolation the moment it was written, well before mainmenu.py existed to tie the application together --- which kept debugging localized to one file at a time.

14\. Glossary

  ----------------------- -----------------------------------------------------------------------------------------------------------------
  **Term**                **Meaning**

  CRUD                    Create, Read, Update, Delete --- the four basic data operations a module exposes.

  PK                      Primary Key --- the column that uniquely identifies each row in a table.

  DFD                     Data Flow Diagram --- a diagram showing how data moves between processes and stores.

  Idempotent              An operation that produces the same result no matter how many times it is run, e.g. CREATE TABLE IF NOT EXISTS.

  JOIN                    A SQL operation that combines rows from two tables based on a related column, e.g. patient_id.

  GROUP BY                A SQL clause that aggregates rows sharing a column value, used by graphs.py to build chart data.

  safe_call()             The project's error boundary function that catches exceptions from any module and triggers a restart.

  Referential integrity   The guarantee that a foreign-key-style reference (e.g. patient_id) always points to a row that actually exists.
  ----------------------- -----------------------------------------------------------------------------------------------------------------

15\. References

\[1\] MySQL 8.0 Reference Manual --- https://dev.mysql.com/doc/

\[2\] mysql-connector-python Documentation --- https://dev.mysql.com/doc/connector-python/en/

\[3\] Matplotlib Documentation --- https://matplotlib.org/stable/contents.html

\[4\] Python 3 Official Documentation --- https://docs.python.org/3/

\[5\] Project source: README.md, StepToCreate.md, Output.md, seed_data.sql (this repository)
Hospital_Management_System_Project_Report_Updated-2.md
Suggestions updatedDisplaying Hospital_Management_System_Project_Report_Updated-2.md.