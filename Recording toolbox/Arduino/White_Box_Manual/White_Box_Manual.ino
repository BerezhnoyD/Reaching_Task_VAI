#include <VarSpeedServo.h>
#include <Bounce2.h>

const int outPin1 = 11;    // Servo pin for the Feeder
const int outPin2 = 2;     // Servo pin for the Door
const int ButPin = 12;     // Button pin for the Control
const int LedPin = 3;       // Ledd pin for the signal led
int reading1 = 0;
const int Timing = 10; // Timing of the program in ms
const int Stay_UP = 5000; // the duration of the Food availability
const int position_up = 95;   // precise value for the upper position of the feeder 100-original during check, but too high
const int position_down = 40;  // precise value for the down position of the feeder
unsigned long cur_time = 0;  
const int but_delay1 = 50; //
int pos;
int speed1 = 30;               // speed to go up
int speed2 = 10;               // speed to go down
unsigned long Up_Time = 0;     

VarSpeedServo Feeder;                     // That's a Servo motor for controling the feeder
Bounce debouncer1 = Bounce();             // That's a Bounce instance for the button press

void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);
pos = position_down;
Feeder.attach(outPin1);           // Attaching the servo to the FEEDER pin
Feeder.write(pos);                // Going to upper position
pinMode(LedPin, OUTPUT);
debouncer1.attach(ButPin, INPUT_PULLUP); // See debouncer
debouncer1.interval(but_delay1);  // The length of staying in front
}

void loop() {
debouncer1.update();            // Reinitializing the debouncers
reading1 = debouncer1.read();   // Monitoring the inputs from Sensors
digitalWrite(LedPin, LOW);

if (reading1 == 1 && pos >= position_up && (millis() - Up_Time) > Stay_UP){
            //      - !!! Feeder Descends !!!
  Feeder.write(position_down,speed1,true);                           // tell servo to go to position in variable 'pos'
  pos = position_down;                  
  digitalWrite(LedPin, LOW);
  }

if (reading1 == 0 && pos <= position_down){
            //      - !!! Feeder Ascends !!!
  Feeder.write(position_up,speed2,true);                           // tell servo to go to position in variable 'pos'
  pos = position_up; 
  digitalWrite(LedPin, HIGH);                      
  Up_Time = millis();
  }

if ((millis() - cur_time) > Timing){                                                                              // LOGGING THE DATA
  cur_time = millis(); // Getting Timestamp from the beginning of the program
  Serial.print(cur_time);   // Timestamp
  Serial.print(" ");
  Serial.print(reading1);
  Serial.print(" ");
  Serial.println(pos);
  }
}
