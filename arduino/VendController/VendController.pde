char tray[3]; // array to hold the incoming serial string bytes
// a1 is a01 etc 
int trayLetter;
int trayNumber;
int motorTime= 3000;
int loopFlag=0; 
int sensorPin=2; 
int sensorValue=0;
int maxMotorTime= 20000; //sets threshhold Motor Time
int motorStartTime=0;
void setup() { 
  pinMode(15, OUTPUT);  //a
  pinMode(14, OUTPUT);  //b
  pinMode(13, OUTPUT);  //c
  pinMode(12, OUTPUT);  //d
  pinMode(11, OUTPUT);  //e
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
  //read the serial port and create a string out of what you read
  int spos = -1;

  while (spos == -1){
    spos = ReadSerialString();
  }
  if(loopFlag==0){
    Spin();
  }
}


void Spin(){
  loopFlag=1; 
  if(tray[0] == 'a'){
    trayLetter= 15;
  }
  else if(tray[0] =='b'){
    trayLetter= 14;
  }
  else if(tray[0] == 'c'){
    trayLetter= 13;
  }
  else if(tray[0] =='d'){
    trayLetter= 12;
  }
  else if(tray[0] == 'e'){
    trayLetter= 11;
  }

  //does some math with characters to get to the correct pin
  trayNumber=11-((tray[1]-48)*10 + tray[2]-48);

  motorStartTime= millis(); 
  while(sensorValue < 700 && millis() - motorStartTime < maxMotorTime){
    digitalWrite(trayLetter, HIGH);   // set the Letter Swtich On   
    digitalWrite(trayNumber, HIGH);   // set the Num Switch on
    sensorValue = analogRead(sensorPin);
  }


  digitalWrite(trayLetter, LOW);    // set the Letter Switch off  
  digitalWrite(trayNumber, LOW);    // set the Num Switch off

}

//read a string from the serial and store it in an array
int ReadSerialString () { 
  int i=0;
  if(!Serial.available()) {
    return -1;
  }
  while (Serial.available() && i <3) {
    int c = Serial.read();
    Serial.println(c);
    tray[i++] = c;
    loopFlag=0;
  }
  //Serial.println(tray);
  return i;
}







