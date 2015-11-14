/* Setup for testing moisture sensor. Writes moisture to serial
 *  
 *  Arduino to YL-38: 
 *  3.3V - VCC
 *  GND - GND
 *  A0 - AO
 *  
 *  YL-38 to YL69:
 *  2 unlabelled pins to 2 unlabelled pins
 */

#define MOISTURE_INPUT A0 

void setup() {
  Serial.begin(9600); 
  pinMode(MOISTURE_INPUT, INPUT); 
}

int input; 
void loop() {
  input = analogRead(MOISTURE_INPUT); 
  Serial.write(input); 
}
