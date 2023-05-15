#include <LiquidCrystal_I2C.h>
#include <Wire.h>
LiquidCrystal_I2C lcd2(0x26,16,2);

int trigTrash = 3;
int echoTrash = 2;
long duration_trash;
int distance_trash;
int trash_bin; 

int trigRecycle = 5;
int echoRecycle = 4;
long duration_recycle;
int distance_recycle;
int recycle_bin;

int trigCompost = 9;
int echoCompost = 8;
long duration_compost;
int distance_compost;
int compost_bin;

void setup() {
  // put your setup code here, to run once:
  lcd2.begin();
  lcd2.backlight();
  pinMode ( trigTrash , OUTPUT);
  pinMode ( echoTrash, INPUT);

  pinMode ( trigRecycle, OUTPUT);
  pinMode ( echoRecycle, INPUT);

  pinMode ( trigCompost, OUTPUT);
  pinMode ( echoCompost, INPUT);

  Serial.begin(9600);
}

int trashBin() {
  digitalWrite(trigTrash, LOW);
  delayMicroseconds(2);

  digitalWrite(trigTrash, HIGH);
  delayMicroseconds(2);

  digitalWrite(trigTrash, LOW);

  duration_trash = pulseIn(echoTrash, HIGH);

  distance_trash = duration_trash * 0.034/2;

  //Serial.print("Distance trash: ");
  //Serial.println(distance_trash);

  return distance_trash;

}

int recycleBin() {
  digitalWrite(trigRecycle, LOW);
  delayMicroseconds(2);

  digitalWrite(trigRecycle, HIGH);
  delayMicroseconds(2);

  digitalWrite(trigRecycle, LOW);

  duration_recycle = pulseIn(echoRecycle, HIGH);

  distance_recycle = duration_recycle * 0.034/2;

  //Serial.print("Distance recycle: ");
  //Serial.println(distance_recycle);

  return distance_recycle;

}

int compostBin() {
  digitalWrite(trigCompost, LOW);
  delayMicroseconds(2);

  digitalWrite(trigCompost, HIGH);
  delayMicroseconds(2);

  digitalWrite(trigCompost, LOW);

  duration_compost = pulseIn(echoCompost, HIGH);

  distance_compost = duration_compost * 0.034/2;

  //Serial.print("Distance compost: ");
  //Serial.println(distance_compost);

  return distance_compost;

}
void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Check for trash volume");
  delay(500);
  trash_bin = trashBin();
  recycle_bin = recycleBin();
  compost_bin = compostBin();

  
  if ( trash_bin <= 20)
  {
    lcd2.clear();
    lcd2.setCursor(0,0);
    lcd2.print("Trash bin full");
    Serial.println("Trash bin full");
    delay(500);
  } 
  else {
    delay(100);
  }


  if ( recycle_bin <= 20)
  {
    Serial.println("Recycle bin full");
    delay(500);
  }
  else {
    delay(100);
  }

  if ( compost_bin <= 20) {
    lcd2.setCursor(0,1);
    lcd2.print("Compost bin full");
    Serial.println("Compost bin full");
    delay(500);
    }
  else {
    delay(100);
  }
  
  delay(100);
}
