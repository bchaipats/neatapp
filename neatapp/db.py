import os

import pandas as pd
import psycopg


def load_data_as_dataframe() -> pd.DataFrame:
    """Load all extracted data stored in the database.

    Returns:
        pd.DataFrame: a pandas DataFrame contains all of the loaded data.
    """
    with psycopg.connect(os.getenv("DB_CONNECTION_STRING")) as conn:
        df = pd.read_sql_query("SELECT id, payload, image_path FROM neatapp", conn)
    return df
