// I2C version of Paul's robotic arm code. 

#define JOINT_STOP 0  
#define JOINT_CW 1    // directions for the arm joint 
#define JOINT_CCW 2

#define MOTOR_ADDRESS 0x10

#include <Wire.h> 

int motor1pin1 = 2;
int motor1pin2 = 3; 
int state = JOINT_STOP;

void setup() {
  Wire.begin(MOTOR_ADDRESS); 
  Wire.onReceive(receiveData); 
  pinMode(motor1pin1, OUTPUT); 
  pinMode(motor1pin2, OUTPUT); 
}

// listener for receiving data. 
void receiveData(int byteCount)
{
  for(int i=0; i<byteCount; i++)
  {
    int incomingByte = Wire.read(); 

    switch (incomingByte)
    {
      case '0':
        state = JOINT_STOP; 
        break; 
      case '1':
        state = JOINT_CW; 
        break; 
      case '2':
        state = JOINT_CCW; 
        break; 
    }
  }
}

// the loop function runs over and over again forever
void loop() {
  switch(state)
  {
    case JOINT_STOP:
      digitalWrite(motor1pin1, LOW);  
      digitalWrite(motor1pin2, LOW);
      break; 
    case JOINT_CW:
      digitalWrite(motor1pin1, LOW); 
      digitalWrite(motor1pin2, HIGH);   
      break; 
    case JOINT_CCW:
      digitalWrite(motor1pin1, HIGH); 
      digitalWrite(motor1pin2, LOW);
      break; 
  }
  delay(250); 
}
