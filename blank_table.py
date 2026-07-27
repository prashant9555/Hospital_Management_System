"""blank_table.py — Initialize the hospital_2026 database and all tables.

Run this ONCE before using the Hospital Management System.
Creates database `hospital_2026` and the tables:
  - patients
  - doctors
  - appointments
  - billing
"""

import mysql.connector as sql


def create_database_and_tables():
    con = sql.connect(host="localhost", user="root", passwd="Pras9555")
    cur = con.cursor()

    cur.execute("CREATE DATABASE IF NOT EXISTS hospital_2026")
    cur.execute("USE hospital_2026")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id   INT PRIMARY KEY,
            name         VARCHAR(60) NOT NULL,
            age          INT,
            gender       VARCHAR(10),
            phone        VARCHAR(15),
            address      VARCHAR(120),
            blood_group  VARCHAR(5),
            admit_date   DATE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            doctor_id     INT PRIMARY KEY,
            name          VARCHAR(60) NOT NULL,
            specialization VARCHAR(50),
            phone         VARCHAR(15),
            fees          INT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            appt_id     INT PRIMARY KEY,
            patient_id  INT,
            doctor_id   INT,
            appt_date   DATE,
            status      VARCHAR(15)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS billing (
            bill_id     INT PRIMARY KEY,
            patient_id  INT,
            amount      INT,
            bill_date   DATE,
            status      VARCHAR(10)
        )
    """)

    con.commit()
    print("Database `hospital_2026` and all tables created successfully.")
    cur.close()
    con.close()


if __name__ == "__main__":
    create_database_and_tables()
