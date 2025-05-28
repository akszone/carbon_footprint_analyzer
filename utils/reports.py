import sqlite3
from collections import defaultdict, OrderedDict

DEFAULT_DB_PATH = "carbon_data.db"

def total_co2_emissions(db_path=DEFAULT_DB_PATH) -> float:
    """Calculate total CO2 emissions from all flights in the database."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(co2_kg) FROM emissions")
        total_co2 = cursor.fetchone()[0] or 0.0
    return total_co2

def flights_by_month(db_path=DEFAULT_DB_PATH) -> dict:
    """
    Return the number of flights by month (YYYY-MM),
    sorted descending by month.
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT strftime('%Y-%m', flight_date), COUNT(*)
            FROM emissions
            GROUP BY strftime('%Y-%m', flight_date)
            ORDER BY strftime('%Y-%m', flight_date) DESC
        """)
        rows = cursor.fetchall()

    # Use OrderedDict to preserve SQL order
    monthly_flights = OrderedDict()
    for month, count in rows:
        monthly_flights[month] = count
    return monthly_flights
