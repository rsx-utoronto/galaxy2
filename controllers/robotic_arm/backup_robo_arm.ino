/* TODO:
   - check and correct assumptions
*/

// for reading instructions from pi
#include <Wire.h>

// temp, I don't actually know how many joints there are
// CW pin means HIGH on that pin, LOW on other turns motor clockwise
#define J_1_CW 1
#define J_1_CCW 2
#define J_2_CW 3
#define J_2_CCW 4
#define J_3_CW 5
#define J_3_CCW 6

// set to 1 if pins used are capable of PWM
#define PWM_ENABLED 0

// variables to store position of joystick
int jointToControl, x, y;

void setup() {
    pinMode(J_1_CW, OUTPUT);
    pinMode(J_1_CWW, OUTPUT);
    pinMode(J_2_CW, OUTPUT);
    pinMode(J_2_CWW, OUTPUT);
    pinMode(J_3_CW, OUTPUT);
    pinMode(J_3_CWW, OUTPUT);
}

int receiveData(int byteCount) {
    jointToControl = Wire.read();  // read a byte
    x = Wire.read(); 
    y = Wire.read();
    byteCount -= 3;

    while (byteCount >= 3) {
    Wire.read();
    Wire.read();
    Wire.read();
    byteCount -= 3;
    }
}

// only y position (assuming forward/back on joystick) will be used to control motors
void loop() {
    receiveData(3) // updates the joystick position variables jointToControl, x, y

    // which joint is currently being controlled, defaults to joint 1
    switch (jointToControl) {
        case 1:
            int cw = J_1_CW, ccw = J_1_CCW;
            break;
        case 2:
            int cw = J_2_CW, ccw = J_2_CCW;
            break;
        case 3:
            int cw = J_3_CW, ccw = J_3_CCW;
            break;
        default:
            int cw = J_1_CW, ccw = J_1_CCW;
    }

    // not capable of pwm, motor moves only at 1 speed regardless of angle of joystick
    if (! PWM_ENABLED) {
        if (y < 0) {
            digitalWrite(ccw, HIGH);     // no particular reason why I chose this combo of directions
            digitalWrite(cw, LOW);
        }
        else if (y > 0) {
            digitalWrite(cw, HIGH);
            digitalWrite(ccw, LOW);
        }
        else if (y == 0) {
            digitalWrite(cw, LOW);
            digitalWrite(ccw, LOW);
        }
    }

    // i think position is given as element of (-1, 1)
    else if (PWM_ENABLED) {
        if (y < 0) {
            analogWrite(ccw, -y * 255);    // 255 scales given value to the argument range for
            digitalWrite(cw, LOW);         // analogWrite (0, 255)
        }
        else if (y > 0) {
            analogWrite(cw, y * 255);
            digitalWrite(ccw, LOW);
        }
        else if (y == 0) {
            digitalWrite(cw, LOW);
            digitalWrite(ccw, LOW);
        }
    }
}
