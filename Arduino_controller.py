import serial

ser = serial.Serial("COM3", 9600) # replace with the correct port

# Define stepper motor connections and motor interface type. 
dirPin1 = 2
stepPin1 = 3
dirPin2 = 4
stepPin2 = 5
dirPin3 = 7
stepPin3 = 6
dirPin4 = 8
stepPin4 = 9

motor_interface_type = 1

# Create a new instance of the AccelStepper class:
stepper1 = AccelStepper(motor_interface_type, stepPin1, dirPin1)
stepper2 = AccelStepper(motor_interface_type, stepPin2, dirPin2)
stepper3 = AccelStepper(motor_interface_type, stepPin3, dirPin3)  
stepper4 = AccelStepper(motor_interface_type, stepPin4, dirPin4)  

# initialize the pushbutton pin as an input:
stepper1.setMaxSpeed(1500)
stepper2.setMaxSpeed(1500)
stepper3.setMaxSpeed(1500)
stepper4.setMaxSpeed(1500)

print("Commands: trash, compost,recycle")

while True:
    command = ser.readline().decode("utf-8").strip()

    if command == "trash":
        while stepper3.currentPosition() != 1500 and stepper4.currentPosition() != -1500:
            stepper3.setSpeed(1500)
            stepper3.runSpeed()
            stepper4.setSpeed(-1500)
            stepper4.runSpeed()

        delay(1000)

        while stepper3.currentPosition() != 0 and stepper4.currentPosition() != 0:
            stepper3.setSpeed(-1500)
            stepper3.runSpeed()
            stepper4.setSpeed(1500)
            stepper4.runSpeed()
        print("taking out the trash")

    elif command == "compost":
        while stepper3.currentPosition() != -1500 and stepper4.currentPosition() != 1500:
            stepper3.setSpeed(-1500)
            stepper3.runSpeed()
            stepper4.setSpeed(1500)
            stepper4.runSpeed()

        delay(1000)

        while stepper3.currentPosition() != 0 and stepper4.currentPosition() != 0:
            stepper3.setSpeed(1500)
            stepper3.runSpeed()
            stepper4.setSpeed(-1500)
            stepper4.runSpeed()
        print("composting")

    elif command == "recycle":
        while stepper2.currentPosition() != 1500 and stepper1.currentPosition() != -1500:
            stepper1.setSpeed(-1500)
            stepper1.runSpeed()
            stepper2.setSpeed(1500)
            stepper2.runSpeed()

        delay(1000)

        while stepper2.currentPosition() != 0 and stepper1.currentPosition() != 0:
            stepper1.setSpeed(1500)
            stepper1.runSpeed()
            stepper2.setSpeed(-1500)
            stepper2.runSpeed()
        print("recycling")
    else:
       
