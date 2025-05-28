import sqlite3
from datetime import datetime
import os

# Default path to the production database
DB_PATH = os.path.join(os.path.dirname(__file__), "../carbon_data.db")

def init_db(db_path=DB_PATH):
    """Create the emissions table if it doesn't exist."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                airline TEXT,
                flight_number TEXT,
                flight_date TEXT,
                origin TEXT,
                destination TEXT,
                class TEXT,
                co2_kg REAL,
                estimated_at TEXT
            )
        """)
        conn.commit()

def save_emission_record(flight_info, co2_kg, db_path=DB_PATH):
    """
    Save flight + emissions data to the database.
    - flight_info: dict from the AI parser
    - co2_kg: CO₂ emission in kilograms from Climatiq
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO emissions (
                airline, flight_number, flight_date, origin, destination, class, co2_kg, estimated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            flight_info.get("airline"),
            flight_info.get("flight_number"),
            flight_info.get("date"),
            flight_info.get("from"),
            flight_info.get("to"),
            flight_info.get("class"),
            co2_kg,
            datetime.utcnow().isoformat()
        ))
        conn.commit()

def get_all_emissions(db_path=DB_PATH):
    """
    Retrieve all emission records.
    Returns a list of sqlite3.Row objects (dict-like access).
    """
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM emissions")
        return cursor.fetchall()
