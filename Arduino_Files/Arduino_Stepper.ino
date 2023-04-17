/*Example sketch to control a stepper motor with A4988 stepper motor driver, AccelStepper library and Arduino: continuous rotation. More info: https://www.makerguides.com */

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
void setup() {
  // initialize the pushbutton pin as an input:
  stepper1.setMaxSpeed(1500);
  stepper2.setMaxSpeed(1500);
  stepper3.setMaxSpeed(1500);
  stepper4.setMaxSpeed(1500);
  Serial.begin(9600);   
 
    Serial.println("Commands: trash, compost,recycle ");

}

String command;


void loop() {


if(Serial.available()){
        command = Serial.readStringUntil('\n');
         
        if(command.equals("trash")){
             while(stepper3.currentPosition() != 1500 && stepper4.currentPosition() != -1500 )
            {
              stepper3.setSpeed(1500);
              stepper3.runSpeed();
              stepper4.setSpeed(-1500);
              stepper4.runSpeed();
            }
          
            delay(1000);
          
            while(stepper3.currentPosition() != 0 && stepper4.currentPosition() != 0) 
            {
              stepper3.setSpeed(-1500);
              stepper3.runSpeed();
              stepper4.setSpeed(1500);
              stepper4.runSpeed();
            }
            Serial.println("taking out the trash");
        }
        else if(command.equals("compost")){
             while(stepper3.currentPosition() != -1500 && stepper4.currentPosition() != 1500 )
            {
              stepper3.setSpeed(-1500);
              stepper3.runSpeed();
              stepper4.setSpeed(1500);
              stepper4.runSpeed();
            }
          
            delay(1000);
          
            while(stepper3.currentPosition() != 0 && stepper4.currentPosition() != 0) 
            {
              stepper3.setSpeed(1500);
              stepper3.runSpeed();
              stepper4.setSpeed(-1500);
              stepper4.runSpeed();
            }
            Serial.println("composting"); 
        }
        else if(command.equals("recycle")){
            


            while(stepper2.currentPosition() != 1500 && stepper1.currentPosition() != -1500 )
            {
              stepper1.setSpeed(-1500);
              stepper1.runSpeed();
              stepper2.setSpeed(1500);
              stepper2.runSpeed();
            }
          
            delay(1000);
          
            // Reset the position to 0:
          
            while(stepper2.currentPosition() != 0 && stepper1.currentPosition() != 0) 
            {
              stepper1.setSpeed(1500);
              stepper1.runSpeed();
              stepper2.setSpeed(-1500);
              stepper2.runSpeed();
            }
            Serial.println("recycling");
        }
        else{
            Serial.println("Invalid command");
        }
    }


  }
