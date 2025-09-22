import sqlite3

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path)

    def execute(self, sql, params=None):
        self.connect()
        with self.conn:
            return self.conn.execute(sql, params or ())

    def query(self, sql, params=None):
        self.connect()
        cur = self.conn.cursor()
        cur.execute(sql, params or ())
        return cur.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()