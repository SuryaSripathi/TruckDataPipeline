import time
import random
import json
import uuid
from datetime import datetime
from typing import Dict, List

# CONFIGURATION
FLEET_SIZE = 6
UPDATE_INTERVAL_SEC = 2  # How often data is sent


class Truck:
    """
    Represents a single delivery truck in the fleet.
    Maintains state to ensure data continuity (Time Series).
    """

    def __init__(self, truck_id: str):
        self.truck_id = truck_id
        # Initial State
        self.speed = 0.0
        self.engine_temp = 70.0  # Degrees Celsius
        self.fuel_level = 100.0  # Percentage
        self.latitude = 41.8781  # Starting near Chicago
        self.longitude = -87.6298
        self.status = "IDLE"

    def _update_state(self):
        """
        Simulates physical changes in the truck.
        This introduces 'autocorrelation' for your SARIMAX model.
        """
        # 1. Simulate Speed (Random walk)
        # Change speed slightly (-5 to +5 mph), keep between 0 and 75
        acceleration = random.uniform(-5, 5)
        self.speed = max(0.0, min(75.0, self.speed + acceleration))

        # 2. Simulate Engine Temp (Correlated with Speed)
        # Higher speed = Higher temp. Plus some random noise.
        target_temp = 70 + (self.speed * 0.5)
        # Move current temp towards target temp slowly (thermal inertia)
        self.engine_temp += (target_temp - self.engine_temp) * 0.1 + random.uniform(-0.5, 0.5)

        # 3. Simulate Fuel Consumption
        consumption = 0.01 + (self.speed * 0.005)
        self.fuel_level = max(0.0, self.fuel_level - consumption)

        # 4. Status Logic
        if self.fuel_level < 5:
            self.status = "LOW_FUEL"
        elif self.engine_temp > 105:
            self.status = "OVERHEAT_WARNING"
        elif self.speed > 0:
            self.status = "IN_TRANSIT"
        else:
            self.status = "IDLE"

    def generate_telemetry(self) -> Dict:
        """
        Updates state and returns a dictionary data packet.
        This mimics a JSON payload from an IoT device.
        """
        self._update_state()

        return {
            "event_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "truck_id": self.truck_id,
            "speed_mph": round(self.speed, 2),
            "engine_temp_c": round(self.engine_temp, 2),
            "fuel_level_pct": round(self.fuel_level, 2),
            "status": self.status,
            # Simulating GPS drift for realism
            "gps_lat": round(self.latitude + random.uniform(-0.001, 0.001), 6),
            "gps_long": round(self.longitude + random.uniform(-0.001, 0.001), 6)
        }


class FleetManager:
    """
    Orchestrates the collection of data from all trucks.
    """

    def __init__(self, size: int):
        self.trucks = [Truck(f"TRUCK-{i + 1:03d}") for i in range(size)]

    def stream_data(self):
        """
        Generator function that yields real-time data.
        """
        print(f"--- STARTING FLEET SIMULATION ({len(self.trucks)} TRUCKS) ---")
        print("Press Ctrl+C to stop.")
        try:
            while True:
                for truck in self.trucks:
                    data = truck.generate_telemetry()
                    # In Phase 2, we will replace this print with a Database Insert
                    print(json.dumps(data))

                time.sleep(UPDATE_INTERVAL_SEC)
        except KeyboardInterrupt:
            print("\n--- SIMULATION STOPPED ---")


if __name__ == "__main__":
    fleet = FleetManager(FLEET_SIZE)
    fleet.stream_data()
    fleet.stream_data()