// REACHING TASK CONTROL PROGRAM
// This Arduino program is designed for the Simple mouse reaching task in the Dr.Chu lab by Daniil Berezhnoi, 03/28/22
// It is capable of receiving data from two Sensors - input Pins - and controlling three instances - output Pins - based
// on those readings. Upon receiving the presence signal from the Sensor 1 (inPin1) it switches ON the Conditioned Stimulus (outPin1)
// and if animal reacts to the conditioned stimulus by pressing a Sensor 2 (inPin2) it turns the Feeder Stepper motor (motorPins) and
// triggers the Gate Servo motor (outPin2) to open the feeder. It also sends the Synchro signal (outPin3) to trigger FLIR camera and Logs
// the data in a serial port.


// Including Libraries
#include <Bounce2.h>
#include <Stepper.h>
#include <Servo.h>
#define BOUNCE_WITH_PROMPT_DETECTION

// Setting the constants
const int stepsPerRevolution = 2048;  // Change this to fit the number of steps per revolution if you are using the motor different from 28BYJ-48
const int motorPins[] = {2, 4, 3, 5}; // Feeder pins
const int inPin1 = 9;     // SENSOR1 pin
const int inPin2 = 10;     // SENSOR2 pin
const int inPin3 = 8;      // SENSOR3 pin
const char inPin4 = A0;     // FLIR_SYNC_PIN
const int ButPin1 = A1;     // SENSOR2 pin
const int ButPin2 = A2;     // SENSOR2 pin

const int outPin1 = 6;      // SPEAKER pin
const int outPin2 = 7;      // GATE pin
const int outPin3 = 12;      // SYNCHRO pin
const int outPin4 = 13;     // TICKING pin

// Here go all the latencies in the protocol   
const int debounceDelay3 = 1000; // the duration of the Food availability
const int but_delay1 = 500; // the latency in ms for the first sensor to be triggered   - !!! DETERMINES THE TIME ANIMAL SHOULD STAY IN FRONT !!!
const int but_delay2 = 100; // the latency in ms for the second sensor to be triggered  - !!! DETERMINES THE TIME ANIMAL SHOULD HOLD THE BAR !!!

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
Stepper myStepper(stepsPerRevolution, motorPins[0], motorPins[1], motorPins[2], motorPins[3]); // That's a Feeder motor and Pins it's connected to
Servo myServo;                                     // That's a Servo motor for controling the door
Bounce debouncer1 = Bounce();                      // That's a debouncers used to track only continuous sensor touches (see debouncer.interval)
Bounce2::Button debouncer2 = Bounce2::Button();    // That's a debouncers used to track only continuous sensor touches (see debouncer.interval)
Bounce debouncer3 = Bounce();
Bounce debouncer4 = Bounce();

void setup() {
// This code runs only once once when the Device starts
  myStepper.setSpeed(5); // Speed for the stepper motor, controling feeder.         !!! CAN BE ADJUSTED !!!
  myServo.attach(outPin2); // Attaching the gate to the GATE pin
  
  pinMode(outPin1, OUTPUT); // Setting the inputs/outputs
  pinMode(outPin2, OUTPUT);
  pinMode(outPin3, OUTPUT);
  pinMode(outPin4, OUTPUT);
  pinMode(inPin3, INPUT_PULLUP);
  debouncer1.attach(inPin1, INPUT_PULLUP); // See debouncer
  debouncer1.interval(but_delay1);  // The length of staying in front
  debouncer2.attach(inPin2, INPUT_PULLUP); // See debouncer
  debouncer2.interval(but_delay2);  // The length of grabbing the bar
  debouncer2.setPressedState(LOW);
  debouncer3.attach(ButPin1, INPUT_PULLUP); // See debouncer - Button for the feeder rotation
  debouncer3.interval(50);  
  debouncer4.attach(ButPin2, INPUT_PULLUP); // See debouncer - Button for the feeder rotation
  debouncer4.interval(50);  
  Serial.begin(115200);               // Starting the data logging
  digitalWrite(outPin1, LOW);
  myServo.write(pos);               // Setting the initial possition for the gate
}

void loop() {
  // This code runs repeatedly and controls the experiment continuously
  digitalWrite(outPin4, HIGH);    // Tick when the code starts
  debouncer1.update();            // Reinitializing the debouncers
  debouncer2.update();
  debouncer3.update();
  debouncer4.update();
  reading1 = debouncer1.read();   // Monitoring the inputs from Sensors
  reading2 = debouncer2.read();
  reading3 = digitalRead(inPin3);
  reading4 = analogRead(inPin4);  // Monitoring the input from FLIR  

  but1_reading = debouncer3.read();   // Monitoring the inputs from buttons
  but2_reading = debouncer4.read();
  
  Reinforcement = 0;

    if (reading2 == 0 && Reinforcement == 0){    // WHEN THE BAR IS PRESSED                                                                        
          Sync = 1;
          digitalWrite(outPin3, HIGH);  // SYNCHRO pin gets high         
          }

          
    if (reading2 == 1 && Reinforcement == 0 && (millis() - lastDebounceTime2) > debounceDelay3){    // WHEN THE BAR IS PRESSED                                                                        
          Sync = 0;
          digitalWrite(outPin3, LOW);  // SYNCHRO pin gets high         
          }

    if (but2_reading == 0 && (millis() - lastDebounceTime2) > debounceDelay3){   // HANDLING THE ROTATION OF THE FEEDER
          Reinforcement = 1;
          myStepper.step(stepsPerRevolution/16);          // One step of the Stepper motor        - !!! FEEDER TURNS !!!
          lastDebounceTime2 = millis(); 
    }

    if (but1_reading == 0 && (millis() - lastDebounceTime2) > debounceDelay3){   // HANDLING THE ROTATION OF THE FEEDER
          Reinforcement = 1;
          myStepper.step(-stepsPerRevolution/16);          // One step of the Stepper motor        - !!! FEEDER TURNS !!!
          lastDebounceTime2 = millis(); 
    }

    


    if ((millis() - cur_time) > Timing){                                                                              // LOGGING THE DATA
        cur_time = millis(); // Getting Timestamp from the beginning of the program
        digitalWrite(outPin4, LOW);    // Tick when the code ends
        Serial.print(cur_time);   // Timestamp
        Serial.print(" ");   
        Serial.print(reading1);   // Sensor1
        Serial.print(" ");   
        Serial.print(Speaker);    // Speaker
        Serial.print(" ");   
        Serial.print(reading2);   // Sensor2
        Serial.print(" "); 
        Serial.print(reading3);   // Sensor3
        Serial.print(" ");
        Serial.print(reading4);   // FLIR
        Serial.print(" ");   
        Serial.print(Gate);     // Gate
        Serial.print(" ");   
        Serial.print(Reinforcement);     // Reinforcement
        Serial.print(" ");   
        Serial.println(Sync);     // Sync
    }

}
