import json
import os

import pandas as pd
import psycopg


def store_result(payload: json, image_path: str) -> None:
    """Save extracted payload and image path into the database.

    Args:
        payload (json): payload of information extracted from the image.
        image_path (str): the saved image path.
    """
    with psycopg.connect(os.getenv("DB_CONNECTION_STRING")) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO neatapp (payload, image_path) VALUES (%s, %s)",
                (
                    payload,
                    image_path,
                ),
            )


def load_data_as_dataframe() -> pd.DataFrame:
    """Load all extracted data stored in the database.

    Returns:
        pd.DataFrame: a pandas DataFrame contains all of the loaded data.
    """
    with psycopg.connect(os.getenv("DB_CONNECTION_STRING")) as conn:
        df = pd.read_sql_query("SELECT id, payload, image_path FROM neatapp", conn)
    return df
