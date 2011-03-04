char tray[3]; // array to hold the incoming serial string bytes
// a1 is a01 etc 
int trayLetter;
int trayNumber;

int loopFlag=0; 
const int sensorPin = A1;
const int knockPin = A0;
const long maxMotorTime= 110000; //sets threshhold Motor Time
const int laserDifference = 10;
const int knockThresh = 100;
const int biasDegree = 25;
void setup() { 
  //pinMode(15, OUTPUT);  //light sensor
  //pinMode(14, OUTPUT);  //vibration sensor in -k
  pinMode(13, OUTPUT);  //a
  pinMode(12, OUTPUT);  //b
  pinMode(11, OUTPUT);  //c
  pinMode(10, OUTPUT);  //d
  pinMode(9, OUTPUT);   //e
  pinMode(8, OUTPUT);   //f 
  pinMode(7, OUTPUT);   //1
  pinMode(6, OUTPUT);   //2
  pinMode(5, OUTPUT);   //3
  pinMode(4, OUTPUT);   //4
  pinMode(3, OUTPUT);   //5
  pinMode(2, OUTPUT);   //6
  pinMode(1, OUTPUT);   //7
  pinMode(16, OUTPUT);   //8
  pinMode(17, OUTPUT);   //9
  pinMode(18, OUTPUT);   //10
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
  Serial.println("Spin");
  if(tray[0] == 'a'){
    trayLetter= 13;
  }
  else if(tray[0] =='b'){
    trayLetter= 12;
  }
  else if(tray[0] == 'c'){
    trayLetter= 11;
  }
  else if(tray[0] =='d'){
    trayLetter= 10;
  }
  else if(tray[0] == 'e'){
    trayLetter= 9;
  }
  else if(tray[0] == 'f'){
    trayLetter= 8;
  }

  //does some math with characters to get to the correct pin
  //must be fixed!
  trayNumber=11-((tray[1]-48)*10 + tray[2]-48);
  
  //hard coded to two until we fix the board
  digitalWrite(trayLetter, HIGH);   // set the Letter Swtich On   
  digitalWrite(2, HIGH);   // set the Num Switch on
  
  long i=0;
  
  //first the laser sensor
  float sensorValueMax = analogRead(sensorPin);
  long sensorValue = sensorValueMax;

  //then the knock sensor
  float knockSensorVal = analogRead(knockPin);

  while((sensorValue > sensorValueMax-laserDifference)  && 
        (knockSensorVal < knockThresh) &&
        i < maxMotorTime ){  
    i++;
    //running biased average
    sensorValueMax = ((sensorValueMax * biasDegree) + sensorValue)/(biasDegree+1);
    Serial.print(sensorValue);
    Serial.print(' ');
    Serial.print(sensorValueMax);
    Serial.print(' ');
    Serial.println(knockSensorVal);
    knockSensorVal = analogRead(knockPin);
    sensorValue = analogRead(sensorPin);
  }
  Serial.println(sensorValueMax);
  Serial.println(sensorValue);
  Serial.println(knockSensorVal);

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
    //delay(100);
    Serial.println(char(c));
    tray[i++] = c;
    loopFlag=0;
  }
  //Serial.println(tray);
  return i;
}
