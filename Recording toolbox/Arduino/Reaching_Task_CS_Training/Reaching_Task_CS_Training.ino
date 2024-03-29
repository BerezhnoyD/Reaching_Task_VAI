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

const int outPin1 = 6;      // SPEAKER pin
const int outPin2 = 7;      // GATE pin
const int outPin3 = 12;      // SYNCHRO pin
const int outPin4 = 13;     // TICKING pin

// Here go all the latencies in the protocol                                                            !!! CAN BE ADJUSTED !!!
const int but_delay1 = 200; // the latency in ms for the first sensor to be triggered   - !!! DETERMINES THE TIME ANIMAL SHOULD STAY IN FRONT !!!
const int but_delay2 = 500; // the latency in ms for the second sensor to be triggered  - !!! DETERMINES THE TIME ANIMAL SHOULD HOLD THE BAR !!!
const int debounceDelay1 = 5000; // the duration of the CS beep sound                   - !!! DETERMINES THE DURATION OF THE SOUND !!!
const int debounceDelay2 = 0; // the latent period after Bar press and before Food    - !!! DETERMINES THE LATENCY BEFORE GATE OPEN !!!
const int debounceDelay3 = 5000; // the duration of the Food availability               - !!! DETERMINES THE TIME GATE REMAINS OPEN !!!
const int debounceDelay4 = 5000; // the duration of the Intertrial interval             - !!! DETERMINES THE INTERTRIAL INTERVAL !!!
const int Frequency = 5000; // Frequency of the buzzer sound in Hertz                   - !!! DETERMINES THE SOUND FREQUENCY !!!

// All other variables
const int Timing = 10; // Timing of the program
unsigned long cur_time = 0;  
unsigned long lastDebounceTime1 = 0;   
unsigned long lastDebounceTime2 = 0;
unsigned long lastDebounceTime3 = 0;      
int reading1 = 0;
int reading2 = 0;
int Speaker = 0;
int Gate = 0;
int Reinforcement = 0;
int Sync = 0;
int pos = 45;    // variable to store the servo position

// Creating components-instances
Stepper myStepper(stepsPerRevolution, motorPins[0], motorPins[1], motorPins[2], motorPins[3]); // That's a Feeder motor and Pins it's connected to
Servo myServo;                                     // That's a Servo motor for controling the door
Bounce debouncer1 = Bounce();                      // That's a debouncers used to track only continuous sensor touches (see debouncer.interval)
Bounce2::Button debouncer2 = Bounce2::Button();    // That's a debouncers used to track only continuous sensor touches (see debouncer.interval)

void setup() {
// This code runs only once once when the Device starts
  myStepper.setSpeed(2); // Speed for the stepper motor, controling feeder.         !!! CAN BE ADJUSTED !!!
  myServo.attach(outPin2); // Attaching the gate to the GATE pin
  
  pinMode(outPin1, OUTPUT); // Setting the inputs/outputs
  pinMode(outPin2, OUTPUT);
  pinMode(outPin3, OUTPUT);
  pinMode(outPin4, OUTPUT);
  debouncer1.attach(inPin1, INPUT_PULLUP); // See debouncer
  debouncer1.interval(but_delay1);  // The length of staying in front
  debouncer2.attach(inPin2, INPUT_PULLUP); // See debouncer
  debouncer2.interval(but_delay2);  // The length of grabbing the bar
  debouncer2.setPressedState(LOW);
  Serial.begin(115200);               // Starting the data logging
  digitalWrite(outPin1, LOW);
  myServo.write(pos);               // Setting the initial possition for the gate
}

void loop() {
  // This code runs repeatedly and controls the experiment continuously
  digitalWrite(outPin4, HIGH);    // Tick when the code starts
  debouncer1.update();            // Reinitializing the debouncers
  debouncer2.update();
  reading1 = debouncer1.read();   // Monitoring the inputs from Sensors
  reading2 = debouncer2.read();


  if (Speaker == 0 && Reinforcement == 0 && reading1 == 0 && (millis() - lastDebounceTime3) > debounceDelay4) {  // CONDITIONED STIMULI ONSET
    tone(outPin1, Frequency);
    //digitalWrite(outPin1, HIGH); // Switching on the CS
    digitalWrite(outPin3, HIGH);  // SYNCHRO pin gets high
    Sync = 1;
    Speaker = 1;
    lastDebounceTime1 = millis();
     
    }
  
  if (Speaker == 1 ){                                       // HANDLING THE OFFSET OF CONDITIONED STIMULI 
      if ((millis() - lastDebounceTime1) > debounceDelay1){ // WHEN TIME ELAPSES
      noTone(outPin1);                                      // Switching off the CS with time - !!! CS OFF AFTER DESIGNATED TIME !!! 
      //digitalWrite(outPin1, LOW);
      digitalWrite(outPin3, LOW);                           // SYNCHRO pin gets low
      Speaker = 0;                                          
      Sync = 0;
      lastDebounceTime3 = millis();
      }
      if (debouncer2.pressed() && Reinforcement == 0){      // WHEN THE BAR IS PRESSED
      noTone(outPin1);                                      // Switching off the CS
      //digitalWrite(outPin1, LOW);
      Speaker = 0;                                          
      Reinforcement = 1;
      lastDebounceTime2 = millis();         
      }
    }

  if (Reinforcement == 1 && (millis() - lastDebounceTime2) > debounceDelay2){   // HANDLING THE OPENING OF THE GATE
          Reinforcement = 2;
          myStepper.step(stepsPerRevolution/16);          // One step of the Stepper motor        - !!! FEEDER TURNS !!!
          for (pos = 45; pos >= 15; pos -= 1) {          //    - !!! DOOR OPENS !!!
            myServo.write(pos);                           // tell servo to go to position in variable 'pos'    
            }
          lastDebounceTime2 = millis();
          Gate = 1;  
          }

  if (Gate == 1 && (millis() - lastDebounceTime2) > debounceDelay3){            // HANDLING THE CLOSING OF THE GATE
          Reinforcement = 0;
          for (pos = 15; pos <= 45; pos += 1) {          //      - !!! DOOR CLOSES !!!
            myServo.write(pos);                           // tell servo to go to position in variable 'pos'
            }
          lastDebounceTime3 = millis();
          digitalWrite(outPin3, LOW);
          Gate = 0;
          Sync = 0;          
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
        Serial.print(Gate);     // Gate
        Serial.print(" ");
        Serial.print(Reinforcement);     // Gate
        Serial.print(" ");   
        Serial.println(Sync);     // Sync
    }

}
