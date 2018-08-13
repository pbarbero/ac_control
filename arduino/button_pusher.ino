#include <ArduinoJson.h>
#include <Servo.h>

Servo myServo;

void setup() {
  myServo.attach(9);
  myServo.write(80);

  Serial.begin(9600);
  while (!Serial) continue;
}

void pushButton() {
  myServo.write(110);
  delay(500);
  myServo.write(80);
}

void loop() {
  if(!Serial.available()) {
    return;
  }

  String jsonString = Serial.readString();
  StaticJsonBuffer<100> jsonBuffer;
  JsonObject& json = jsonBuffer.parseObject(jsonString);
  if (!json.success()) {
    return;
  }

  String action = json.get<String>("action");
  if (action == "motor") {
    pushButton();
  }
}

