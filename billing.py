"""billing.py — Patient billing, payment tracking, and collection summary.

Business rule: bills carry a status of 'Paid' or 'Pending'. The summary
view aggregates total collected vs pending amounts.
"""

import mysql.connector as sql


def _connect():
    return sql.connect(host="localhost", user="root", passwd="Pras9555", database="hospital_2026")


def add_bill():
    con = _connect()
    cur = con.cursor()
    bid = int(input("Bill ID: "))
    pid = int(input("Patient ID: "))
    amount = int(input("Amount: "))
    date = input("Bill Date (YYYY-MM-DD): ")
    status = input("Status (Paid/Pending): ")
    cur.execute("INSERT INTO billing VALUES (%s,%s,%s,%s,%s)",
                (bid, pid, amount, date, status))
    con.commit()
    print("Bill added.")
    con.close()


def view_bills():
    con = _connect()
    cur = con.cursor()
    cur.execute("""
        SELECT b.bill_id, p.name, b.amount, b.bill_date, b.status
        FROM billing b JOIN patients p ON b.patient_id = p.patient_id
    """)
    rows = cur.fetchall()
    print(f"{'BID':<5}{'Patient':<25}{'Amount':<10}{'Date':<12}{'Status'}")
    print("-" * 70)
    for r in rows:
        print(f"{r[0]:<5}{r[1]:<25}{r[2]:<10}{str(r[3]):<12}{r[4]}")
    con.close()


def pending_bills():
    con = _connect()
    cur = con.cursor()
    cur.execute("""
        SELECT b.bill_id, p.name, b.amount, b.bill_date
        FROM billing b JOIN patients p ON b.patient_id = p.patient_id
        WHERE b.status = 'Pending'
    """)
    rows = cur.fetchall()
    if not rows:
        print("No pending bills.")
    total = 0
    for r in rows:
        print(f"BID {r[0]} | {r[1]} | Rs.{r[2]} | {r[3]}")
        total += r[2]
    print(f"Total Pending: Rs.{total}")
    con.close()


def mark_paid():
    con = _connect()
    cur = con.cursor()
    bid = int(input("Bill ID to mark Paid: "))
    cur.execute("UPDATE billing SET status='Paid' WHERE bill_id=%s", (bid,))
    con.commit()
    print("Bill marked as Paid." if cur.rowcount else "Bill not found.")
    con.close()


def collection_summary():
    con = _connect()
    cur = con.cursor()
    cur.execute("SELECT status, SUM(amount) FROM billing GROUP BY status")
    print("--- Collection Summary ---")
    for status, total in cur.fetchall():
        print(f"{status}: Rs.{total}")
    con.close()


def menu():
    while True:
        print("\n--- BILLING ---")
        print("1. Add Bill")
        print("2. View All Bills")
        print("3. View Pending Bills")
        print("4. Mark Bill as Paid")
        print("5. Collection Summary")
        print("6. Back")
        ch = input("Choice: ")
        if ch == "1": add_bill()
        elif ch == "2": view_bills()
        elif ch == "3": pending_bills()
        elif ch == "4": mark_paid()
        elif ch == "5": collection_summary()
        elif ch == "6": break
        else: print("Invalid choice.")
