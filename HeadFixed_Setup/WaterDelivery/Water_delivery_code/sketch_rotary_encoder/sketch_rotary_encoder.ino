volatile long temp = 0;
volatile long counter = 0; //This variable will increase or decrease depending on the rotation of encoder
unsigned long time = 0;
int counter_new = 0;
int counter_old = 0;
const int reading_delay = 10; // Timing of the program in ms
    
void setup() {
  Serial.begin (115200);
  pinMode(2, INPUT_PULLUP); // internal pullup input pin 2  
  pinMode(3, INPUT_PULLUP); // internal pullup input pin 3
  pinMode(13, OUTPUT); // defining the sync pin
   //Setting up interrupt
  //A rising pulse from encodenren activated ai0(). AttachInterrupt 0 is DigitalPin nr 2 on moust Arduino.
  attachInterrupt(0, ai0, RISING);
   
  //B rising pulse from encodenren activated ai1(). AttachInterrupt 1 is DigitalPin nr 3 on moust Arduino.
  attachInterrupt(1, ai1, RISING);
  }
   
  void loop() {
    digitalWrite(13, LOW);
    if ((millis() - time) > reading_delay){                                                                              // LOGGING THE DATA
      time = millis(); // Getting Timestamp from the beginning of the program
      digitalWrite(13, LOW); // Ticking on the sync pin
      counter_old = counter_new; // Measurement from the rotary encoder
      counter_new = counter;

      // Printing out the information
      Serial.print(time);   // Timestamp
      Serial.print(" ");   
      Serial.print((counter_new-counter_old)*100);     // Rotations per second calculated as difference in position per 10ms X 100 (extrapolate for the whole second)
      Serial.print(" ");   
      Serial.println(counter_new);     // Current position of the counter
    }
  }
   
  void ai0() {
  // ai0 is activated if DigitalPin nr 2 is going from LOW to HIGH
  // Check pin 3 to determine the direction
  if(digitalRead(3)==LOW) {
  counter--;
  }
  else{
  counter++;

  }
  }
  
  void ai1() {
  // ai0 is activated if DigitalPin nr 3 is going from LOW to HIGH
  // Check with pin 2 to determine the direction
  if(digitalRead(2)==LOW) {
  counter--;
  }
  else{
  counter++;
  }
  }