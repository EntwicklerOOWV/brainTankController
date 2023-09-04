import sqlite3


database_name = "database.db"


class DatabaseEntry:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._date = None
        self._projected_ppt = None
        self._actual_ppt = None
        self._waterlevel = None
        self._stored = None
        self._used = None
        self._overflow = None
        self._rainday = None

    # Property decorators
    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def projected_ppt(self):
        return self._projected_ppt

    @projected_ppt.setter
    def projected_ppt(self, value):
        self._projected_ppt = value

    @property
    def actual_ppt(self):
        return self._actual_ppt

    @actual_ppt.setter
    def actual_ppt(self, value):
        self._actual_ppt = value

    @property
    def waterlevel(self):
        return self._waterlevel

    @waterlevel.setter
    def waterlevel(self, value):
        self._waterlevel = value

    @property
    def stored(self):
        return self._stored

    @stored.setter
    def stored(self, value):
        self._stored = value

    @property
    def used(self):
        return self._used

    @used.setter
    def used(self, value):
        self._used = value

    @property
    def overflow(self):
        return self._overflow

    @overflow.setter
    def overflow(self, value):
        self._overflow = value

    @property
    def rainday(self):
        return self._rainday
    
    @rainday.setter
    def rainday(self, value):
        self._rainday = value

dbEntry = DatabaseEntry()

def db_init():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS measurements (
                        date TEXT,
                        projectedPPT NUMERIC,
                        actualPPT NUMERIC,
                        waterlevel NUMERIC,
                        stored NUMERIC,
                        used NUMERIC,
                        overflow NUMERIC,
                        rainday NUMERIC
                      )''')
        conn.commit()
        print("db created")
    except sqlite3.Error as e:
        print("db_init error:", e)

def db_insert(entry):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    try: 
        insert_query = """INSERT INTO measurements
        (date, projectedPPT, actualPPT, waterlevel, stored, used, overflow, rainday)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        data_tuple = (
            entry.date,
            entry.projected_ppt,
            entry.actual_ppt,
            entry.waterlevel,
            entry.stored,
            entry.used,
            entry.overflow,
            entry.rainday
        )
        cursor.execute(insert_query, data_tuple)
        conn.commit()
    except sqlite3.OperationalError as e:
        print("db_insert error", e)
    finally:
        conn.close()

def db_query(query):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    result = []
    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except sqlite3.OperationalError as e:
        print("db_query error", e)
    finally:
        conn.close()
        return result