import os
import pandas as pd
import psycopg2

# Load and clean CSV
csv_path = os.path.join(os.path.dirname(__file__), '../csv/data.csv')
df = pd.read_csv(csv_path)
df = df.dropna()  # Remove rows with missing values

# Database connection details
db_config = {
    "dbname": "investo_db",
    "user": "postgres",
    "password": os.getenv("POSTGRES_PASSWORD", "yourpassword"),
    "host": "localhost",
    "port": 5432
}

# Insert data into the database
def insert_data():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO stock_data (datetime, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (datetime) DO NOTHING;
        """, tuple(row))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    insert_data()
    print("Data inserted successfully!")