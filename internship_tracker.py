import sqlite3
import csv


def export_to_csv():
    conn = sqlite3.connect("internships.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT company, role, status FROM applications"
    )

    rows = cursor.fetchall()

    with open("applications.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Company", "Role", "Status"])

        writer.writerows(rows)

    conn.close()

    print("Applications exported successfully!")
def create_database():
    conn = sqlite3.connect("internships.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        role TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_application():
    company = input("Enter company name: ")
    role = input("Enter role name: ")
    status = input("Enter status (Applied/Interview/Rejected/Selected): ").lower()

    valid_statuses = ["applied", "interview", "rejected", "selected"]

    if status not in valid_statuses:
        print("Invalid status entered.")
        return

    conn = sqlite3.connect("internships.db")

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO applications (company, role, status) VALUES (?, ?, ?)",
        (company, role, status)
    )

    conn.commit()
    conn.close()

    print("Application added successfully!")


def view_applications():
    conn = sqlite3.connect("internships.db")

    cursor = conn.cursor()

    cursor.execute("SELECT company, role, status FROM applications")

    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No applications found.")
    else:
        for row in rows:
            print("--------------------")
            print("Company:", row[0])
            print("Role:", row[1])
            print("Status:", row[2])
            print("--------------------")

    conn.close()


def update_status():
    company = input("Enter company name: ")
    new_status = input("Enter new status: ").lower()

    valid_statuses = ["applied", "interview", "rejected", "selected"]

    if new_status not in valid_statuses:
        print("Invalid status entered.")
        return

    conn = sqlite3.connect("internships.db")

    cursor = conn.cursor()

    cursor.execute(
        "UPDATE applications SET status = ? WHERE company = ?",
        (new_status, company)
    )

    conn.commit()

    if cursor.rowcount > 0:
        print("Status updated successfully!")
    else:
        print("Company not found.")

    conn.close()

def main():
    while True:
        print("\n===== SMART INTERNSHIP TRACKER =====")
        print("1. Add Application")
        print("2. View Applications")
        print("3. Update Status")
        print("4. Delete Application")
        print("5. Search Application")
        print("6. View Statistics")
        print("7. Export to CSV")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_application()

        elif choice == "2":
            view_applications()

        elif choice == "3":
            update_status()

        elif choice == "4":
            delete_application()

        elif choice == "5":
            search_application()

        elif choice == "6":
            view_statistics()

        elif choice == "7":
            export_to_csv()

        elif choice == "8":
            print("Thank you for using Smart Internship Tracker!")
            break
        else:
            print("Invalid choice. Try again.")

def delete_application():
    company = input("Enter company name to delete: ")

    conn = sqlite3.connect("internships.db")

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM applications WHERE company = ?",
        (company,)
    )

    conn.commit()

    if cursor.rowcount > 0:
        print("Application deleted successfully!")
    else:
        print("Company not found.")

    conn.close()


def search_application():
    company = input("Enter company name to search: ")

    conn = sqlite3.connect("internships.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT company, role, status FROM applications WHERE company = ?",
        (company,)
    )

    result = cursor.fetchone()

    if result:
        print("--------------------")
        print("Company:", result[0])
        print("Role:", result[1])
        print("Status:", result[2])
        print("--------------------")
    else:
        print("Company not found.")

    conn.close()


def view_statistics():
    conn = sqlite3.connect("internships.db")

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM applications")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE status = 'applied'")
    applied = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE status = 'interview'")
    interview = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE status = 'rejected'")
    rejected = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE status = 'selected'")
    selected = cursor.fetchone()[0]

    print("\n===== APPLICATION STATISTICS =====")
    print("Total Applications:", total)
    print("Applied:", applied)
    print("Interview:", interview)
    print("Rejected:", rejected)
    print("Selected:", selected)

    conn.close()
create_database()
main()