#include <Servo.h>
#include <Wire.h> 

#define DRIVE_ADDRESS 0x12

//Using mega 2560 and sabertooth dip switch 010111 *make sure its set to that specific order*
int servo1=8; //pin 8 for servo 1
int servo2=9; //pin 9 for servo 2
int forward_backward;
int left_right;

Servo myservo;
Servo myservo2;
 
void setup() {
  // put your setup code here, to run once:s
  Wire.begin(DRIVE_ADDRESS);
  Wire.onReceive(receiveData); 
  
  pinMode(servo1, OUTPUT);
  pinMode(servo2, OUTPUT);
  myservo.attach(servo1); //attach servo1
  myservo2.attach(servo2); //attach servo2

  Serial.begin(9600); // debugging console
}

void receiveData(int byteCount) // we should only be getting 2 bytes at once. 
{
  forward_backward = Wire.read();  // read a byte
  left_right = Wire.read(); 
  Serial.print("==Motors== BC: "); 
  Serial.println(byteCount);
  Serial.println(forward_backward);
  Serial.println(left_right);
  byteCount -= 2;

  myservo.write(forward_backward);// 93 is stop backward and forward is scalable range 25 to 155
  myservo2.write(left_right);//93 is no steering, steering range(in degrees) 30 to 160  

  while(byteCount >= 2){
    Wire.read();
    Wire.read();
    byteCount -= 2;
  }
}

void loop() {
  delay(1); 
}

