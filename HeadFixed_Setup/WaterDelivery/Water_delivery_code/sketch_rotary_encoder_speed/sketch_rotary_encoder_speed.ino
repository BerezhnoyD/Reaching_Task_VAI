#include <Encoder.h>
Encoder myEncoder(2, 3);

const unsigned long timePeriod = 10;
unsigned long startTime;
long startPosition;
    
void setup() {
  Serial.begin (115200);
  pinMode(2, INPUT_PULLUP); // internal pullup input pin 2  
  pinMode(3, INPUT_PULLUP); // internal pullup input pin 3
  startPosition = myEncoder.read();
  startTime = millis();
  }
   
  long oldPosition = -999;

  void loop() {
  unsigned long now = millis();
  long newPosition = myEncoder.read();

  if ( now - startTime >= timePeriod ) {
    // time to calculate average encoder speed
    float speed = (newPosition - startPosition) / (float)timePeriod;
    Serial.print( "Avg speed is ");
    Serial.println( speed, 4 );
    startTime = now;
    startPosition = newPosition;
  }
  if (newPosition  != oldPosition) {
    oldPosition = newPosition;
    Serial.println(newPosition);
   
  }
  }