import serial
import time

PORT = '/dev/ttyACM0'
BAUD = 9600

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)
    print("✅ Serial connection established with Arduino.")
except Exception as e:
    print(f"❌ Could not open serial port {PORT}: {e}")
    raise SystemExit

try:
    while True:
        raw = ser.readline().decode('utf-8', errors='ignore').strip()
        if not raw:
            continue

        # ignore non-CSV startup lines like "READY"
        if raw.upper().startswith("READY") or ("," not in raw):
            # optional debug: print("DBG:", raw)
            continue

        parts = raw.split(",")
        if len(parts) != 5:
            print(f"⚠️ Invalid data format: {raw}")
            continue

        try:
            gas_value = int(float(parts[0]))
            gas_detected = int(float(parts[1]))
            flame_detected = int(float(parts[2]))
            temperature = float(parts[3])
            humidity = float(parts[4])
        except Exception as e:
            print("⚠️ Conversion error:", e, "line:", raw)
            continue

        gas_status = "DETECTED" if gas_detected == 1 else "SAFE"
        flame_status = "DETECTED" if flame_detected == 1 else "SAFE"
        temp_str = f"{temperature:.2f} °C" if temperature != -127.0 else "ERROR(-127)"
        hum_str = f"{humidity:.1f}%" if humidity != -1.0 else "ERROR(-1)"

        print(f"🔥 Gas: {gas_value} | Gas Det: {gas_detected} ({gas_status}) | "
              f"Flame: {flame_detected} ({flame_status}) | Temp: {temp_str} | Humidity: {hum_str}")

        
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n🛑 Exiting...")
finally:
    if ser.is_open:
        ser.close()
        print("🔌 Serial connection closed.")
