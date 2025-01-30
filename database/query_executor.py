import sys
sys.dont_write_bytecode = True
import pandas as pd
from database.db_connection import get_db_connection

def fetch_data(db_key, query):
    """Fetch data from a specified database using an SQL query."""
    conn = get_db_connection(db_key)
    try:
        df = pd.read_sql(query, conn)
        return df
    finally:
        conn.close()
