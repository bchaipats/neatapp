import datetime
import os
import json
import pandas as pd
import psycopg


class DatabaseManager:
    def __init__(self, connection_string: str = None):
        self.connection_string = connection_string or os.getenv("DB_CONNECTION_STRING")

    def store_result(self, payload: dict, image_path: str) -> None:
        with psycopg.connect(self.connection_string) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO neatapp (payload, image_path, created_timestamp) VALUES (%s, %s, %s)",
                    (json.dumps(payload), image_path, datetime.datetime.now()),
                )

    def load_all_data(self) -> pd.DataFrame:
        with psycopg.connect(self.connection_string) as conn:
            df = pd.read_sql_query("SELECT created_timestamp, image_path, payload FROM neatapp", conn)
        return df