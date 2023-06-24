#include <Servo.h>

Servo myservo;

void setup() {
  myservo.attach(9);
}

void ServoClose(){
  for (int pos = 270; pos >= 20; pos -= 10) { 
    myservo.write(pos);
    delay(10);
  }
}

void ServoOpen()
{
  for (int pos = 20; pos <= 270; pos += 10) {
    myservo.write(pos);
    delay(10);
  }
}

void loop() {
    ServoOpen();
    delay(10000);
    ServoClose();
    delay(10000);
     
}
