"""appointments.py — Appointment booking, viewing, and status updates."""

import mysql.connector as sql


def _connect():
    return sql.connect(host="localhost", user="root", passwd="Pras9555", database="hospital_2026")


def book_appointment():
    con = _connect()
    cur = con.cursor()
    aid = int(input("Appointment ID: "))
    pid = int(input("Patient ID: "))
    did = int(input("Doctor ID: "))
    date = input("Appointment Date (YYYY-MM-DD): ")
    cur.execute("INSERT INTO appointments VALUES (%s,%s,%s,%s,%s)",
                (aid, pid, did, date, "Scheduled"))
    con.commit()
    print("Appointment booked successfully.")
    con.close()


def view_appointments():
    con = _connect()
    cur = con.cursor()
    cur.execute("""
        SELECT a.appt_id, p.name, d.name, a.appt_date, a.status
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors  d ON a.doctor_id  = d.doctor_id
        ORDER BY a.appt_date
    """)
    rows = cur.fetchall()
    print(f"{'AID':<5}{'Patient':<25}{'Doctor':<25}{'Date':<12}{'Status'}")
    print("-" * 80)
    for r in rows:
        print(f"{r[0]:<5}{r[1]:<25}{r[2]:<25}{str(r[3]):<12}{r[4]}")
    con.close()


def update_status():
    con = _connect()
    cur = con.cursor()
    aid = int(input("Appointment ID: "))
    status = input("New Status (Scheduled/Completed/Cancelled): ")
    cur.execute("UPDATE appointments SET status=%s WHERE appt_id=%s", (status, aid))
    con.commit()
    print("Status updated." if cur.rowcount else "Appointment not found.")
    con.close()


def appointments_by_doctor():
    con = _connect()
    cur = con.cursor()
    did = int(input("Doctor ID: "))
    cur.execute("""
        SELECT a.appt_id, p.name, a.appt_date, a.status
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        WHERE a.doctor_id = %s
    """, (did,))
    rows = cur.fetchall()
    if not rows:
        print("No appointments for this doctor.")
    for r in rows:
        print(f"AID {r[0]} | Patient: {r[1]} | Date: {r[2]} | {r[3]}")
    con.close()


def menu():
    while True:
        print("\n--- APPOINTMENTS ---")
        print("1. Book Appointment")
        print("2. View All Appointments")
        print("3. Update Status")
        print("4. View Appointments by Doctor")
        print("5. Back")
        ch = input("Choice: ")
        if ch == "1": book_appointment()
        elif ch == "2": view_appointments()
        elif ch == "3": update_status()
        elif ch == "4": appointments_by_doctor()
        elif ch == "5": break
        else: print("Invalid choice.")
