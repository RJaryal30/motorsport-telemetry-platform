import os
import fastf1

os.makedirs("cache", exist_ok=True)

# Enable local caching - Store downloaded data locally so it doesn't re-download every run
fastf1.Cache.enable_cache("cache")

# Load a race session
session = fastf1.get_session(2024, "Monaco", "R")

print("Loading session...")
session.load()

print("Session loaded!")

# print(session.laps.head())
print(session.laps.columns.tolist())
print("********************************")

verstappen = session.laps.pick_drivers("VER")
fastest_lap = verstappen.pick_fastest()
print(fastest_lap)
print("********************************")

telemetry = fastest_lap.get_car_data()
print(telemetry.head())
print(telemetry.columns.tolist())
print("********************************")
print(fastest_lap.get_telemetry().columns.tolist())
