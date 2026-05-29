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


// Setting the pins
const int CSpin = 7;
const int relayPin = 8;
const int inPin1 = 2;     // BUTTON1/SENSOR1 pin
const int inPin2 = 12;     // SENSOR2 pin
const int outPin1 = 13;      // SYNCHRO pin

// Here go all the latencies in the protocol   
const int but_delay1 = 100; // the latency in ms for the first sensor to be triggered   - !!! DETERMINES THE TIME ANIMAL SHOULD HOLD THE BAR FOR THE WATER TO DISPENSE !!!
const int but_delay2 = 1000; // the latency in ms for the second sensor to be triggered  - !!! DETERMINES THE SPEED OF THE REACTION TO THE SPOUT TOUCH !!!
const int CS_length = 10000; // the duration of the CS beep sound  
const int Frequency = 5000; // the frequency for the CS beep sound

// All other variables
const int Timing = 1; // Timing of the program in ms
unsigned long cur_time = 0;  
unsigned long lastDebounceTime1 = 0; 
const int relayTime = 500; // Time of the relay activation for Genie pump

int reading1 = 0;
int reading2 = 0;
int Speaker = 0;
int Reinforcement = 0;
int Sync = 0;

// Creating components-instances

Bounce debouncer1 = Bounce();                      // That's a debouncers used to track only continuous sensor touches (see debouncer.interval)
Bounce2::Button debouncer2 = Bounce2::Button();    // That's a debouncers used to track only continuous sensor touches (see debouncer.interval)

void setup() {
// This code runs only once once when the Device starts
  
  debouncer1.attach(inPin1, INPUT_PULLUP); // See debouncer
  debouncer1.interval(but_delay1);  // The length of staying in front
  debouncer2.attach(inPin2, INPUT_PULLUP); // See debouncer
  debouncer2.interval(but_delay2);  // The length of grabbing the bar
  debouncer2.setPressedState(LOW);


  pinMode(outPin1, OUTPUT); // Setting the inputs/outputs
  pinMode(relayPin, OUTPUT);
  pinMode(CSpin, OUTPUT);
  Serial.begin(115200);               // Starting the data logging
  
}

void loop() {
  // This code runs repeatedly and controls the experiment continuously
  debouncer1.update();            // Reinitializing the debouncers
  debouncer2.update();
  digitalWrite(relayPin, LOW);

  reading1 = debouncer1.read();   // Monitoring the inputs from Sensors
  reading2 = debouncer2.read();
  Reinforcement = 0;

  if (Speaker == 0 && Reinforcement == 0 && reading1 == 0) {  // CONDITIONED STIMULI ONSET
    tone(CSpin, Frequency);
    //digitalWrite(outPin1, HIGH); // Switching on the CS
    digitalWrite(outPin1, HIGH);  // SYNCHRO pin gets high
    Sync = 1;
    Speaker = 1;
    lastDebounceTime1 = millis();
     
    }
  
  if (Speaker == 1 ){                                       // HANDLING THE OFFSET OF CONDITIONED STIMULI 
      if ((millis() - lastDebounceTime1) > CS_length){ // WHEN TIME ELAPSES
      noTone(CSpin);                                      // Switching off the CS with time - !!! CS OFF AFTER DESIGNATED TIME !!! 
      //digitalWrite(outPin1, LOW);
      digitalWrite(outPin1, LOW);                           // SYNCHRO pin gets low
      Speaker = 0;                                          
      Sync = 0;
      }
    }

  if (reading2 == 0 && Speaker == 1){   // HANDLING THE ROTATION OF THE SYRINGE PUMP MOTOR - NOT THE BEST WAY AS THE FUNCTION IS BLOCKING, NEED TO REWRITE USING STEPPER LIBRARY IF IT PROVIDES THE SAME TORQUE OR DRIVE PATTERN AS HERE
        noTone(CSpin);
        digitalWrite(outPin1, LOW);
        Reinforcement = 1;
        Speaker = 0;                                          
        Sync = 0;

        digitalWrite(relayPin, HIGH);
        delay(relayTime);

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
      Serial.println(Sync);     // Sync
  }

}
