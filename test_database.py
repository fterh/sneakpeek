import sqlite3
import unittest
import config

# Set ENV to "test" before loading database module
config.ENV = "test"

from database import DatabaseManager

DB_NAME = config.DATABASE["NAME"]
DB_SUBMISSIONS_TABLE = config.DATABASE["TABLES"]["SUBMISSIONS"]["NAME"]
DB_SUBMISSIONS_ID = config.DATABASE["TABLES"]["SUBMISSIONS"]["ID_NAME"]
DB_SUBMISSIONS_ACTION = config.DATABASE["TABLES"]["SUBMISSIONS"]["ACTION_NAME"]
DB_SUBMISSIONS_INDEX = config.DATABASE["TABLES"]["SUBMISSIONS"]["ID_INDEX_NAME"]


class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        """Wipe database and insert test data before each test."""
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        # bootstrap(c)
        # DatabaseManager.bootstrapped = True

        c.execute("DELETE FROM {}".format(DB_SUBMISSIONS_TABLE))
        c.execute("INSERT INTO {} VALUES ('id1', 'action1', '')".format(
            DB_SUBMISSIONS_TABLE
        ))

        conn.commit()
        conn.close()

    @classmethod
    def tearDownClass(cls):
        """Wipe database after all tests."""
        DatabaseManager.disconnect()

        conn = sqlite3.connect(DB_NAME)
        conn.cursor().execute("DELETE FROM {}".format(DB_SUBMISSIONS_TABLE))
        conn.commit()
        conn.close()

    def test_check_id(self):
        self.assertEqual(DatabaseManager.check_id("id1"), True)
        self.assertEqual(DatabaseManager.check_id("id2"), False)

    def test_write_id(self):
        self.assertEqual(DatabaseManager.check_id("id2"), False)
        DatabaseManager.write_id("id2", "action2")
        self.assertEqual(DatabaseManager.check_id("id2"), True)

    def test_persistent_storage(self):
        self.assertEqual(DatabaseManager.check_id("id2"), False)
        DatabaseManager.write_id("id2", "action2")
        self.assertEqual(DatabaseManager.check_id("id2"), True)
        DatabaseManager.disconnect()
        self.assertEqual(DatabaseManager.check_id("id1"), True)
        self.assertEqual(DatabaseManager.check_id("id2"), True)


if __name__ == "__main__":
    unittest.main()
