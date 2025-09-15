import os
import json
import pandas as pd
import psycopg


def store_result(payload: dict, image_path: str) -> None:
    """Store extracted data payload and image path in the database.

    Args:
        payload (dict): extracted data as dictionary
        image_path (str): saved image file path
    """
    with psycopg.connect(os.getenv("DB_CONNECTION_STRING")) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO neatapp (payload, image_path, created_timestamp)
                VALUES (%s, %s, NOW())
                """,
                (json.dumps(payload), image_path),
            )
        conn.commit()


def load_all_data() -> pd.DataFrame:
    """Load all data from the neatapp table into a pandas DataFrame.

    Returns:
        pd.DataFrame: DataFrame with created_timestamp, image_path, and payload columns
    """
    with psycopg.connect(os.getenv("DB_CONNECTION_STRING")) as conn:
        df = pd.read_sql_query("SELECT created_timestamp, image_path, payload FROM neatapp ORDER BY created_timestamp DESC", conn)
    return df