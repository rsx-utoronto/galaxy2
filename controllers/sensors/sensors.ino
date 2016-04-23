 // I2C version of James' sensor code. Does not include the compass because I need i2c. 

#include <Wire.h>
#define SENSOR_ADDRESS 0x11
// the sensors send values over serial using the addresses 0x80, 0x81, 0x82, 0x83 

// raw values from analog pins
// int raw_sensors[16] = {0};  // raw analog values from the sensors. in the range 0, 255
byte adjusted_sensors[16] = {0}; // values to be sent to the raspberry pi. 

void setup() {
  pinMode(A0, INPUT); // for(int i=A0; i<=A15; i++) may work, but is not guaranteed. that's why there's all this verbose code
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(A4, INPUT);
  pinMode(A5, INPUT);
  pinMode(A6, INPUT);
  pinMode(A7, INPUT);
  pinMode(A8, INPUT);
  pinMode(A9, INPUT);
  pinMode(A10, INPUT);
  pinMode(A11, INPUT);
  pinMode(A12, INPUT);
  pinMode(A13, INPUT);
  pinMode(A14, INPUT);
  pinMode(A15, INPUT);
	
	Wire.begin(SENSOR_ADDRESS);
  Wire.onRequest(handleRequest); 
  Serial.begin(9600); 
}

void loop() {
  Serial.println("===Sensors==="); 
  for(int i=0; i<16; i++)
  {
    adjusted_sensors[i] = analogRead(i) / 4; // scale to [0, 255] 
    Serial.print(adjusted_sensors[i]); 
    Serial.print(" "); 
  }
  Serial.println(""); 
  delay(1000);
}

void handleRequest()
{
  Wire.write(adjusted_sensors, 16); 
}
