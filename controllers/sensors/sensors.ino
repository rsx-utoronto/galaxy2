 // I2C version of James' sensor code. Does not include the compass because I need i2c. 

#include <Wire.h>
#define SENSOR_ADDRESS 0x11

//analog pins
const int moisture_pin = A5; // connected to soil moisture sensor 
const int gas_1_pin = A0;    // connected to gas sensor
const int gas_2_pin = A1;
const int gas_3_pin = A2;
const int voltage_sensor_pin = A3;  // connected to voltage sensor (DFR0051)
//compass SCL goes to SCL (Mega) // not anymore, connect this directly to the Raspberry pi's i2c 
//compass SDA goes to SDA (Mega)

int moisture_value, gas_1_value, gas_2_value, gas_3_value; 
int voltage_value;  // voltage "value" is 10 times the actual voltage

void setup() {
	pinMode(moisture_pin, INPUT);
	pinMode(gas_1_pin, INPUT);
	pinMode(gas_2_pin, INPUT);
	pinMode(gas_3_pin, INPUT);
	pinMode(voltage_sensor_pin, INPUT);
	
	Wire.begin(SENSOR_ADDRESS);
    Wire.onRequest(handleRequest); 
    Serial.begin(9600); 
}

void loop() {
	//get sensor values. These get the raw values of the sensors, scaled to be [0, 255] i.e. fit in an unsigned byte. 
  moisture_value = analogRead(moisture_pin) / 4;  // unknown units. 
	gas_1_value = analogRead(gas_1_pin) / 4;
	gas_2_value = analogRead(gas_2_pin) / 4;
	gas_3_value = analogRead(gas_3_pin) / 4;
	voltage_value = analogRead(voltage_sensor_pin)/40.92 * 10;   // divide 'voltage' by 10 to get a value in volts. 
    Serial.println("===Sensors==="); 
	Serial.println(moisture_value); 
	Serial.println(gas_1_value); 
	Serial.println(gas_2_value); 
	Serial.println(gas_3_value);
	Serial.println(voltage_value); 
    delay(1000);
}

void handleRequest()
{
  byte sensors[] = {moisture_value, gas_1_value, gas_2_value, gas_3_value}; 
  Wire.write(sensors, sensors.length); 
	/*Wire.write(moisture_value); 
	Wire.write(gas_1_value); 
	Wire.write(gas_2_value); 
	Wire.write(gas_3_value); 
	Wire.write(voltage_value);  */ 
}
