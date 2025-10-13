import serial
import time

PORT = '/dev/ttyACM0'
BAUD = 9600

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)
    print("✅ Serial connection established with Arduino.\n")
except Exception as e:
    print(f"❌ Could not open serial port {PORT}: {e}")
    raise SystemExit

try:
    while True:
        raw = ser.readline().decode('utf-8', errors='ignore').strip()
        if not raw:
            continue

        if raw.upper().startswith("READY") or ("," not in raw):
            continue

        parts = raw.split(",")
        if len(parts) != 6:
            print(f"⚠️ Invalid data line: {raw}")
            continue

        try:
            gas_value = int(float(parts[0]))
            gas_detected = int(float(parts[1]))
            flame_detected = int(float(parts[2]))
            temperature = float(parts[3])
            humidity = float(parts[4])
            bpm = int(float(parts[5]))
        except Exception as e:
            print(f"⚠️ Conversion error: {e}, line: {raw}")
            continue

        gas_status = "DETECTED" if gas_detected else "SAFE"
        flame_status = "DETECTED" if flame_detected else "SAFE"
        temp_str = f"{temperature:.2f}" if temperature != -127.0 else "ERROR(-127)"
        hum_str = f"{humidity:.1f}" if humidity != -1.0 else "ERROR(-1)"
        bpm_str = f"{bpm:02d}" if bpm > 0 else "00"

        # --- Print in your desired style ---
        print(f"🔥 Gas: {gas_value} | Gas Det: {gas_detected} ({gas_status}) | "
              f"Flame: {flame_detected} ({flame_status}) | "
              f"Temp: {temp_str} | Humidity: {hum_str} | Pulse: {bpm_str}")

        time.sleep(1)

except KeyboardInterrupt:
    print("\n🛑 Exiting...")
finally:
    if ser.is_open:
        ser.close()
        print("🔌 Serial connection closed.")
