// REACHING TASK CONTROL PROGRAM
// This Arduino program is designed for the Simple mouse reaching task in the Dr.Chu lab by Daniil Berezhnoi, 03/28/22
// It is capable of receiving data from two Sensors - input Pins - and controlling three instances - output Pins - based
// on those readings. Upon receiving the presence signal from the Sensor 1 (inPin1) it switches ON the Conditioned Stimulus (outPin1)
// and if animal reacts to the conditioned stimulus by pressing a Sensor 2 (inPin2) it turns the Feeder Stepper motor (motorPins) and
// triggers the Gate Servo motor (CS_sync_Pin) to open the feeder. It also sends the Synchro signal (outPin3) to trigger FLIR camera and Logs
// the data in a serial port.


// Including Libraries
#include <Bounce2.h>
#include <Servo.h>
#include <Stepper.h>

#define BOUNCE_WITH_PROMPT_DETECTION

#define STEPS 200

// Setting the constants
//const int motor1Pins[] = {3, 4, 5, 6}; // Motor1 pins
const int motorPin1 = 3;
const int motorPin2 = 4;
const int motorPin3 = 5;
const int motorPin4 = 6;
const int delivery_sync_Pin = 8;
const int potpin = A7;
const int inPin1 = 2;     // BUTTON1/SENSOR1 pin
const int inPin2 = 12;     // SENSOR2 pin
const int outPin1 = 11;      // MOTOR spout attenuator pin
const int outPin2 = 9;       // NEMA motor pin1 
const int outPin3 = 10;      // NEMA motor pin2
const int CS_sync_Pin = 13;      // SYNCHRO pin
const int CSpin = 7;



// Here go all the latencies in the protocol   
const int but_delay1 = 100; // the latency in ms for the first sensor to be triggered   - !!! DETERMINES THE TIME ANIMAL SHOULD HOLD THE BAR FOR THE WATER TO DISPENSE !!!
const int but_delay2 = 1000; // the latency in ms for the second sensor to be triggered  - !!! DETERMINES THE SPEED OF THE REACTION TO THE SPOUT TOUCH !!!
const int CS_length = 10000; // the duration of the CS beep sound  
const int Frequency = 5000;

// All other variables
const int Timing = 1; // Timing of the program in ms
unsigned long cur_time = 0;  
unsigned long lastDebounceTime1 = 0; 
const int delayTime = 2; // Speed of the syringe motor
const int steps = 30; // Number of steps to control the pump
const int Number_Steps = 50; // Number of steps to control the pump (Nema)

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

Stepper stepper(STEPS, outPin2, outPin3);
#define motorInterfaceType 1

void setup() {
// This code runs only once once when the Device starts
  
  stepper.setSpeed(100);
  myServo.attach(outPin1); // Attaching the motor to the SPOUT pin
  debouncer1.attach(inPin1, INPUT_PULLUP); // See debouncer
  debouncer1.interval(but_delay1);  // The length of staying in front
  debouncer2.attach(inPin2, INPUT_PULLUP); // See debouncer
  debouncer2.interval(but_delay2);  // The length of grabbing the bar
  debouncer2.setPressedState(LOW);


  pinMode(outPin1, OUTPUT); // Setting the inputs/outputs
  pinMode(CS_sync_Pin, OUTPUT);
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorPin3, OUTPUT);
  pinMode(motorPin4, OUTPUT);
  pinMode(delivery_sync_Pin, OUTPUT);
  pinMode(CSpin, OUTPUT);
  Serial.begin(115200);               // Starting the data logging
  
}

void loop() {
  // This code runs repeatedly and controls the experiment continuously
  debouncer1.update();            // Reinitializing the debouncers
  debouncer2.update();
  digitalWrite(delivery_sync_Pin, LOW);

  reading1 = debouncer1.read();   // Monitoring the inputs from Sensors
  reading2 = debouncer2.read();
  val = analogRead(potpin);
  val = map(val, 0, 1023, 0, 180);
  myServo.write(val);               // Setting the initial possition for the spout
  Reinforcement = 0;

  if (Speaker == 0 && Reinforcement == 0 && reading1 == 0) {  // CONDITIONED STIMULI ONSET
    tone(CSpin, Frequency);
    digitalWrite(CS_sync_Pin, HIGH);  // SYNCHRO pin gets high
    Sync = 1;
    Speaker = 1;
    lastDebounceTime1 = millis();
     
    }
  
  if (Speaker == 1 ){                                       // HANDLING THE OFFSET OF CONDITIONED STIMULI 
      if ((millis() - lastDebounceTime1) > CS_length){ // WHEN TIME ELAPSES
      noTone(CSpin);                                      // Switching off the CS with time - !!! CS OFF AFTER DESIGNATED TIME !!! 
      digitalWrite(CS_sync_Pin, LOW);                           // SYNCHRO pin gets low
      Speaker = 0;                                          
      Sync = 0;
      }
    }

  if (reading2 == 0 && Speaker == 1){   // HANDLING THE ROTATION OF THE SYRINGE PUMP MOTOR - NOT THE BEST WAY AS THE FUNCTION IS BLOCKING, NEED TO REWRITE USING STEPPER LIBRARY IF IT PROVIDES THE SAME TORQUE OR DRIVE PATTERN AS HERE
        noTone(CSpin);
        digitalWrite(CS_sync_Pin, LOW);
        Reinforcement = 1;
        Speaker = 0;                                          
        Sync = 0;

        digitalWrite(delivery_sync_Pin, HIGH);
        stepper.step(Number_Steps);

        for (int x = 0; x < steps; x++) {
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
      Serial.print(val);     // Angle of the spout actuator
      Serial.print(" ");   
      Serial.println(Sync);     // Sync
  }

}
