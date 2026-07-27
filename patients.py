"""patients.py — Patient records management (CRUD)."""

import mysql.connector as sql


def _connect():
    return sql.connect(host="localhost", user="root", passwd="Pras9555", database="hospital_2026")


def add_patient():
    con = _connect()
    cur = con.cursor()
    pid = int(input("Patient ID: "))
    name = input("Name: ")
    age = int(input("Age: "))
    gender = input("Gender (M/F/O): ")
    phone = input("Phone: ")
    address = input("Address: ")
    blood = input("Blood Group: ")
    admit = input("Admit Date (YYYY-MM-DD): ")
    cur.execute(
        "INSERT INTO patients VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
        (pid, name, age, gender, phone, address, blood, admit),
    )
    con.commit()
    print("Patient added successfully.")
    con.close()


def view_patients():
    con = _connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM patients")
    rows = cur.fetchall()
    print(f"{'ID':<5}{'Name':<25}{'Age':<5}{'Gender':<8}{'Phone':<15}{'Blood':<7}{'Admitted'}")
    print("-" * 80)
    for r in rows:
        print(f"{r[0]:<5}{r[1]:<25}{r[2]:<5}{r[3]:<8}{r[4]:<15}{r[6]:<7}{r[7]}")
    con.close()


def search_patient():
    con = _connect()
    cur = con.cursor()
    pid = int(input("Enter Patient ID to search: "))
    cur.execute("SELECT * FROM patients WHERE patient_id = %s", (pid,))
    r = cur.fetchone()
    if r:
        print(f"ID: {r[0]}\nName: {r[1]}\nAge: {r[2]}\nGender: {r[3]}\n"
              f"Phone: {r[4]}\nAddress: {r[5]}\nBlood: {r[6]}\nAdmitted: {r[7]}")
    else:
        print("Patient not found.")
    con.close()


def update_patient():
    con = _connect()
    cur = con.cursor()
    pid = int(input("Patient ID to update: "))
    phone = input("New Phone: ")
    address = input("New Address: ")
    cur.execute("UPDATE patients SET phone=%s, address=%s WHERE patient_id=%s",
                (phone, address, pid))
    con.commit()
    print("Patient updated." if cur.rowcount else "Patient not found.")
    con.close()


def delete_patient():
    con = _connect()
    cur = con.cursor()
    pid = int(input("Patient ID to delete: "))
    cur.execute("DELETE FROM patients WHERE patient_id=%s", (pid,))
    con.commit()
    print("Patient deleted." if cur.rowcount else "Patient not found.")
    con.close()


def menu():
    while True:
        print("\n--- PATIENTS ---")
        print("1. Add Patient")
        print("2. View All Patients")
        print("3. Search Patient")
        print("4. Update Patient")
        print("5. Delete Patient")
        print("6. Back")
        ch = input("Choice: ")
        if ch == "1": add_patient()
        elif ch == "2": view_patients()
        elif ch == "3": search_patient()
        elif ch == "4": update_patient()
        elif ch == "5": delete_patient()
        elif ch == "6": break
        else: print("Invalid choice.")
