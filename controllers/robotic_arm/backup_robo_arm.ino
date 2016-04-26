/* TODO:
   - implemented receiving of data
   - check and correct assumptions
   - implement functionality whereby the user can change which joint they're controlling
*/

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

void setup() {
    pinMode(J_1_CW, OUTPUT);
    pinMode(J_1_CWW, OUTPUT);
    pinMode(J_2_CW, OUTPUT);
    pinMode(J_2_CWW, OUTPUT);
    pinMode(J_3_CW, OUTPUT);
    pinMode(J_3_CWW, OUTPUT);
}

// temp: assume data comes as [x, y, z] as position of joystick
// only y position (assuming forward/back on joystick) will be used to control motors
void loop() {
    int joystickPos[3] = receiveData() // funtion to be implemented once I know how data is sent
    int xPos = joystickPos[0], yPos = joystickPos[1], zPos = joystickPos[2];

    // which joint is currently being controlled, defaults to joint 1
    int cw = J_1_CW, ccw = J_1_CCW;
    // TODO: implement functionality where user presses a button on the joystick to switch joint

    // not capable of pwm, motor moves only at 1 speed regardless of angle of joystick
    if (! PWM_ENABLED) {
        if (yPos < 0) {
            digitalWrite(ccw, HIGH);     // no particular reason why I chose this combo of directions
            digitalWrite(cw, LOW);
        }
        else if (yPos > 0) {
            digitalWrite(cw, HIGH);
            digitalWrite(ccw, LOW);
        }
        else if (yPos == 0) {
            digitalWrite(cw, LOW);
            digitalWrite(ccw, LOW);
        }
    }

    // temp: assume position is given as element of (-255, 255)
    else if (PWM_ENABLED) {
        if (yPos < 0) {
            analogWrite(ccw, -yPos);
            digitalWrite(cw, LOW);
        }
        else if (yPos > 0) {
            analogWrite(cw, yPos);
            digitalWrite(ccw, LOW);
        }
        else if (yPos == 0) {
            digitalWrite(cw, LOW);
            digitalWrite(ccw, LOW);
        }
    }
}
