import unittest
#import os
import sqlite3
import sys
import os
# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.reports import total_co2_emissions, flights_by_month

TEST_DB_PATH = "test_carbon_data.db"

class TestReports(unittest.TestCase):

    def setUp(self):
        # Create test DB and emissions table
        self.conn = sqlite3.connect(TEST_DB_PATH)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
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
        self.conn.commit()

        # Insert sample data
        sample_data = [
            ("AirlineA", "AA101", "2025-05-01", "JFK", "LAX", "Economy", 150.0, "2025-05-01T12:00:00Z"),
            ("AirlineB", "BB202", "2025-05-15", "LAX", "SFO", "Business", 50.0, "2025-05-15T12:00:00Z"),
            ("AirlineC", "CC303", "2025-04-20", "SFO", "SEA", "Economy", 70.0, "2025-04-20T12:00:00Z"),
            ("AirlineD", "DD404", "2025-04-25", "SEA", "JFK", "Economy", 200.0, "2025-04-25T12:00:00Z"),
            # Add more if you want
        ]

        self.cursor.executemany("""
            INSERT INTO emissions 
            (airline, flight_number, flight_date, origin, destination, class, co2_kg, estimated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_data)
        self.conn.commit()

    def tearDown(self):
        self.conn.close()
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def test_total_co2_emissions(self):
        total = total_co2_emissions(db_path=TEST_DB_PATH)
        expected_total = 150.0 + 50.0 + 70.0 + 200.0
        self.assertAlmostEqual(total, expected_total)

    def test_flights_by_month(self):
        flights = flights_by_month(db_path=TEST_DB_PATH)
        # Should be ordered descending by month (2025-05 first)
        expected = {
            "2025-05": 2,
            "2025-04": 2,
        }
        self.assertEqual(dict(flights), expected)

    def test_print_report(self):
        total = total_co2_emissions(db_path=TEST_DB_PATH)
        flights = flights_by_month(db_path=TEST_DB_PATH)

        print("\n--- Sample Report ---")
        print(f"Total CO2 Emissions: {total:.2f} kg")
        print("Flights by Month:")
        for month, count in flights.items():
            print(f"  {month}: {count} flights")


if __name__ == "__main__":
    unittest.main()
