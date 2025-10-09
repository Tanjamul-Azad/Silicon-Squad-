import serial
import time

# Adjust serial port if necessary
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # allow Arduino reset

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            parts = line.split(",")
            if len(parts) == 4:
                gas_value = int(parts[0])         # MQ-2 analog
                gas_detected = int(parts[1])      # MQ-2 digital
                flame_detected = int(parts[2])    # Flame sensor
                temperature = float(parts[3])     # DS18B20

                print(f"Gas: {gas_value} | Gas Det: {gas_detected} | Flame: {flame_detected} | Temp: {temperature:.2f} °C")

except KeyboardInterrupt:
    ser.close()
    print("Exiting...")