#include <DHT.h>

// ---------------- Pin Definitions ----------------
#define DHTPIN 5          // DHT11 data pin
#define DHTTYPE DHT11
#define MQ2_A A0          // MQ-2 analog output
#define MQ2_D 7           // MQ-2 digital output (optional)
#define FLAME_PIN 3       // Flame sensor digital pin (active LOW)
#define PULSE_PIN A1      // Pulse sensor analog input

// ---------------- Sensor Objects ----------------
DHT dht(DHTPIN, DHTTYPE);

// ---------------- Threshold ----------------
int gasThreshold = 400;   // Analog threshold for MQ-2 detection

// ---------------- Setup ----------------
void setup() {
  Serial.begin(9600);
  dht.begin();

  pinMode(MQ2_A, INPUT);
  pinMode(MQ2_D, INPUT);
  pinMode(FLAME_PIN, INPUT_PULLUP);  // Active LOW
  pinMode(PULSE_PIN, INPUT);

  delay(2000); // Sensor warm-up
  Serial.println("READY");
}

// ---------------- Main Loop ----------------
void loop() {
  // --- MQ-2 Gas Sensor ---
  int gasValue = analogRead(MQ2_A);               // 0–1023
  int gasDetected = (gasValue >= gasThreshold) ? 1 : 0;

  // --- Flame Sensor (Active LOW) ---
  int flameRaw = digitalRead(FLAME_PIN);
  int flameDetected = (flameRaw == LOW) ? 1 : 0;

  // --- DHT11 Temperature & Humidity ---
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  bool dht_ok = (!isnan(temperature) && !isnan(humidity));

  if (!dht_ok) {
    temperature = -127.0;
    humidity = -1.0;
  }

  // --- Pulse Sensor ---
  int pulseValue = analogRead(PULSE_PIN);
  // Normalize a bit (simple smoothing)
  pulseValue = map(pulseValue, 0, 1023, 0, 200); // optional scaling

  // --- CSV Output for Raspberry Pi ---
  // Format: gasValue,gasDetected,flameDetected,temperature,humidity,pulse
  Serial.print(gasValue); Serial.print(",");
  Serial.print(gasDetected); Serial.print(",");
  Serial.print(flameDetected); Serial.print(",");
  Serial.print(temperature); Serial.print(",");
  Serial.print(humidity); Serial.print(",");
  Serial.println(pulseValue);

  delay(1000);
}
