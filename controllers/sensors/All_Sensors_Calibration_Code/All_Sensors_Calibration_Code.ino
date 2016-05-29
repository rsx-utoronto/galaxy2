/********************
Compiling all sensors codes
Analog Inputs:
A0 - Moisture Sensor A
A1 - MQ-8 (H2) Sensor
A2 - MQ-4 (CH4) Sensor
A3 - Moisture Sensor B
********************/
/******************************************
 MQ-4(CH4) Sensor Macro Definition Begin:
******************************************/
/*******************Demo for MQ-8 Gas Sensor Module V1.0 Modified for MQ-4*****************************
Contact: support[at]sandboxelectronics.com

Lisence: Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0)

Note:    This piece of source code is supposed to be used as a demostration ONLY. More
         sophisticated calibration is required for industrial field application. 

                                                    Sandbox Electronics    2014-02-03
************************************************************************************/

/************************Hardware Related Macros************************************/
#define         CH4_MQ_PIN                       (2)     //define which analog input channel you are going to use
#define         CH4_RL_VALUE                     (20)    //define the load resistance on the board, in kilo ohms
#define         CH4_RO_CLEAN_AIR_FACTOR          (9.21)  //RO_CLEAR_AIR_FACTOR=(Sensor resistance in clean air)/RO,
                                                     //which is derived from the chart in datasheet

/***********************Software Related Macros************************************/
#define         CALIBARAION_SAMPLE_TIMES     (50)    //define how many samples you are going to take in the calibration phase
#define         CALIBRATION_SAMPLE_INTERVAL  (500)   //define the time interal(in milisecond) between each samples in the
                                                     //cablibration phase
#define         READ_SAMPLE_INTERVAL         (50)    //define how many samples you are going to take in normal operation
#define         READ_SAMPLE_TIMES            (5)     //define the time interal(in milisecond) between each samples in 
                                                     //normal operation

/**********************Application Related Macros**********************************/
#define         GAS_CH4                      (0)

/*****************************Globals***********************************************/
float           CH4Curve[3]  =  {2.3, 0.26,-0.35};    //two points are taken from the curve in datasheet. 
                                                     //with these two points, a line is formed which is "approximately equivalent" 
                                                     //to the original curve. 
                                                     //MQ-8:data format:{ x, y, slope}; point1: (lg200, lg8.5), point2: (lg10000, lg0.03) 
                                                     //MQ-4:data format:{ x, y, slope}; point1: (lg200, lg1.8), point2: (lg10000, lg0.45)

float           CH4_Ro           =  20;                  //CH4_Ro is initialized to 20 kilo ohms


/********************************************************************************
*********************************************************************************/
/******************************************
 MQ-4(CH4) Sensor Macro Definition End
******************************************/
/******************************************
 MQ-8(H2) Sensor Macro Defintion Begin:
******************************************/

/*******************Demo for MQ-8 Gas Sensor Module V1.0*****************************
Contact: support[at]sandboxelectronics.com

Lisence: Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0)

Note:    This piece of source code is supposed to be used as a demostration ONLY. More
         sophisticated calibration is required for industrial field application. 

                                                    Sandbox Electronics    2014-02-03
************************************************************************************/

/************************Hardware Related Macros************************************/
#define         MQ_PIN                       (1)     //define which analog input channel you are going to use
#define         RL_VALUE                     (10)    //define the load resistance on the board, in kilo ohms
#define         RO_CLEAN_AIR_FACTOR          (9.21)  //RO_CLEAR_AIR_FACTOR=(Sensor resistance in clean air)/RO,
                                                     //which is derived from the chart in datasheet

/***********************Software Related Macros************************************/
#define         CALIBARAION_SAMPLE_TIMES     (50)    //define how many samples you are going to take in the calibration phase
#define         CALIBRATION_SAMPLE_INTERVAL  (500)   //define the time interal(in milisecond) between each samples in the
                                                     //cablibration phase
#define         READ_SAMPLE_INTERVAL         (50)    //define how many samples you are going to take in normal operation
#define         READ_SAMPLE_TIMES            (5)     //define the time interal(in milisecond) between each samples in 
                                                     //normal operation

/**********************Application Related Macros**********************************/
#define         GAS_H2                      (0)

/*****************************Globals***********************************************/
float           H2Curve[3]  =  {2.3, 0.93,-1.44};    //two points are taken from the curve in datasheet. 
                                                     //with these two points, a line is formed which is "approximately equivalent" 
                                                     //to the original curve. 
                                                     //data format:{ x, y, slope}; point1: (lg200, lg8.5), point2: (lg10000, lg0.03) 

float           Ro           =  10;                  //Ro is initialized to 10 kilo ohms



/********************************************************************************
*********************************************************************************/
/******************************************
 MQ-8(H2) Sensor Macro Definition End
******************************************/

void setup()
{  
  //Printing  MQ-4(CH4) Sensor Calibration
  Serial.begin(9600);                                //UART setup, baudrate = 9600bps
  Serial.print("Calibrating CH4Sensor...\n");                
  CH4_Ro = CH4_MQCalibration(CH4_MQ_PIN);            //Calibrating the sensor. Please make sure the sensor is in clean air 
                                                     //when you perform the calibration                    
  Serial.print("Calibration (CH4Sensor) is done...\n"); 
  Serial.print("CH4_Ro=");
  Serial.print(CH4_Ro);
  Serial.print("kohm");
  Serial.print("\n");
  
  //Printing  MQ-8(H2) Sensor Calibration
  Serial.print("Calibrating H2Sensor...\n");                
  Ro = MQCalibration(MQ_PIN);                        //Calibrating the sensor. Please make sure the sensor is in clean air 
                                                     //when you perform the calibration                    
  Serial.print("Calibration (H2Sensor) is done...\n"); 
  Serial.print("H2_Ro=");
  Serial.print(Ro);
  Serial.print("kohm");
  Serial.print("\n");
  
  //Moisture Sensor A Setup  
  pinMode(A0, INPUT); //set up analog pin 0 to be input
  //Moisture Sensor B Setup  
  pinMode(A3, INPUT); //set up analog pin 3 to be input
}

void loop()
{
   //CH4 Sensor
   Serial.print("CH4:"); 
   Serial.print(CH4_MQGetGasPercentage(CH4_MQRead(CH4_MQ_PIN)/CH4_Ro,GAS_CH4) );
   Serial.print( "ppm" );
   Serial.print("\n");
   //H2 Sensor
   Serial.print("H2:"); 
   Serial.print(MQGetGasPercentage(MQRead(MQ_PIN)/Ro,GAS_H2) );
   Serial.print( "ppm" );
   Serial.print("\n");
   //Soil Moisture Sensor A
   int s = analogRead(A0); //take a sample
   Serial.print(s); Serial.print(" - ");
   
   if(s >= 1000) {
    Serial.println("Sensor A is not in the Soil or DISCONNECTED");
   }
   if(s < 1000 && s >= 600) { 
    Serial.println("Soil A is DRY");
   }
   if(s < 600 && s >= 370) {
    Serial.println("Soil A is HUMID"); 
   }
   if(s < 370) {
    Serial.println("Sensor A in WATER");
   }
   //Soil Moisture Sensor B
   int t = analogRead(A3); //take a sample
   Serial.print(t); Serial.print(" - ");
   
   if(t >= 1000) {
    Serial.println("Sensor B is not in the Soil or DISCONNECTED");
   }
   if(t < 1000 && t >= 600) { 
    Serial.println("Soil B is DRY");
   }
   if(t < 600 && t >= 370) {
    Serial.println("Soil B is HUMID"); 
   }
   if(t < 370) {
    Serial.println("Sensor B in WATER");
   }
   Serial.println("\n");
   delay(1500);
}


/******************************************
 MQ-4(CH4) Sensor Functions Begin:
******************************************/
/****************** CH4_MQResistanceCalculation ****************************************
Input:   raw_adc - raw value read from adc, which represents the voltage
Output:  the calculated sensor resistance
Remarks: The sensor and the load resistor forms a voltage divider. Given the voltage
         across the load resistor and its resistance, the resistance of the sensor
         could be derived.
************************************************************************************/ 
float CH4_MQResistanceCalculation(int raw_adc)
{
  return ( ((float)CH4_RL_VALUE*(1023-raw_adc)/raw_adc));
}

/***************************** CH4_MQCalibration ****************************************
Input:   mq_pin - analog channel
Output:  CH4_Ro of the sensor
Remarks: This function assumes that the sensor is in clean air. It use  
         CH4_MQResistanceCalculation to calculates the sensor resistance in clean air 
         and then divides it with CH4_RO_CLEAN_AIR_FACTOR. CH4_RO_CLEAN_AIR_FACTOR is about 
         10, which differs slightly between different sensors.
************************************************************************************/ 
float CH4_MQCalibration(int mq_pin)
{
  int i;
  float val=0;

  for (i=0;i<CALIBARAION_SAMPLE_TIMES;i++) {            //take multiple samples
    val += CH4_MQResistanceCalculation(analogRead(mq_pin));
    delay(CALIBRATION_SAMPLE_INTERVAL);
  }
  val = val/CALIBARAION_SAMPLE_TIMES;                   //calculate the average value

  val = val/CH4_RO_CLEAN_AIR_FACTOR;                        //divided by CH4_RO_CLEAN_AIR_FACTOR yields the CH4_Ro 
                                                        //according to the chart in the datasheet 

  return val; 
}
/*****************************  CH4_MQRead *********************************************
Input:   mq_pin - analog channel
Output:  Rs of the sensor
Remarks: This function use CH4_MQResistanceCalculation to caculate the sensor resistenc (Rs).
         The Rs changes as the sensor is in the different consentration of the target
         gas. The sample times and the time interval between samples could be configured
         by changing the definition of the macros.
************************************************************************************/ 
float CH4_MQRead(int mq_pin)
{
  int i;
  float rs=0;

  for (i=0;i<READ_SAMPLE_TIMES;i++) {
    rs += CH4_MQResistanceCalculation(analogRead(mq_pin));
    delay(READ_SAMPLE_INTERVAL);
  }

  rs = rs/READ_SAMPLE_TIMES;

  return rs;  
}

/*****************************  CH4_MQGetGasPercentage **********************************
Input:   rs_ro_ratio - Rs divided by CH4_Ro
         gas_id      - target gas type
Output:  ppm of the target gas
Remarks: This function passes different curves to the CH4_MQGetPercentage function which 
         calculates the ppm (parts per million) of the target gas.
************************************************************************************/ 
int CH4_MQGetGasPercentage(float rs_ro_ratio, int gas_id)
{
  if ( gas_id == GAS_CH4) {
     return CH4_MQGetPercentage(rs_ro_ratio,CH4Curve);
  }  
  return 0;
}

/*****************************  CH4_MQGetPercentage **********************************
Input:   rs_ro_ratio - Rs divided by CH4_Ro
         pcurve      - pointer to the curve of the target gas
Output:  ppm of the target gas
Remarks: By using the slope and a point of the line. The x(logarithmic value of ppm) 
         of the line could be derived if y(rs_ro_ratio) is provided. As it is a 
         logarithmic coordinate, power of 10 is used to convert the result to non-logarithmic 
         value.
************************************************************************************/ 
int  CH4_MQGetPercentage(float rs_ro_ratio, float *pcurve)
{
  return (pow(10,( ((log(rs_ro_ratio)-pcurve[1])/pcurve[2]) + pcurve[0])));
}

/******************************************
 MQ-4(CH4) Sensor Functions End
******************************************/

/******************************************
 H2 Sensor Functions Begin:
******************************************/

/****************** MQResistanceCalculation ****************************************
Input:   raw_adc - raw value read from adc, which represents the voltage
Output:  the calculated sensor resistance
Remarks: The sensor and the load resistor forms a voltage divider. Given the voltage
         across the load resistor and its resistance, the resistance of the sensor
         could be derived.
************************************************************************************/ 
float MQResistanceCalculation(int raw_adc)
{
  return ( ((float)RL_VALUE*(1023-raw_adc)/raw_adc));
}

/***************************** MQCalibration ****************************************
Input:   mq_pin - analog channel
Output:  Ro of the sensor
Remarks: This function assumes that the sensor is in clean air. It use  
         MQResistanceCalculation to calculates the sensor resistance in clean air 
         and then divides it with RO_CLEAN_AIR_FACTOR. RO_CLEAN_AIR_FACTOR is about 
         10, which differs slightly between different sensors.
************************************************************************************/ 
float MQCalibration(int mq_pin)
{
  int i;
  float val=0;

  for (i=0;i<CALIBARAION_SAMPLE_TIMES;i++) {            //take multiple samples
    val += MQResistanceCalculation(analogRead(mq_pin));
    delay(CALIBRATION_SAMPLE_INTERVAL);
  }
  val = val/CALIBARAION_SAMPLE_TIMES;                   //calculate the average value

  val = val/RO_CLEAN_AIR_FACTOR;                        //divided by RO_CLEAN_AIR_FACTOR yields the Ro 
                                                        //according to the chart in the datasheet 

  return val; 
}
/*****************************  MQRead *********************************************
Input:   mq_pin - analog channel
Output:  Rs of the sensor
Remarks: This function use MQResistanceCalculation to caculate the sensor resistenc (Rs).
         The Rs changes as the sensor is in the different consentration of the target
         gas. The sample times and the time interval between samples could be configured
         by changing the definition of the macros.
************************************************************************************/ 
float MQRead(int mq_pin)
{
  int i;
  float rs=0;

  for (i=0;i<READ_SAMPLE_TIMES;i++) {
    rs += MQResistanceCalculation(analogRead(mq_pin));
    delay(READ_SAMPLE_INTERVAL);
  }

  rs = rs/READ_SAMPLE_TIMES;

  return rs;  
}

/*****************************  MQGetGasPercentage **********************************
Input:   rs_ro_ratio - Rs divided by Ro
         gas_id      - target gas type
Output:  ppm of the target gas
Remarks: This function passes different curves to the MQGetPercentage function which 
         calculates the ppm (parts per million) of the target gas.
************************************************************************************/ 
int MQGetGasPercentage(float rs_ro_ratio, int gas_id)
{
  if ( gas_id == GAS_H2) {
     return MQGetPercentage(rs_ro_ratio,H2Curve);
  }  
  return 0;
}

/*****************************  MQGetPercentage **********************************
Input:   rs_ro_ratio - Rs divided by Ro
         pcurve      - pointer to the curve of the target gas
Output:  ppm of the target gas
Remarks: By using the slope and a point of the line. The x(logarithmic value of ppm) 
         of the line could be derived if y(rs_ro_ratio) is provided. As it is a 
         logarithmic coordinate, power of 10 is used to convert the result to non-logarithmic 
         value.
************************************************************************************/ 
int  MQGetPercentage(float rs_ro_ratio, float *pcurve)
{
  return (pow(10,( ((log(rs_ro_ratio)-pcurve[1])/pcurve[2]) + pcurve[0])));
}

/******************************************
 H2 Sensor Functions Ends
******************************************/

