//Calculates Temperature in Celius
// (Ground) ---- (10k-Resistor) -------|------- (Thermistor) ---- (+5v)
//                                     |
//                               Analog Pin 0
float Thermistor(int RawADC) {  
  float Temp;
  Temp = log(10000*((1024.0 / RawADC) - 1)); // Saving the Log(resistance) so not to calculate  it 4 times later
  Temp = (1 / (0.001129148 + (0.000234125 * Temp) + (0.0000000876741 * Temp * Temp * Temp))) - 273.15; //Calulate temperature in Celsius using Steinhart-Hart equation                      
  return Temp;                              // Return the Temperature
}

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.print(float(Thermistor(analogRead(0)))); // read ADC at Pin 0 and  convert it to Celsius and display
  Serial.println("");                                    
  delay(5000);                                      // Delay a bit... 
}
