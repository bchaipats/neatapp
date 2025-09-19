import os
import json
from typing import Any
import pandas as pd
import psycopg

class Database:
    def __init__(self, conn_str: str | None = None):
        self.conn_str = conn_str or os.getenv('DB_CONNECTION_STRING')

    def insert_result(self, payload: dict | str, image_path: str) -> None:
        """Insert extracted data and image path."""
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        with psycopg.connect(self.conn_str) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO neatapp (payload, image_path, created_timestamp) VALUES (%s, %s, NOW())",
                    (payload, image_path)
                )
                conn.commit()

    def load_all(self) -> pd.DataFrame:
        """Fetch all records as DataFrame."""
        with psycopg.connect(self.conn_str) as conn:
            df = pd.read_sql_query("SELECT created_timestamp, image_path, payload FROM neatapp", conn)
        return df