#include <OneWire.h>
#include <DallasTemperature.h>

// DS18B20 setup
#define ONE_WIRE_BUS 4
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// MQ-2 setup
int gasAnalog = A0;
int gasDigital = 2;

// Flame sensor
int flamePin = 3;

// Calibration threshold for digital detection
int gasThreshold = 400; // adjust this based on your sensor

void setup() {
  Serial.begin(9600);
  sensors.begin();
  pinMode(gasDigital, INPUT);
  pinMode(flamePin, INPUT);
}

void loop() {
  // Read analog value
  int gasValue = analogRead(gasAnalog);

  // Determine digital detection based on threshold
  int gasDetected = (gasValue >= gasThreshold) ? 1 : 0;

  // Flame sensor
  int flameRaw = digitalRead(flamePin);
  int flameDetected = (flameRaw == LOW) ? 1 : 0;

  // Temperature
  sensors.requestTemperatures();
  float temperatureC = sensors.getTempCByIndex(0);

  // Send CSV line
  Serial.print(gasValue);
  Serial.print(",");
  Serial.print(gasDetected);
  Serial.print(",");
  Serial.print(flameDetected);
  Serial.print(",");
  Serial.println(temperatureC);

  delay(1000);
}
