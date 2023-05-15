#include "LiquidCrystal_I2C.h"
#include "Wire.h"
// Include the AccelStepper library:
#include <AccelStepper.h>

// Define stepper motor connections and motor interface type. Motor interface type must be set to 1 when using a driver:
#define dirPin1 2
#define stepPin1 3
#define dirPin2 4
#define stepPin2 5
#define dirPin3 7
#define stepPin3 6
#define dirPin4 8
#define stepPin4 9

#define motorInterfaceType 1

// Create a new instance of the AccelStepper class:
AccelStepper stepper1 = AccelStepper(motorInterfaceType, stepPin1, dirPin1);
AccelStepper stepper2 = AccelStepper(motorInterfaceType, stepPin2, dirPin2);
AccelStepper stepper3 = AccelStepper(motorInterfaceType, stepPin3, dirPin3);  
AccelStepper stepper4 = AccelStepper(motorInterfaceType, stepPin4, dirPin4);  
// variables will change:
int buttonState = 0;  // variable for reading the pushbutton status
int buttonState1 = 0;

// SET LCD
LiquidCrystal_I2C lcd(0x27, 16, 2);


void setup() {
  // put your setup code here, to run once:
  stepper1.setMaxSpeed(1500);
  stepper2.setMaxSpeed(1500);
  stepper3.setMaxSpeed(1500);
  stepper4.setMaxSpeed(1500);
  pinMode(12, OUTPUT);
  lcd.begin();
  lcd.backlight();
  Serial.begin(9600);
  Serial.println("Commands: welcome, detected, nondected, trash, compost, recycle, thankyou");
}

String command;
void loop() {
  // put your main code here, to run repeatedly:
if (Serial.available()) {
  command = Serial.readStringUntil('\n');
   
        if(command.equals("trash")){
            digitalWrite(12, HIGH);
            lcd.clear();
            lcd.print("Trash detected");
            //delay(500);
            //lcd.clear();
            //lcd.print("----Sorting----");

            
             while(stepper3.currentPosition() != 1400 && stepper4.currentPosition() != -1400 )
            {
              stepper3.setSpeed(1500);
              stepper3.runSpeed();
              stepper4.setSpeed(-1500);
              stepper4.runSpeed();
            }
          
            delay(500);
          
            while(stepper3.currentPosition() != 0 && stepper4.currentPosition() != 0) 
            {
              stepper3.setSpeed(-1500);
              stepper3.runSpeed();
              stepper4.setSpeed(1500);
              stepper4.runSpeed();
            }
            Serial.println("taking out the trash");
            lcd.clear();
            lcd.print("Sorting completed");
            delay(1500);
            lcd.clear();
            digitalWrite(12, LOW);
        }
        else if(command.equals("compost")){
            digitalWrite(12, HIGH);
            lcd.clear();
            lcd.print("Compost detected");
            //delay(500);
            //lcd.clear();
            //lcd.print("----Sorting----");
            
             while(stepper3.currentPosition() != -1400 && stepper4.currentPosition() != 1400 )
            {
              stepper3.setSpeed(-1500);
              stepper3.runSpeed();
              stepper4.setSpeed(1500);
              stepper4.runSpeed();
            }
          
            delay(500);
          
            while(stepper3.currentPosition() != 0 && stepper4.currentPosition() != 0) 
            {
              stepper3.setSpeed(1500);
              stepper3.runSpeed();
              stepper4.setSpeed(-1500);
              stepper4.runSpeed();
            }
            Serial.println("composting");
            lcd.clear();
            lcd.print("Sorting completed");
            delay(1500);
            lcd.clear();
            digitalWrite(12, LOW);
        }
        else if(command.equals("recycle")){
            digitalWrite(12, HIGH);
            lcd.clear();
            lcd.print("Recycle detected");
            //delay(500);
            //lcd.clear();
            //lcd.print("----Sorting----");

            while(stepper2.currentPosition() != 1400 && stepper1.currentPosition() != -1400 )
            {
              stepper1.setSpeed(-1500);
              stepper1.runSpeed();
              stepper2.setSpeed(1500);
              stepper2.runSpeed();
            }
          
            delay(500);
          
            // Reset the position to 0:
          
            while(stepper2.currentPosition() != 0 && stepper1.currentPosition() != 0) 
            {
              stepper1.setSpeed(1500);
              stepper1.runSpeed();
              stepper2.setSpeed(-1500);
              stepper2.runSpeed();
            }
            Serial.println("recycling");
            lcd.clear();
            lcd.print("Sorting completed");
            delay(1500);
            lcd.clear();
            digitalWrite(12, LOW);
        }

        else if(command.equals("welcome")){
          lcd.setCursor(3,0);
          lcd.print("Automatic");
          lcd.setCursor(1,1);
          lcd.print("Wastes Sorter");
          
          
        }
        else if(command.equals("detected")) {
          lcd.setCursor(1,0);
          lcd.print("Hello there!");
          delay(500);
          lcd.clear();
          lcd.setCursor(2,0);
          lcd.print("Please throw");
          lcd.setCursor(1,1);
          lcd.print("your wastes in"); 
          
          delay(500);
          lcd.clear();
        }
        else if (command.equals("nondetected")){
          lcd.setCursor(3,0);
          lcd.print("Automatic");
          lcd.setCursor(1,1);
          lcd.print("Wastes Sorter");
          delay(500);
          lcd.clear();
        }
        else if (command.equals("thankyou")){
          lcd.setCursor(3,0);
          lcd.print("Thankyou!");
          delay(500);
          lcd.clear();
        }
        else if (command.equals("activate")){
          digitalWrite(12, HIGH);
        }
        else if (command.equals("deactivate")){
          digitalWrite(12, LOW);
        }
        else{
            Serial.println("Invalid command");
          lcd.setCursor(3,0);
          lcd.print("Automatic");
          lcd.setCursor(1,1);
          lcd.print("Wastes Sorter");
          delay(500);
          lcd.clear();
            
        }
    }


  }

