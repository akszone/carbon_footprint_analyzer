import unittest
import sqlite3
import sys
import os
# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.storage import init_db, save_emission_record, get_all_emissions

TEST_DB_PATH = "test_carbon_data.db"

class TestStorage(unittest.TestCase):

    def setUp(self):
        # Create a fresh test database
        init_db(TEST_DB_PATH)

    def tearDown(self):
        # Clean up the test DB
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def test_init_db_creates_table(self):
        # Verify the emissions table exists
        with sqlite3.connect(TEST_DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='emissions'")
            self.assertIsNotNone(cursor.fetchone())

    def test_save_and_get_emission_record(self):
        flight_info = {
            "airline": "TestAir",
            "flight_number": "TA123",
            "date": "2025-05-24",
            "from": "JFK",
            "to": "LAX",
            "class": "Economy"
        }
        co2_kg = 123.45

        save_emission_record(flight_info, co2_kg, TEST_DB_PATH)

        records = get_all_emissions(TEST_DB_PATH)
        self.assertEqual(len(records), 1)

        record = records[0]
        self.assertEqual(record["airline"], "TestAir")
        self.assertEqual(record["flight_number"], "TA123")
        self.assertEqual(record["origin"], "JFK")
        self.assertEqual(record["destination"], "LAX")
        self.assertEqual(record["class"], "Economy")
        self.assertAlmostEqual(record["co2_kg"], 123.45, places=2)

if __name__ == "__main__":
    unittest.main()
