#include <Wire.h> 

#define DRIVE_ADDRESS 0x12

//


//Using mega 2560 and sabertooth dip switch 010111 *make sure its set to that specific order*
int s2=8; //pin 8 for servo 1
int s1=9; //pin 9 for servo 2
int f_b = 0, l_r = 0;

void setup() {
  // put your setup code here, to run once:s
  Wire.begin(DRIVE_ADDRESS);
  Wire.onReceive(receiveData); 
  Serial.setTimeout(10);
  
  pinMode(s1, OUTPUT);
  pinMode(s2, OUTPUT);

  Serial.begin(9600); // debugging console
}

void receiveData(int byteCount) // we should only be getting 2 bytes at once. 
{
  f_b = Wire.read();  // read a byte
  l_r = Wire.read(); 
  Serial.print("==Motors== BC: "); 
  Serial.println(byteCount);
  Serial.println(s1);
  Serial.println(s2);
  byteCount -= 2;

  analogWrite(s1, f_b);// 93 is stop backward and forward is scalable range 25 to 155
  analogWrite(s2, l_r);//93 is no steering, steering range(in degrees) 30 to 160  

  while(byteCount >= 2){
    Wire.read();
    Wire.read();
    byteCount -= 2;
  }
}

void recieveSerial(void){
  if (Serial.available() > 0) {
    // read the incoming byte:
    f_b = Serial.parseInt();
    l_r = Serial.parseInt();
    
    analogWrite(s1, f_b);// 93 is stop backward and forward is scalable range 25 to 155
    analogWrite(s2, l_r);//93 is no steering, steering range(in degrees) 30 to 160  
    
    Serial.println("==Motors== "); 
    Serial.println(f_b);
    Serial.println(l_r);
    delay(10);
    Serial.flush();
  }
}

void loop() {
  recieveSerial();
  delay(1); 
}

