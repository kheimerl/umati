/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.
 
  This example code is in the public domain.
 */

char tray[3]; 
int trayNum=9;
int trayLetter=11;

void setup() {                
  // initialize the digital pin as an output.
  // Pin 13 has an LED connected on most Arduino boards:
  pinMode(13, OUTPUT);  //a
  pinMode(12, OUTPUT);  //b
  pinMode(11, OUTPUT);  //c
  pinMode(10, OUTPUT);  //1
  pinMode(9, OUTPUT);   //2
  pinMode(8, OUTPUT);   //3 
  pinMode(7, OUTPUT);   //4
  pinMode(6, OUTPUT);   //5
  pinMode(5, OUTPUT);   //6
  pinMode(4, OUTPUT);   //7
  pinMode(3, OUTPUT);   //8
  pinMode(2, OUTPUT);   //9
  pinMode(1, OUTPUT);   //10
  Serial.begin(9600); //probably connect to python using this 
}

void loop() {
  
  int spos = readSerialString();
  
  //Interpret that string and write to
    
  digitalWrite(trayNum, HIGH);
  digitalWrite(trayLetter, HIGH);   // set the LED on
   // digitalWrite(12, HIGH);   // set the LED on
     // digitalWrite(11, HIGH);   // set the LED on
  delay(12000);              // wait for a second
  digitalWrite(trayLetter, LOW);   // set the LED off
    //digitalWrite(12, LOW);   // set the LED on
  digitalWrite(trayNum, LOW);
  delay(1000);              // wait for a second
}

//read a string from the serial and store it in an array
int readSerialString () { 
  int i=0;
  if(!Serial.available()) {
    return -1;
  }
  while (Serial.available() && i <3) {
    int c = Serial.read();
    tray[i++] = c;
  }
  Serial.println(tray);
  return i;
}
