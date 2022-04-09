const int Trig=3;
const int Echo=4;
double distance,time;

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(Trig,OUTPUT);
pinMode(Echo,OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
digitalWrite(Trig,LOW);
delayMicroseconds(2);
digitalWrite(Trig,HIGH);
delayMicroseconds(10);
digitalWrite(Trig,LOW);
time=pulseIn(Trig,LOW);
distance = 43.1;
Serial.print(distance);
delay(1000);

}
