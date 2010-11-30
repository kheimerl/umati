char tray[3]; // array to hold the incoming serial string bytes
// a1 is a01 etc 
int trayLetter;
int trayNumber;
int motorTime= 3000;
int loopTime=0; 
void setup() { 
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
  //read the serial port and create a string out of what you read
  int spos = -1;
  while (spos == -1){
    spos = ReadSerialString();
  }
  if(loopTime==0){
    Spin();
  }
}


void Spin(){
  loopTime=1; 
  if(tray[0] == 'b'){
    trayLetter= 13;
  }
  else if(tray[0] =='c'){
    trayLetter= 12;
  }
  else if(tray[0] == 'd'){
    trayLetter= 11;
  }

  //does some math with characters to get to the correct pin
  trayNumber=11-((tray[1]-48)*10 + tray[2]-48);

  digitalWrite(trayLetter, HIGH);                           // set the Letter Swtich On   
  digitalWrite(trayNumber, HIGH);   // set the Num Switch on
  delay(motorTime);                                       // wait for a second
  digitalWrite(trayLetter, LOW);                        // set the Letter Switch off  
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
    loopTime=0;
  }
  //Serial.println(tray);
  return i;
}




