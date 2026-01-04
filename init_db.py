import psycopg2
from config import DB_CONFIG, TABLE_NAME


def create_table():
    """
    Connects to the Postgres DB and creates the sensor_data table.
    """
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id SERIAL PRIMARY KEY,
        event_id UUID NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        truck_id VARCHAR(50) NOT NULL,
        speed_mph DECIMAL(5, 2),
        engine_temp_c DECIMAL(5, 2),
        fuel_level_pct DECIMAL(5, 2),
        status VARCHAR(20),
        gps_lat DECIMAL(9, 6),
        gps_long DECIMAL(9, 6)
    );
    """

    try:
        # Establish connection
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Execute Query
        print(f"Creating table '{TABLE_NAME}' if it doesn't exist...")
        cur.execute(create_table_query)

        # Commit changes and close
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully.")

    except Exception as e:
        print(f"Error initializing database: {e}")


if __name__ == "__main__":
    create_table()