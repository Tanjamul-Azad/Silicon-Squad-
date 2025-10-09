#include <OneWire.h>
#include <DallasTemperature.h>
#include <DHT.h>

// ---------------- Pin Definitions ----------------
#define ONE_WIRE_BUS 4   // DS18B20 data pin
#define DHTPIN 5         // DHT11 data pin
#define DHTTYPE DHT11
#define MQ2_A A0         // MQ-2 analog output
#define MQ2_D 7          // MQ-2 digital output (optional)
#define FLAME_PIN 3      // Flame sensor digital pin (active LOW)

// ---------------- Sensor Objects ----------------
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
DHT dht(DHTPIN, DHTTYPE);

// ---------------- Threshold ----------------
int gasThreshold = 400; // Analog threshold for MQ-2 detection

// ---------------- Setup ----------------
void setup() {
  Serial.begin(9600);
  sensors.begin();
  dht.begin();

  pinMode(MQ2_A, INPUT);
  pinMode(MQ2_D, INPUT);       // optional, module’s own digital output
  pinMode(FLAME_PIN, INPUT_PULLUP); // avoid floating, module pulls LOW on flame

  delay(2000); // Sensor warm-up
  Serial.println("READY");
}

// ---------------- Main Loop ----------------
void loop() {
  // --- MQ-2 Gas Sensor ---
  int gasValue = analogRead(MQ2_A);               // 0..1023
  int gasDetected = (gasValue >= gasThreshold) ? 1 : 0; // 1 = detected, 0 = safe

  // --- Flame Sensor (Active LOW) ---
  int flameRaw = digitalRead(FLAME_PIN);
  int flameDetected = (flameRaw == LOW) ? 1 : 0; // 1 = flame detected, 0 = safe

  // --- DS18B20 Temperature ---
  sensors.requestTemperatures();
  float tempDS = sensors.getTempCByIndex(0);
  bool ds_ok = (tempDS != DEVICE_DISCONNECTED_C);

  // --- DHT11 Temperature & Humidity ---
  float tempDHT = dht.readTemperature();  // may be NAN if fail
  float humidity = dht.readHumidity();    // may be NAN if fail

  // --- Decide temperature to send ---
  float temperatureToSend;
  if (ds_ok) {
    temperatureToSend = tempDS;
  } else if (!isnan(tempDHT)) {
    temperatureToSend = tempDHT;
  } else {
    temperatureToSend = -127.0;
  }

  if (isnan(humidity)) humidity = -1.0;

  // --- CSV Output for Raspberry Pi ---
  // Format: gasValue,gasDetected,flameDetected,temperature,humidity
  Serial.print(gasValue); Serial.print(",");
  Serial.print(gasDetected); Serial.print(",");
  Serial.print(flameDetected); Serial.print(",");
  Serial.print(temperatureToSend); Serial.print(",");
  Serial.println(humidity);

  delay(1000);
}
