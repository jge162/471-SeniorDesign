#include <SoftwareSerial.h>

#include <LiquidCrystal_I2C.h>
#include <Wire.h>

LiquidCrystal_I2C lcd2(0x27,20,4);
//SoftwareSerial bluetoothDevice(2,3);
byte battery1[1][8] = {
  {0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F}, // 25% (1 block)
  
};

byte battery0[1][8] = {
  {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}, // 25% (1 block)
};
//TRASH INITIALIZE
int trigTrash = 3;
int echoTrash = 2;
long duration_trash;
int distance_trash;
int trash_bin; 
//RECYCLE INITIALIZE
int trigRecycle = 5;
int echoRecycle = 4;
long duration_recycle;
int distance_recycle;
int recycle_bin;
//COMPOST INITIALIZE
int trigCompost = 9;
int echoCompost = 8;
long duration_compost;
int distance_compost;
int compost_bin;

void setup() {
  // put your setup code here, to run once:
  lcd2.begin();
  lcd2.backlight();
  lcd2.createChar(1, battery1[0]);
  lcd2.createChar(0, battery0[0]);

  pinMode ( trigTrash , OUTPUT);
  pinMode ( echoTrash, INPUT);

  pinMode ( trigRecycle, OUTPUT);
  pinMode ( echoRecycle, INPUT);

  pinMode ( trigCompost, OUTPUT);
  pinMode ( echoCompost, INPUT);

  Serial.println("Check: trashbin,recyclebin,compostbin");
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
  return distance_compost;

}
String check;
void loop() {
  /*Serial.println("Hello World!");
  /*if (Serial.available()) {
    check = Serial.readStringUntil('\n');
    //Serial.println("Check for trash volume");
    delay(500);
    trash_bin = trashBin();
    recycle_bin = recycleBin();
    compost_bin = compostBin();
    //Serial.println(trash_bin);
    //Serial.println(recycle_bin);
    //Serial.println(compost_bin);
      if (check.equals("trashbin)")) {
        if ( 40 <= trash_bin && trash_bin < 50) {
          Serial.println("Trash 20%");
        }
        else if ( 30 <= trash_bin && trash_bin < 40)  {
          Serial.println("Trash 40%");
        }
        else if ( 20 <= trash_bin && trash_bin < 30) {
          Serial.println("Trash 60%");
        }
        else if ( 10 <= trash_bin && trash_bin < 20) {
          Serial.println("Trash 80%");
        }
        else if ( trash_bin < 10) {
          Serial.println("Trash FULL");
        }
        else  {
          Serial.println("Trash empty");
        }
      }
      else if (check.equals("recyclebin")){
        if ( 40 <= recycle_bin && recycle_bin < 50) {
          Serial.println("Recycle 20%");
        }
        else if ( 30 <= recycle_bin && recycle_bin < 40)  {
          Serial.println("Recycle 40%");
        }
        else if ( 20 <= recycle_bin && recycle_bin < 30) {
          Serial.println("Recycle 60%");
        }
        else if ( 10 <= recycle_bin && recycle_bin < 20) {
          Serial.println("Recycle 80%");
        }
        else if ( recycle_bin < 10) {
          Serial.println("Recycle FULL");
        }
        else  {
          Serial.println("Recycle empty");
        } 
      }
      else if (check.equals("compost")){
        if ( 40 <= compost_bin && compost_bin < 50) {
          Serial.println("Compost 20%");
        }
        else if ( 30 <= compost_bin && compost_bin < 40)  {
          Serial.println("Compost 40%");
        }
        else if ( 20 <= compost_bin &&  compost_bin < 30) {
          Serial.println("Compost 60%");
        }
        else if ( 10 <= compost_bin && compost_bin < 20) {
          Serial.println("Compost 80%");
        }
        else if ( compost_bin < 10) {
          Serial.println("Compost FULL");
        }
        else  {
          Serial.println("Compost empty");
        }
      }
      else {
        Serial.println("Invalid command");
      }
  } */

  /*if (bluetoothDevice.available()) {
    String message = bluetoothDevice.readStringUntil('\n');
    message.trim();

    if (message == "Check for bins volume") {
      trash_bin = trashBin();
      recycle_bin = recycleBin();
      compost_bin = compostBin();

      String trash00  = "Trash bin: EMPTY\n";
      String trash20  = "Trash bin: 20%\n";
      String trash40  = "Trash bin: 40%\n";
      String trash60  = "Trash bin: 60%\n";
      String trash80  = "Trash bin: 80%\n";
      String trash100 = "Trash bin: FULL\n";

      String recycle00 = "Recycle bin: EMPTY\n";
      String recycle20 = "Recycle bin: 20%\n";
      String recycle40 = "Recycle bin: 40%\n";
      String recycle60 = "Recycle bin: 60%\n";
      String recycle80 = "Recycle bin: 80%\n";
      String recycle100 = "Recycle bin: FULL\n";

      String compost00 = "Compost bin: EMPTY\n";
      String compost20 = "Compost bin: 20%\n";
      String compost40 = "Compost bin: 40%\n";
      String compost60 = "Compost bin: 60%\n";
      String compost80 = "Compost bin: 80%\n";
      String compost100 = "Compost bin: FULL\n";

      //TRASH
      if ( 40 <= trash_bin && trash_bin < 50) { 
        bluetoothDevice.print(trash20);
      }

      else if ( 30 <= trash_bin && trash_bin < 40) {
        bluetoothDevice.print(trash40);
      }
      else if ( 20 <= trash_bin && trash_bin < 30) {
        bluetoothDevice.print(trash60);
      }
      else if ( 10 <= recycle_bin && recycle_bin < 20) {
        bluetoothDevice.print(trash80);
      }
      else if ( trash_bin < 10) {
        bluetoothDevice.print(trash100);
      }
      else { bluetoothDevice.print(trash00); 
      }
      delay(100);
      }

      //RECYCLE
      if ( 40 <= recycle_bin && recycle_bin < 50) { 
        bluetoothDevice.print(recycle20);
      }

      else if ( 30 <= recycle_bin && recycle_bin < 40) {
        bluetoothDevice.print(recycle40);
      }
      else if ( 20 <= recycle_bin && recycle_bin < 30) {
        bluetoothDevice.print(recycle60);
      }
      else if ( 10 <= recycle_bin && recycle_bin < 20) {
        bluetoothDevice.print(recycle80);
      }
      else if ( recycle_bin < 10) {
        bluetoothDevice.print(recycle100);
      }
      else { bluetoothDevice.print(recycle00); 
      }
      delay(100);
      }

      //COMPOST
      if ( 40 <= compost_bin && compost_bin < 50) { 
        bluetoothDevice.print(recycle20);
      }

      else if ( 30 <= compost_bin && compost_bin < 40) {
        bluetoothDevice.print(compost40);
      }
      else if ( 20 <= compost_bin && compost_bin < 30) {
        bluetoothDevice.print(compost60);
      }
      else if ( 10 <= compost_bin && compost_bin < 20) {
        bluetoothDevice.print(compost80);
      }
      else if ( compost_bin < 10) {
        bluetoothDevice.print(compost100);
      }
      else { bluetoothDevice.print(compost00); 
      }
      delay(100);
      }
  } */
  // put your main code here, to run repeatedly:
  Serial.println("Check for trash volume");
  delay(500);
  trash_bin = trashBin();
  recycle_bin = recycleBin();
  compost_bin = compostBin();
  Serial.println(trash_bin);
  Serial.println(recycle_bin);
  Serial.println(compost_bin);
  lcd2.setCursor(0,0);
  lcd2.print("Trash   bin:");
  lcd2.setCursor(0,1);
  lcd2.print("Recycle bin:");
  lcd2.setCursor(0,2);
  lcd2.print("Compost bin:");

  if ( 40 <= trash_bin && trash_bin < 50)
  {
    lcd2.setCursor(13,0);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(14,0);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(15,0);
    lcd2.write(byte(0)); //
    lcd2.setCursor(16,0);
    lcd2.print("20%");
    lcd2.setCursor(19,0);
    lcd2.write(byte(1)); //

    Serial.println("Trash bin 20%");
    //delay(1000);
  } 
  
 
  else if ( 30 <= trash_bin && trash_bin < 40)
  {
    lcd2.setCursor(13,0);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(14,0);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(15,0);
    lcd2.print("40%");
    lcd2.setCursor(18,0);
    lcd2.write(byte(1)); //
    lcd2.setCursor(19,0);
    lcd2.write(byte(1)); 
    Serial.println("Trash bin 40%");
    //delay(1000);
  } 
  

  else if ( 20 <= trash_bin && trash_bin < 30)
  {
    lcd2.setCursor(13,0);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(14,0);
    lcd2.print("60%");
    lcd2.setCursor(17,0);
    lcd2.write(byte(1)); // 75% (3 blocks))
    lcd2.setCursor(18,0);
    lcd2.write(byte(1)); //
    lcd2.setCursor(19,0);
    lcd2.write(byte(1)); 
    Serial.println("Trash bin 60%");
    //delay(1000);
  } 
  else if ( 10 <= trash_bin && trash_bin < 20)
  {
    lcd2.setCursor(13,0);
    lcd2.print("80%");
    lcd2.setCursor(16,0);
    lcd2.write(byte(1)); // 75% (3 blocks))
    lcd2.setCursor(17,0);
    lcd2.write(byte(1)); // 75% (3 blocks))
    lcd2.setCursor(18,0);
    lcd2.write(byte(1)); //
    lcd2.setCursor(19,0);
    lcd2.write(byte(1));
    Serial.println("Trash bin 80%");
    //delay(1000);
  } 

  else if ( trash_bin < 10)
  {
    lcd2.setCursor(13,0);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(14,0);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(15,0);
    lcd2.print("FULL");
    lcd2.setCursor(19,0);
    lcd2.write(byte(0)); 
    Serial.println("Trash bin full");
    //delay(1000);
  }  
  else {
    lcd2.setCursor(13,0);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(14,0);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(15,0);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(16,0);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(17,0);
    lcd2.write(byte(0)); // 75% (3 blocks))
    lcd2.setCursor(18,0);
    lcd2.write(byte(0)); //
    lcd2.setCursor(19,0);
    lcd2.write(byte(0)); 
    //delay(500);
  }

  //RECYCLE

  if ( 40 <= recycle_bin && recycle_bin < 50)
  {
    lcd2.setCursor(13,1);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(14,1);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(15,1);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(16,1);
    lcd2.print("20%");
    lcd2.setCursor(19,1);
    lcd2.write(byte(1)); // 
    Serial.println("Recycle bin 20%");
    //delay(1000);
  } 
  
 
  else if ( 30 <= recycle_bin && recycle_bin < 40)
  {
    lcd2.setCursor(13,1);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(14,1);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(15,1);
    lcd2.print("40%");
    lcd2.setCursor(18,1);
    lcd2.write(byte(1)); //
    lcd2.setCursor(19,1);
    lcd2.write(byte(1)); 
    Serial.println("Recycle bin 40%");
    //delay(1000);
  } 
  

  else if ( 20 <= recycle_bin && recycle_bin < 30)
  {
    lcd2.setCursor(13,1);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(14,1);
    lcd2.print("60%");
    lcd2.setCursor(17,1);
    lcd2.write(byte(1)); // 75% (3 blocks))
    lcd2.setCursor(18,1);
    lcd2.write(byte(1)); //
    lcd2.setCursor(19,1);
    lcd2.write(byte(1)); 
    Serial.println("Recycle bin 60%");
    //delay(1000);
  } 
  else if ( 10 <= recycle_bin && recycle_bin < 20)
  {
    lcd2.setCursor(13,1);
    lcd2.print("80%");
    lcd2.setCursor(16,1);
    lcd2.write(byte(1)); // 75% (3 blocks))
    lcd2.setCursor(17,1);
    lcd2.write(byte(1)); // 75% (3 blocks))
    lcd2.setCursor(18,1);
    lcd2.write(byte(1)); //
    lcd2.setCursor(19,1);
    lcd2.write(byte(1));
    Serial.println("Recycle bin 80%");
    //delay(1000);
  } 

  else if ( recycle_bin < 10)
  {
    lcd2.setCursor(13,1);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(14,1);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(15,1);
    lcd2.print("FULL");
    lcd2.setCursor(19,1);
    lcd2.write(byte(0)); 
    Serial.println("Recycle bin full");
    //delay(1000);
  }  
  else {
    lcd2.setCursor(13,1);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(14,1);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(15,1);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(16,1);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(17,1);
    lcd2.write(byte(0)); // 75% (3 blocks))
    lcd2.setCursor(18,1);
    lcd2.write(byte(0)); //
    lcd2.setCursor(19,1);
    lcd2.write(byte(0)); 
    //delay(500);
  }


  //COMPOST

  if ( 40 <= compost_bin && compost_bin < 50)
  {
    lcd2.setCursor(13,2);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(14,2);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(15,2);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(16,2);
    lcd2.print("20%");
    lcd2.setCursor(19,2);
    lcd2.write(byte(1)); // 
    Serial.println("Compost bin 20%");
    //delay(1000);
  } 
  
 
  else if ( 30 <= compost_bin && compost_bin < 40)
  {
    lcd2.setCursor(13,2);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(14,2);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(15,2);
    lcd2.print("40%");
    lcd2.setCursor(18,2);
    lcd2.write(byte(1)); //
    lcd2.setCursor(19,2);
    lcd2.write(byte(1)); 
    Serial.println("Compost bin 40%");
    //delay(1000);
  } 
  

  else if ( 20 <= compost_bin && compost_bin < 30)
  {
    lcd2.setCursor(13,2);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(14,2);
    lcd2.print("60%");
    lcd2.setCursor(17,2);
    lcd2.write(byte(1)); // 75% (3 blocks))
    lcd2.setCursor(18,2);
    lcd2.write(byte(1)); //
    lcd2.setCursor(19,2);
    lcd2.write(byte(1)); 
    Serial.println("Compost bin 60%");
    //delay(1000);
  } 
  else if ( 10 <= compost_bin && compost_bin < 20)
  {
    lcd2.setCursor(13,2);
    lcd2.print("80%");
    lcd2.setCursor(16,2);
    lcd2.write(byte(1)); // 75% (3 blocks))
    lcd2.setCursor(17,2);
    lcd2.write(byte(1)); // 75% (3 blocks))
    lcd2.setCursor(18,2);
    lcd2.write(byte(1)); //
    lcd2.setCursor(19,2);
    lcd2.write(byte(1));
    Serial.println("Compost bin 80%");
    //delay(1000);
  } 

  else if ( compost_bin < 10)
  {
    lcd2.setCursor(13,2);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(14,2);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(15,2);
    lcd2.print("FULL");
    lcd2.setCursor(19,2);
    lcd2.write(byte(0)); 
    Serial.println("Compost bin full");
    //delay(1000);
  }  
  else {
    lcd2.setCursor(13,2);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(14,2);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(15,2);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(16,2);
    lcd2.write(byte(0)); // 
    lcd2.setCursor(17,2);
    lcd2.write(byte(0)); // 75% (3 blocks))
    lcd2.setCursor(18,2);
    lcd2.write(byte(0)); //
    lcd2.setCursor(19,2);
    lcd2.write(byte(0)); 
    //delay(500);
  }


}
