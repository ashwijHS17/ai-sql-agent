import pandas as pd
import sqlite3
import os

def csv_to_sqlite(csv_file, db_path="data.db"):
    """
    Reads a CSV and writes it to a SQLite database.
    """
    try:
        # Load the CSV
        df = pd.read_csv(csv_file)
        
        # Clean column names for SQL compatibility
        df.columns = [c.strip().replace(' ', '_').replace('(', '').replace(')', '').lower() for c in df.columns]
        
        # Connect and write
        conn = sqlite3.connect(db_path)
        df.to_sql("data_table", conn, if_exists='replace', index=False)
        conn.close()
        return db_path, "data_table"
    except Exception as e:
        return None, str(e)

def get_db_schema(db_path):
    """Returns the schema of the generated table."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='data_table';")
    schema = cursor.fetchone()
    conn.close()
    return schema[0] if schema else "No schema found."
