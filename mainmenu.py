"""mainmenu.py — Central navigation for Hospital Management System.

Wraps each module call in a try/except. On error, prints the reason
and auto-restarts the program after 3 seconds.
"""

import os
import sys
import time

import patients
import doctors
import appointments
import billing
import graphs


def restart_program():
    print("\nRestarting the program in 3 seconds...")
    time.sleep(3)
    os.execl(sys.executable, sys.executable, *sys.argv)


def safe_call(func):
    try:
        func()
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        print("Reason: The module could not complete due to the error above.")
        restart_program()


def mainmenu():
    while True:
        print("\n========= HOSPITAL MANAGEMENT SYSTEM =========")
        print("1. Patients")
        print("2. Doctors")
        print("3. Appointments")
        print("4. Billing")
        print("5. Graphs / Reports")
        print("6. Exit")
        choice = input("Enter choice: ").strip()

        if not choice.isdigit():
            print("Invalid input. Please enter a number between 1 and 6.")
            continue

        choice = int(choice)
        if choice == 1: safe_call(patients.menu)
        elif choice == 2: safe_call(doctors.menu)
        elif choice == 3: safe_call(appointments.menu)
        elif choice == 4: safe_call(billing.menu)
        elif choice == 5: safe_call(graphs.menu)
        elif choice == 6:
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Enter 1-6.")


if __name__ == "__main__":
    mainmenu()
