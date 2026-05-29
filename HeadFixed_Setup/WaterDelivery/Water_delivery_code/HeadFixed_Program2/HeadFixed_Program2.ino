



// REACHING TASK CONTROL PROGRAM
// This Arduino program is designed for the Simple mouse reaching task in the Dr.Chu lab by Daniil Berezhnoi, 03/28/22
// It is capable of receiving data from two Sensors - input Pins - and controlling three instances - output Pins - based
// on those readings. Upon receiving the presence signal from the Sensor 1 (inPin1) it switches ON the Conditioned Stimulus (outPin1)
// and if animal reacts to the conditioned stimulus by pressing a Sensor 2 (inPin2) it turns the Feeder Stepper motor (motorPins) and
// triggers the Gate Servo motor (outPin2) to open the feeder. It also sends the Synchro signal (outPin3) to trigger FLIR camera and Logs
// the data in a serial port.


// Including Libraries
#include <Bounce2.h>
#include <Servo.h>
#define BOUNCE_WITH_PROMPT_DETECTION


// Setting the constants
//const int motor1Pins[] = {3, 4, 5, 6}; // Motor1 pins
const int motorPin1 = 3;
const int motorPin2 = 4;
const int motorPin3 = 5;
const int motorPin4 = 6;
const int potpin = 19;
const int motor2Pins[] = {7, 8, 9, 10}; // Motor1 pins
const int inPin1 = 2;     // BUTTON1/SENSOR1 pin
const int inPin2 = 12;     // SENSOR2 pin
const int outPin1 = 11;      // MOTOR spout attenuator pin
const int outPin2 = 13;      // SYNCHRO pin



// Here go all the latencies in the protocol   
const int but_delay1 = 1000; // the latency in ms for the first sensor to be triggered   - !!! DETERMINES THE TIME ANIMAL SHOULD HOLD THE BAR FOR THE WATER TO DISPENSE !!!
const int but_delay2 = 100; // the latency in ms for the second sensor to be triggered  - !!! DETERMINES THE SPEED OF THE REACTION TO THE SPOUT TOUCH !!!

// All other variables
const int Timing = 1; // Timing of the program in ms
const int delayTime = 2; // Speed of the syringe motor
unsigned long cur_time = 0;  

int reading1 = 0;
int reading2 = 0;
int Speaker = 0;
int Reinforcement = 0;
int Sync = 0;
int val;
int pos = 15;    // variable to store the servo position

// Creating components-instances

Servo myServo;                                     // That's a Servo motor for controling the drinking spout position
Bounce debouncer1 = Bounce();                      // That's a debouncers used to track only continuous sensor touches (see debouncer.interval)
Bounce2::Button debouncer2 = Bounce2::Button();    // That's a debouncers used to track only continuous sensor touches (see debouncer.interval)


void setup() {
// This code runs only once once when the Device starts
  
  myServo.attach(outPin1); // Attaching the motor to the SPOUT pin
  debouncer1.attach(inPin1, INPUT_PULLUP); // See debouncer
  debouncer1.interval(but_delay1);  // The length of staying in front
  debouncer2.attach(inPin2, INPUT_PULLUP); // See debouncer
  debouncer2.interval(but_delay2);  // The length of grabbing the bar
  debouncer2.setPressedState(LOW);



  pinMode(outPin1, OUTPUT); // Setting the inputs/outputs
  pinMode(outPin2, OUTPUT);
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorPin3, OUTPUT);
  pinMode(motorPin4, OUTPUT);


  Serial.begin(115200);               // Starting the data logging
  
}

void loop() {
  // This code runs repeatedly and controls the experiment continuously
  debouncer1.update();            // Reinitializing the debouncers
  debouncer2.update();

  reading1 = debouncer1.read();   // Monitoring the inputs from Sensors
  reading2 = debouncer2.read();
  val = analogRead(potpin);
  
  myServo.write(pos);               // Setting the initial possition for the gate


  Reinforcement = 0;

    if (reading1 == 0){   // HANDLING THE ROTATION OF THE SYRINGE PUMP MOTOR - NOT THE BEST WAY AS THE FUNCTION IS BLOCKING, NEED TO REWRITE USING STEPPER LIBRARY IF IT PROVIDES THE SAME TORQUE OR DRIVE PATTERN AS HERE
          Reinforcement = 1;
          digitalWrite(motorPin1, LOW);
          digitalWrite(motorPin2, LOW);
          digitalWrite(motorPin3, LOW);
          digitalWrite(motorPin4, HIGH);
          delay(delayTime);
          digitalWrite(motorPin1, LOW);
          digitalWrite(motorPin2, LOW);
          digitalWrite(motorPin3, HIGH);
          digitalWrite(motorPin4, HIGH);
          delay(delayTime);
          digitalWrite(motorPin1, LOW);
          digitalWrite(motorPin2, LOW);
          digitalWrite(motorPin3, HIGH);
          digitalWrite(motorPin4, LOW);
          delay(delayTime);
          digitalWrite(motorPin1, LOW);
          digitalWrite(motorPin2, HIGH);
          digitalWrite(motorPin3, HIGH);
          digitalWrite(motorPin4, LOW);
          delay(delayTime);
          digitalWrite(motorPin1, LOW);
          digitalWrite(motorPin2, HIGH);
          digitalWrite(motorPin3, LOW);
          digitalWrite(motorPin4, LOW);
          delay(delayTime);
          digitalWrite(motorPin1, HIGH);
          digitalWrite(motorPin2, HIGH);
          digitalWrite(motorPin3, LOW);
          digitalWrite(motorPin4, LOW);
          delay(delayTime);
          digitalWrite(motorPin1, HIGH);
          digitalWrite(motorPin2, LOW);
          digitalWrite(motorPin3, LOW);
          digitalWrite(motorPin4, LOW);
          delay(delayTime);
          digitalWrite(motorPin1, HIGH);
          digitalWrite(motorPin2, LOW);
          digitalWrite(motorPin3, LOW);
          digitalWrite(motorPin4, HIGH);
          delay(delayTime);
    }

    if (reading2 == 0 ){   // HANDLING THE ROTATION OF THE FEEDER

          
    }


    if ((millis() - cur_time) > Timing){                                                                              // LOGGING THE DATA
        cur_time = millis(); // Getting Timestamp from the beginning of the program
        Serial.print(cur_time);   // Timestamp
        Serial.print(" ");   
        Serial.print(reading1);   // Sensor1
        Serial.print(" ");   
        Serial.print(reading2);   // Sensor2
        Serial.print(" ");   
        Serial.print(Reinforcement);     // Reinforcement
        Serial.print(" ");   
        Serial.print(val);     // Reinforcement
        Serial.print(" ");   
        Serial.println(Sync);     // Sync
    }

}
