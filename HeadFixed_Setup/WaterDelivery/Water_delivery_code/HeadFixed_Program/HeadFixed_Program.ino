



// REACHING TASK CONTROL PROGRAM
// This Arduino program is designed for the Simple mouse reaching task in the Dr.Chu lab by Daniil Berezhnoi, 03/28/22
// It is capable of receiving data from two Sensors - input Pins - and controlling three instances - output Pins - based
// on those readings. Upon receiving the presence signal from the Sensor 1 (inPin1) it switches ON the Conditioned Stimulus (outPin1)
// and if animal reacts to the conditioned stimulus by pressing a Sensor 2 (inPin2) it turns the Feeder Stepper motor (motorPins) and
// triggers the Gate Servo motor (outPin2) to open the feeder. It also sends the Synchro signal (outPin3) to trigger FLIR camera and Logs
// the data in a serial port.


// Including Libraries
#include <Bounce2.h>
#include <AccelStepper.h>
#include <MultiStepper.h>
#include <Servo.h>
#define BOUNCE_WITH_PROMPT_DETECTION
#define HALFSTEP 8

// Setting the constants
const int steps = 1024;  // Change this to fit the number of steps per revolution if you are using the motor different from 28BYJ-48
const int motor1Pins[] = {3, 4, 5, 6}; // Motor1 pins
const int motor2Pins[] = {7, 8, 9, 10}; // Motor1 pins
const int inPin1 = 2;     // BUTTON1/SENSOR1 pin
const int inPin2 = 12;     // SENSOR2 pin
const int outPin1 = 11;      // MOTOR spout pin
const int outPin2 = 13;      // SYNCHRO pin


// Here go all the latencies in the protocol   
const int but_delay1 = 500; // the latency in ms for the first sensor to be triggered   - !!! DETERMINES THE TIME ANIMAL SHOULD STAY IN FRONT !!!
const int but_delay2 = 500; // the latency in ms for the second sensor to be triggered  - !!! DETERMINES THE TIME ANIMAL SHOULD HOLD THE BAR !!!
const int debounceDelay3 = 500;

// All other variables
const int Timing = 1; // Timing of the program in ms
unsigned long cur_time = 0;  
unsigned long lastDebounceTime2 = 0; 
int reading1 = 0;
int reading2 = 0;
int reading3 = 0;
int reading4 = 0;
int but1_reading = 0;
int but2_reading = 0;
int Speaker = 0;
int Gate = 1;
int Reinforcement = 0;
int Sync = 0;
int pos = 15;    // variable to store the servo position

// Creating components-instances
AccelStepper myStepper1(AccelStepper::FULL4WIRE, motor1Pins[0], motor1Pins[1], motor1Pins[2], motor1Pins[3]); // That's a Feeder motor and Pins it's connected to
AccelStepper myStepper2(AccelStepper::FULL4WIRE, motor2Pins[0], motor2Pins[1], motor2Pins[2], motor2Pins[3]); // That's a Feeder motor and Pins it's connected to

Servo myServo;                                     // That's a Servo motor for controling the door
Bounce debouncer1 = Bounce();                      // That's a debouncers used to track only continuous sensor touches (see debouncer.interval)
Bounce2::Button debouncer2 = Bounce2::Button();    // That's a debouncers used to track only continuous sensor touches (see debouncer.interval)
Bounce debouncer3 = Bounce();
Bounce debouncer4 = Bounce();

void setup() {
// This code runs only once once when the Device starts

  

  myServo.attach(outPin1); // Attaching the motor to the SPOUT pin
  
  pinMode(outPin1, OUTPUT); // Setting the inputs/outputs
  pinMode(outPin2, OUTPUT);
  debouncer1.attach(inPin1, INPUT_PULLUP); // See debouncer
  debouncer1.interval(but_delay1);  // The length of staying in front
  debouncer2.attach(inPin2, INPUT_PULLUP); // See debouncer
  debouncer2.interval(but_delay2);  // The length of grabbing the bar
  debouncer2.setPressedState(LOW);  
  Serial.begin(115200);               // Starting the data logging
  myServo.write(pos);               // Setting the initial possition for the gate
}

void loop() {
  // This code runs repeatedly and controls the experiment continuously
  debouncer1.update();            // Reinitializing the debouncers
  debouncer2.update();

  reading1 = debouncer1.read();   // Monitoring the inputs from Sensors
  reading2 = debouncer2.read();
  
  Reinforcement = 0;


  myStepper1.move(steps);          // One step of the Stepper motor        - !!! FEEDER TURNS !!!

  myStepper2.move(steps);          // One step of the Stepper motor        - !!! FEEDER TURNS !!!
  
  myStepper1.run();
  myStepper2.run();

    if (but2_reading == 0 && (millis() - lastDebounceTime2) > debounceDelay3){   // HANDLING THE ROTATION OF THE FEEDER
          Reinforcement = 1;
          

          lastDebounceTime2 = millis(); 
    }

    if (but1_reading == 0 && (millis() - lastDebounceTime2) > debounceDelay3){   // HANDLING THE ROTATION OF THE FEEDER
          Reinforcement = 1;
          myStepper1.moveTo(steps);          // One step of the Stepper motor        - !!! FEEDER TURNS !!!
          myStepper2.moveTo(steps);          // One step of the Stepper motor        - !!! FEEDER TURNS !!!
          
          lastDebounceTime2 = millis(); 
    }


    if ((millis() - cur_time) > Timing){                                                                              // LOGGING THE DATA
        cur_time = millis(); // Getting Timestamp from the beginning of the program
        Serial.print(cur_time);   // Timestamp
        Serial.print(" ");   
        Serial.print(reading1);   // Sensor1
        Serial.print(" ");   
        Serial.print(Speaker);    // Speaker
        Serial.print(" ");   
        Serial.print(reading2);   // Sensor2
        Serial.print(" "); 
        Serial.print(Gate);     // Gate
        Serial.print(" ");   
        Serial.print(Reinforcement);     // Reinforcement
        Serial.print(" ");   
        Serial.println(Sync);     // Sync
    }

}
