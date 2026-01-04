import pandas as pd
import psycopg2
from statsmodels.tsa.statespace.sarimax import SARIMAX
from config import DB_CONFIG, TABLE_NAME
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")


def fetch_data(truck_id):
    """
    Connects to the DB and fetches the last 100 data points for a specific truck.
    JD Requirement: 'Experience with SQL, Python'
    """
    conn = psycopg2.connect(**DB_CONFIG)
    query = f"""
        SELECT timestamp, engine_temp_c 
        FROM {TABLE_NAME} 
        WHERE truck_id = '{truck_id}' 
        ORDER BY timestamp ASC 
        LIMIT 100
    """
    # Load directly into a Pandas DataFrame
    df = pd.read_sql(query, conn)
    conn.close()

    # Convert timestamp to datetime object
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df


def train_and_predict(df):
    """
    Trains a SARIMAX model on the engine temperature.
    JD Requirement: 'Statistical and machine learning techniques'
    """
    if len(df) < 10:
        print("Not enough data to train model yet.")
        return

    # We use engine_temp_c as the target variable
    # Order=(1,1,1) is a standard starting point for ARIMA
    # Seasonal_order=(1,1,1,12) assumes some seasonality (simulated)
    print("Training SARIMAX model...")
    model = SARIMAX(df['engine_temp_c'],
                    order=(1, 1, 1),
                    seasonal_order=(1, 1, 1, 12))

    model_fit = model.fit(disp=False)

    # Forecast the next 5 steps (simulating next 10 seconds)
    forecast = model_fit.forecast(steps=5)

    # Check if any predicted value exceeds the danger threshold
    next_temp = forecast.iloc[0]
    print(f"Current Temp: {df['engine_temp_c'].iloc[-1]:.2f}°C")
    print(f"Predicted Temp (Next Step): {next_temp:.2f}°C")

    if next_temp > 100:
        print("⚠️ ALERT: PREDICTED OVERHEATING! SCHEDULE MAINTENANCE.")
    else:
        print("✅ Status: Normal Operation")


def get_active_trucks():
    """
    Finds all unique truck IDs currently in the database.
    """
    conn = psycopg2.connect(**DB_CONFIG)
    # query to get unique truck_ids
    query = f"SELECT DISTINCT truck_id FROM {TABLE_NAME}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df['truck_id'].tolist()


if __name__ == "__main__":
    print("--- STARTING FLEET ANALYSIS ---")

    # 1. Get list of all trucks (e.g., ['TRUCK-001', 'TRUCK-002', ...])
    trucks = get_active_trucks()
    print(f"Found {len(trucks)} active trucks.")

    # 2. Loop through each truck and run the model
    for truck_id in trucks:
        print(f"\nAnalyzing {truck_id}...")
        data = fetch_data(truck_id)

        if not data.empty:
            try:
                train_and_predict(data)
            except Exception as e:
                print(f"Could not train model for {truck_id}: {e}")
        else:
            print("No data found.")

    print("\n--- ANALYSIS COMPLETE ---")