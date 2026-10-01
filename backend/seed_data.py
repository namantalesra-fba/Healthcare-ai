from datetime import datetime, timedelta
from database import get_connection, initialize_database


def seed_database():
    """
    Initializes tables and seeds sample doctors and appointment slots.
    Guards against duplicate entries if run multiple times.
    """
    initialize_database()
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Seed Doctors if table is empty
    cursor.execute("SELECT COUNT(*) AS count FROM doctors;")
    doctor_count = cursor.fetchone()["count"]

    doctors_to_insert = [
        (
            "Dr. Rajesh Sharma",
            "General Physician",
            "City Care Hospital",
            "+91-9876543210",
            500,
        ),
        (
            "Dr. Priya Deshmukh",
            "Dermatologist",
            "Skin & Aesthetic Clinic",
            "+91-9876543211",
            700,
        ),
        (
            "Dr. Ananya Roy",
            "Cardiologist",
            "Heart Care Institute",
            "+91-9876543212",
            1000,
        ),
        (
            "Dr. Vikram Mehta",
            "Neurologist",
            "Apex Neuro Hospital",
            "+91-9876543213",
            1200,
        ),
        (
            "Dr. Sameer Khan",
            "Pulmonologist",
            "Breathe Easy Clinic",
            "+91-9876543214",
            800,
        ),
    ]

    if doctor_count == 0:
        cursor.executemany(
            """
            INSERT INTO doctors (name, specialization, hospital, contact, fee)
            VALUES (?, ?, ?, ?, ?);
            """,
            doctors_to_insert,
        )
        conn.commit()
        print("Doctor records inserted.")
    else:
        print("Doctors already exist. Skipping doctor seeding.")

    # 2. Seed Slots for each doctor if slots table is empty
    cursor.execute("SELECT COUNT(*) AS count FROM slots;")
    slot_count = cursor.fetchone()["count"]

    if slot_count == 0:
        cursor.execute("SELECT id FROM doctors;")
        doctors = cursor.fetchall()

        # Generate tomorrow and day-after-tomorrow dates (YYYY-MM-DD)
        today = datetime.now()
        dates = [
            (today + timedelta(days=1)).strftime("%Y-%m-%d"),
            (today + timedelta(days=2)).strftime("%Y-%m-%d"),
        ]

        time_slots = [
            ("09:00 AM", "09:30 AM"),
            ("10:00 AM", "10:30 AM"),
            ("11:30 AM", "12:00 PM"),
            ("02:00 PM", "02:30 PM"),
            ("03:30 PM", "04:00 PM"),
        ]

        slots_to_insert = []
        for doc in doctors:
            doc_id = doc["id"]
            for slot_date in dates:
                for start_t, end_t in time_slots:
                    slots_to_insert.append((doc_id, slot_date, start_t, end_t, 0))

        cursor.executemany(
            """
            INSERT INTO slots (doctor_id, date, start_time, end_time, is_booked)
            VALUES (?, ?, ?, ?, ?);
            """,
            slots_to_insert,
        )
        conn.commit()
        print("Appointment slots inserted.")
    else:
        print("Slots already exist. Skipping slot seeding.")

    # 3. Verification step
    cursor.execute("SELECT COUNT(*) AS total_doctors FROM doctors;")
    total_doctors = cursor.fetchone()["total_doctors"]

    cursor.execute(
        "SELECT COUNT(*) AS available_slots FROM slots WHERE is_booked = 0;"
    )
    available_slots = cursor.fetchone()["available_slots"]

    cursor.execute("SELECT COUNT(*) AS booked_slots FROM slots WHERE is_booked = 1;")
    booked_slots = cursor.fetchone()["booked_slots"]

    print("\n--- Database Verification Summary ---")
    print(f"Total registered doctors : {total_doctors}")
    print(f"Available slots          : {available_slots}")
    print(f"Booked slots             : {booked_slots}")
    print("--------------------------------------\n")

    conn.close()


if __name__ == "__main__":
    seed_database()