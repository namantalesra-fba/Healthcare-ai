import os
import sqlite3

# Define base directories and target SQLite file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "medivoice.db")


def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    Enables foreign key constraint enforcement and dict-like row access.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def initialize_database():
    """
    Creates all required tables if they do not already exist.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            hospital TEXT,
            contact TEXT,
            fee INTEGER
        );

        CREATE TABLE IF NOT EXISTS slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            is_booked INTEGER DEFAULT 0,
            FOREIGN KEY (doctor_id) REFERENCES doctors (id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            patient_name TEXT NOT NULL,
            patient_contact TEXT,
            disease_predicted TEXT,
            symptoms TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (slot_id) REFERENCES slots (id) ON DELETE CASCADE,
            FOREIGN KEY (doctor_id) REFERENCES doctors (id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS symptom_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            symptoms TEXT,
            disease_predicted TEXT,
            created_at TEXT NOT NULL
        );
        """
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized successfully at: {DB_PATH}")