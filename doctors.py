"""doctors.py — Doctor records and specialization management."""

import mysql.connector as sql


def _connect():
    return sql.connect(host="localhost", user="root", passwd="root", database="hospital_2026")


def add_doctor():
    con = _connect()
    cur = con.cursor()
    did = int(input("Doctor ID: "))
    name = input("Name: ")
    spec = input("Specialization: ")
    phone = input("Phone: ")
    fees = int(input("Consultation Fees: "))
    cur.execute("INSERT INTO doctors VALUES (%s,%s,%s,%s,%s)",
                (did, name, spec, phone, fees))
    con.commit()
    print("Doctor added successfully.")
    con.close()


def view_doctors():
    con = _connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM doctors")
    rows = cur.fetchall()
    print(f"{'ID':<5}{'Name':<25}{'Specialization':<20}{'Phone':<15}{'Fees'}")
    print("-" * 75)
    for r in rows:
        print(f"{r[0]:<5}{r[1]:<25}{r[2]:<20}{r[3]:<15}{r[4]}")
    con.close()


def search_by_specialization():
    con = _connect()
    cur = con.cursor()
    spec = input("Specialization to search: ")
    cur.execute("SELECT * FROM doctors WHERE specialization LIKE %s", (f"%{spec}%",))
    rows = cur.fetchall()
    if not rows:
        print("No doctor found for this specialization.")
    for r in rows:
        print(f"{r[0]} | {r[1]} | {r[2]} | Fees: Rs.{r[4]}")
    con.close()


def update_doctor():
    con = _connect()
    cur = con.cursor()
    did = int(input("Doctor ID to update: "))
    fees = int(input("New Fees: "))
    cur.execute("UPDATE doctors SET fees=%s WHERE doctor_id=%s", (fees, did))
    con.commit()
    print("Doctor updated." if cur.rowcount else "Doctor not found.")
    con.close()


def delete_doctor():
    con = _connect()
    cur = con.cursor()
    did = int(input("Doctor ID to delete: "))
    cur.execute("DELETE FROM doctors WHERE doctor_id=%s", (did,))
    con.commit()
    print("Doctor deleted." if cur.rowcount else "Doctor not found.")
    con.close()


def menu():
    while True:
        print("\n--- DOCTORS ---")
        print("1. Add Doctor")
        print("2. View All Doctors")
        print("3. Search by Specialization")
        print("4. Update Doctor Fees")
        print("5. Delete Doctor")
        print("6. Back")
        ch = input("Choice: ")
        if ch == "1": add_doctor()
        elif ch == "2": view_doctors()
        elif ch == "3": search_by_specialization()
        elif ch == "4": update_doctor()
        elif ch == "5": delete_doctor()
        elif ch == "6": break
        else: print("Invalid choice.")
