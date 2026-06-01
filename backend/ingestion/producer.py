import os
import json
import fastf1
import psycopg2
import pandas as pd
from kafka import KafkaProducer
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# --- Connections ---
db = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="motorsport_telemetry",
    user="telemetry_user",
    password=os.getenv("POSTGRES_PASSWORD")
)
cursor = db.cursor()

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# --- Load FastF1 session ---
fastf1.Cache.enable_cache("cache")
session = fastf1.get_session(2024, "Monaco", "R") #change race info here to create new session
print("Loading session...")
session.load()
print("Session loaded.")

# --- Insert session row ---
cursor.execute("""
    INSERT INTO sessions (year, gp_name, session_type)
    VALUES (%s, %s, %s)
    RETURNING id
""", (2025, "Monaco", "Race"))
session_id = cursor.fetchone()[0]
db.commit()
print(f"Session inserted: {session_id}")

# --- Process each driver's laps ---
def to_ms(value):
    """Convert timedelta or NaT to milliseconds integer, or None."""
    if value is None or str(value) == "NaT":
        return None
    if isinstance(value, timedelta):
        return int(value.total_seconds() * 1000)
    return None

laps = session.laps

for _, lap in laps.iterrows():
    # Insert lap row
    cursor.execute("""
        INSERT INTO laps (
            session_id, driver_code, team, lap_number,
            lap_time_ms, sector1_ms, sector2_ms, sector3_ms,
            compound, tyre_life, stint, fresh_tyre,
            position, track_status, pit_in_time_ms, pit_out_time_ms,
            is_personal_best, deleted, deleted_reason, is_accurate
        ) VALUES (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        ) RETURNING id
    """, (
        str(session_id),
        lap["Driver"],
        lap["Team"],
        int(lap["LapNumber"]) if not pd.isna(lap["LapNumber"]) else None, #have to check since NaN can't be converted to int, normal if check doesnt check NaN
        to_ms(lap["LapTime"]),
        to_ms(lap["Sector1Time"]),
        to_ms(lap["Sector2Time"]),
        to_ms(lap["Sector3Time"]),
        lap["Compound"] if lap["Compound"] else None,
        int(lap["TyreLife"]) if not pd.isna(lap["TyreLife"]) else None,
        int(lap["Stint"]) if not pd.isna(lap["Stint"]) else None,
        bool(lap["FreshTyre"]) if lap["FreshTyre"] else None,
        int(lap["Position"]) if not pd.isna(lap["Position"]) else None,
        str(lap["TrackStatus"]) if lap["TrackStatus"] else None,
        to_ms(lap["PitInTime"]),
        to_ms(lap["PitOutTime"]),
        bool(lap["IsPersonalBest"]),
        bool(lap["Deleted"]) if lap["Deleted"] else False,
        str(lap["DeletedReason"]) if lap["DeletedReason"] else None,
        bool(lap["IsAccurate"])
    ))
    lap_id = cursor.fetchone()[0]
    db.commit()

    # Get car signals for this lap and publish to Kafka
    try:
        car_data = lap.get_car_data()
        for _, signal in car_data.iterrows():
            message = {
                "lap_id": str(lap_id),
                "session_time_ms": int(signal["SessionTime"].total_seconds() * 1000),
                "speed": int(signal["Speed"]) if not pd.isna(signal["Speed"]) else None,
                "rpm": int(signal["RPM"]) if not pd.isna(signal["RPM"]) else None,
                "throttle": int(signal["Throttle"]) if not pd.isna(signal["Throttle"]) else None,
                "brake": bool(signal["Brake"]),
                "gear": int(signal["nGear"]) if not pd.isna(signal["nGear"]) else None,
                "drs": int(signal["DRS"]) if not pd.isna(signal["DRS"]) else None,
            }
            producer.send("car.signals.raw", key=None, value=message)
    except Exception as e:
        print(f"Skipping signals for lap {lap['LapNumber']} {lap['Driver']}: {e}")
        continue

producer.flush()
print("All messages published to Kafka.")
cursor.close()
db.close()