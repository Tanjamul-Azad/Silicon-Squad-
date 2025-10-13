import serial
import mysql.connector
import time

# === Serial Setup ===
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)

# === Database Setup ===
db = mysql.connector.connect(
    host="localhost",
    user="care_user",
    password="care_pass",
    database="care_companion"
)
cursor = db.cursor()

print("✅ Collecting data from Arduino...")

while True:
    line = ser.readline().decode('utf-8').strip()
    if line:
        try:
            parts = line.split(',')

            # Expect exactly 6 parts (gas, gas_det, flame, temp, hum, pulse)
            if len(parts) != 6:
                print("⚠️ Skipping malformed line:", line)
                continue

            gas = float(parts[0])
            gas_det = int(parts[1])
            flame = int(parts[2])
            temperature = float(parts[3])
            humidity = float(parts[4])
            pulse = int(parts[5])

            cursor.execute(
                "INSERT INTO sensor_data (gas, flame, temperature, humidity, pulse) VALUES (%s, %s, %s, %s, %s)",
                (gas, flame, temperature, humidity, pulse)
            )
            db.commit()
            print(f"✅ Inserted: Gas={gas}, Flame={flame}, Temp={temperature}, Hum={humidity}, Pulse={pulse}")

        except Exception as e:
            print("⚠️ Error parsing line:", line, "|", e)
