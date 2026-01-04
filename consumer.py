import sys
import json
import psycopg2
from datetime import datetime
from config import DB_CONFIG, TABLE_NAME


def insert_record(cursor, data):
    """
    Inserts a single JSON record into the database.
    """
    insert_query = f"""
    INSERT INTO {TABLE_NAME} 
    (event_id, timestamp, truck_id, speed_mph, engine_temp_c, fuel_level_pct, status, gps_lat, gps_long)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(insert_query, (
        data['event_id'],
        data['timestamp'],
        data['truck_id'],
        data['speed_mph'],
        data['engine_temp_c'],
        data['fuel_level_pct'],
        data['status'],
        data['gps_lat'],
        data['gps_long']
    ))


def start_consumer():
    """
    Reads JSON lines from Standard Input (stdin) and inserts them into DB.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True  # Auto-save data immediately
        cur = conn.cursor()
        print("Consumer started. Waiting for data...")

        # Loop through every line piped into the script
        for line in sys.stdin:
            try:
                # Parse JSON
                record = json.loads(line)

                # Insert to DB
                insert_record(cur, record)

                # Simple logging
                print(f"Stored: {record['truck_id']} at {record['timestamp']}")

            except json.JSONDecodeError:
                continue  # Skip partial lines or errors

    except KeyboardInterrupt:
        print("Consumer stopping...")
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()


if __name__ == "__main__":
    start_consumer()