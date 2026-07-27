"""graphs.py — Visualizations for hospital data using matplotlib."""

import mysql.connector as sql
import matplotlib.pyplot as plt


def _connect():
    return sql.connect(host="localhost", user="root", passwd="Pras9555", database="hospital_2026")


def patients_by_gender():
    con = _connect()
    cur = con.cursor()
    cur.execute("SELECT gender, COUNT(*) FROM patients GROUP BY gender")
    data = cur.fetchall()
    labels = [d[0] for d in data]
    counts = [d[1] for d in data]
    plt.pie(counts, labels=labels, autopct="%1.1f%%")
    plt.title("Patients by Gender")
    plt.show()
    con.close()


def doctors_by_specialization():
    con = _connect()
    cur = con.cursor()
    cur.execute("SELECT specialization, COUNT(*) FROM doctors GROUP BY specialization")
    data = cur.fetchall()
    labels = [d[0] for d in data]
    counts = [d[1] for d in data]
    plt.bar(labels, counts, color="teal")
    plt.title("Doctors by Specialization")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    con.close()


def appointment_status_chart():
    con = _connect()
    cur = con.cursor()
    cur.execute("SELECT status, COUNT(*) FROM appointments GROUP BY status")
    data = cur.fetchall()
    labels = [d[0] for d in data]
    counts = [d[1] for d in data]
    plt.pie(counts, labels=labels, autopct="%1.1f%%")
    plt.title("Appointment Status")
    plt.show()
    con.close()


def billing_status_chart():
    con = _connect()
    cur = con.cursor()
    cur.execute("SELECT status, SUM(amount) FROM billing GROUP BY status")
    data = cur.fetchall()
    labels = [d[0] for d in data]
    totals = [d[1] for d in data]
    plt.bar(labels, totals, color=["green", "red"])
    plt.title("Billing: Paid vs Pending (Rs.)")
    plt.show()
    con.close()


def menu():
    while True:
        print("\n--- GRAPHS ---")
        print("1. Patients by Gender (Pie)")
        print("2. Doctors by Specialization (Bar)")
        print("3. Appointment Status (Pie)")
        print("4. Billing Paid vs Pending (Bar)")
        print("5. Back")
        ch = input("Choice: ")
        if ch == "1": patients_by_gender()
        elif ch == "2": doctors_by_specialization()
        elif ch == "3": appointment_status_chart()
        elif ch == "4": billing_status_chart()
        elif ch == "5": break
        else: print("Invalid choice.")
