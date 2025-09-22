from .models import Restaurant

class RestaurantService:
    def __init__(self, db):
        self.db = db
        self._ensure_table()

    def _ensure_table(self):
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                cuisine TEXT NOT NULL,
                location TEXT NOT NULL
            )
        ''')

    def create(self, name, cuisine, location):
        sql = 'INSERT INTO restaurants (name, cuisine, location) VALUES (?, ?, ?);'
        cur = self.db.execute(sql, (name, cuisine, location))
        rid = cur.lastrowid
        return Restaurant(rid, name, cuisine, location)

    def get_by_id(self, rid):
        row = self.db.query('SELECT id, name, cuisine, location FROM restaurants WHERE id = ?', (rid,))
        if not row:
            return None
        return Restaurant(*row[0])

    def list_all(self):
        rows = self.db.query('SELECT id, name, cuisine, location FROM restaurants')
        return [Restaurant(*row) for row in rows]