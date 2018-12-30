import sqlite3

import config

DB_NAME = config.DATABASE["NAME"]
DB_SUBMISSIONS_TABLE = config.DATABASE["TABLES"]["SUBMISSIONS"]["NAME"]
DB_SUBMISSIONS_ID = config.DATABASE["TABLES"]["SUBMISSIONS"]["ID_NAME"]
DB_SUBMISSIONS_ACTION = config.DATABASE["TABLES"]["SUBMISSIONS"]["ACTION_NAME"]
DB_SUBMISSIONS_INDEX = config.DATABASE["TABLES"]["SUBMISSIONS"]["ID_INDEX_NAME"]


class DatabaseActionEnum:
    """Provide a list of constants comprising valid actions to write to the database table column `action`."""
    ERROR = "error"
    SKIP = "skip"
    SUCCESS = "success"


class DatabaseManager:
    """
    Handle all communication with the database.
    """

    # bootstrapped = False
    connected = False
    connection = None
    cursor = None

    @classmethod
    def connect(cls):
        conn = sqlite3.connect(DB_NAME)
        cls.connection = conn
        cls.cursor = conn.cursor()
        cls.connected = True

        # if not cls.bootstrapped:
        #     bootstrap(cls.cursor)
        #     cls.bootstrapped = True

    @classmethod
    def disconnect(cls):
        if cls.connection is not None:
            cls.connection.commit()
            cls.connection.close()
        cls.cursor = None
        cls.connected = False

    @classmethod
    def check_id(cls, id):
        """Check if submission ID already exists in database."""
        if not cls.connected:
            cls.connect()

        c = cls.cursor
        c.execute(
            "SELECT COUNT(1) FROM {} WHERE {} = ?".format(
                DB_SUBMISSIONS_TABLE,
                DB_SUBMISSIONS_ID),
            (id,))
        res = c.fetchone()
        return res[0] == 1

    @classmethod
    def write_id(cls, id, action):
        """
        Write (id, action) to database.
        Raise ValueError if id already exists in database.
        """
        print("Starting write_id")
        if not cls.connected:
            print("Connection not established. Attempting to connect.")
            cls.connect()
            print("Connection established.")

        if cls.check_id(id):
            raise ValueError("id {} already exists in database".format(id))

        c = cls.cursor
        c.execute(
            "INSERT INTO {} VALUES (?, ?, ?)".format(DB_SUBMISSIONS_TABLE),
            (
                id,
                action,
                ""
            ))
