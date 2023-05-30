#include <nRF24L01.h>
#include <RF24.h>
#include <RF24_config.h>
#include <Servo.h>

RF24 radio(7, 8);
byte endereco[6] = "1node";
boolean abrirPorta;
Servo myservo;
void setup() {
  myservo.attach(9);
  radio.openReadingPipe(1, endereco);
  radio.startListening();
}

void ServoClose()
{
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
  
  if (radio.available()){
    radio.read(&abrirPorta, sizeof(boolean));
    if (abrirPorta) {
      ServoOpen();
      delay(10000);
      ServoClose();
    }
  }
}
