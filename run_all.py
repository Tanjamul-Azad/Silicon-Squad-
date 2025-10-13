import subprocess
import time

print("🚀 Starting Care Companion system...")

# Start data collector
collector = subprocess.Popen(["python", "data_collector.py"])
time.sleep(2)  # wait a bit for it to start

# Start Flask dashboard
dashboard = subprocess.Popen(["python", "app.py"])

print("✅ Both scripts running.")
print("Press Ctrl+C to stop everything.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Stopping both scripts...")
    collector.terminate()
    dashboard.terminate()
