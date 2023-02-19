import os
import pathlib
import time
import cv2
from pycoral.utils import edgetpu
from pycoral.utils import dataset
from pycoral.adapters import common
from pycoral.adapters import classify
from periphery import GPIO, Serial


class Stepper:
    def __init__(self, pin1, pin2, pin3, pin4):
        # Initialize the stepper motor with the given pins.
        self.direction = None
        self.current_speed = None
        self.pin1 = pin1
        self.pin2 = pin2
        self.pin3 = pin3
        self.pin4 = pin4
        self.current_position = 0
        self.max_speed = 1500

    def setMaxSpeed(self, speed):
        # Set the maximum speed of the stepper motor.
        self.max_speed = speed

    def setCurrentPosition(self, position):
        # Set the current position of the stepper motor.
        self.current_position = position

    def currentPosition(self):
        # Get the current position of the stepper motor.
        return self.current_position

    def setSpeed(self, speed):
        # Set the current speed of the stepper motor, taking the direction of movement into account.
        self.current_speed = min(self.max_speed, abs(speed))
        self.direction = 1 if speed > 0 else -1

    def runSpeed(self):
        # Move the stepper motor at the current speed and direction, updating the current position.
        self.current_position += self.direction
        self.current_position %= 200

        # Define the coil states for each position in the stepper motor sequence.
        coils = [
            (1, 0, 0, 1),
            (1, 0, 0, 0),
            (1, 1, 0, 0),
            (0, 1, 0, 0),
            (0, 1, 1, 0),
            (0, 0, 1, 0),
            (0, 0, 1, 1),
            (0, 0, 0, 1),
        ]

        # Set the coil state for the current position in the stepper motor sequence.
        coil = coils[self.current_position % 8]
        self.pin1.write(coil[0])
        self.pin2.write(coil[1])
        self.pin3.write(coil[2])
        self.pin4.write(coil[3])


""" 
def setup():
    # Declare stepper1, stepper2, stepper3, and stepper4 as global variables, so they can be used outside the setup()
    # function.
    global stepper1, stepper2, stepper3, stepper4, class_label, confidence

    # Initialize the pushbutton pins as output pins:
    recycling_gpio = GPIO("/dev/gpiochip4", 14, "out")
    waste_gpio = GPIO("/dev/gpiochip4", 15, "out")
    compost_gpio = GPIO("/dev/gpiochip4", 7, "out")

    # Define the pins for each stepper motor.
    stepper1_pins = (
        GPIO("/dev/gpiochip4", 4, "out"), GPIO("/dev/gpiochip4", 17, "out"), GPIO("/dev/gpiochip4", 27, "out"),
        GPIO("/dev/gpiochip4", 22, "out"))

    # For stepper 2:
    stepper2_pins = (
        GPIO("/dev/gpiochip4", 5, "out"), GPIO("/dev/gpiochip4", 6, "out"), GPIO("/dev/gpiochip4", 13, "out"),
        GPIO("/dev/gpiochip4", 19, "out"))

    # For stepper 3:
    stepper3_pins = (
        GPIO("/dev/gpiochip4", 18, "out"), GPIO("/dev/gpiochip4", 23, "out"), GPIO("/dev/gpiochip4", 24, "out"),
        GPIO("/dev/gpiochip4", 25, "out"))

    # For stepper 4:
    stepper4_pins = (
        GPIO("/dev/gpiochip4", 12, "out"), GPIO("/dev/gpiochip4", 16, "out"), GPIO("/dev/gpiochip4", 20, "out"),
        GPIO("/dev/gpiochip4", 21, "out"))

    # Create a Stepper object for each stepper motor, using the corresponding pins.
    stepper1 = Stepper(*stepper1_pins)
    stepper2 = Stepper(*stepper2_pins)
    stepper3 = Stepper(*stepper3_pins)
    stepper4 = Stepper(*stepper4_pins)

    # Set the maximum speed for each stepper motor.
    stepper1.setMaxSpeed(1500)
    stepper2.setMaxSpeed(1500)
    stepper3.setMaxSpeed(1500)
    stepper4.setMaxSpeed(1500)

    # Return the GPIO objects for recycling, waste, and compost bins, and the stepper motors
    return recycling_gpio, waste_gpio, compost_gpio, stepper1, stepper2, stepper3, stepper4


# get list using this on Coral ls /dev/tt* and /dev/i2c-1
# this is to use usb port -> /dev/ttyUSB0
uncomment this once arduino is connected
# ser = Serial("/dev/i2c-1", 9600)
"""
# Specify the TensorFlow model, labels, and camera device
script_dir = pathlib.Path(__file__).parent.absolute()
model_file = os.path.join(script_dir, '2-17model.tflite')
label_file = os.path.join(script_dir, '2-17labels.txt')
device = 1
width = 640
height = 480

# Initialize the TF interpreter
interpreter = edgetpu.make_interpreter(model_file)
interpreter.allocate_tensors()

# Open the camera device
cap = cv2.VideoCapture(device)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


def main():
    # Call the setup function to initialize the GPIO pins and stepper motors.
    """setup() uncomment when ready to connect Arduino"""
    # Loop over frames from the camera
    while True:
        # Capture the current frame from the camera
        ret, frame = cap.read()

        # Convert the frame to RGB format and resize it
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        size = common.input_size(interpreter)
        rgb = cv2.resize(rgb, size)

        # Pass the resized frame to the interpreter
        common.set_input(interpreter, rgb)

        # Run an inference
        interpreter.invoke()
        classes = classify.get_classes(interpreter, top_k=1)

        # Print the result and check the class label and confidence score
        labels = dataset.read_label_file(label_file)
        for c in classes:
            class_label = labels.get(c.id, c.id)
            confidence = c.score
            if class_label == 'Recycling' and confidence > 0.7:
                """ 
                recycling_gpio.write(True)
                waste_gpio.write(False)
                compost_gpio.write(False)

                while stepper2.currentPosition() != 1500 and stepper1.currentPosition() != -1500:
                    stepper1.setSpeed(-1500)
                    stepper1.runSpeed()
                    stepper2.setSpeed(1500)
                    stepper2.runSpeed()
                time.sleep(1)
                while stepper2.currentPosition() != 0 and stepper1.currentPosition() != 0:
                    stepper1.setSpeed(1500)
                    stepper1.runSpeed()
                    stepper2.setSpeed(-1500)
                    stepper2.runSpeed()

                ser.write(b'trash\n')
                """
            elif class_label == 'Waste' and confidence > 0.5:
                """
                recycling_gpio.write(False)
                waste_gpio.write(True)
                compost_gpio.write(False)
                while stepper3.currentPosition() != 0 and stepper4.currentPosition() != 0:
                    stepper3.setSpeed(-1500)
                    stepper3.runSpeed()
                    stepper4.setSpeed(1500)
                    stepper4.runSpeed()

                ser.write(b'recycle\n')

            elif class_label == 'Compost' and confidence > 0.5:
                recycling_gpio.write(False)
                waste_gpio.write(False)
                compost_gpio.write(True)
                while stepper3.currentPosition() != 1500 and stepper4.currentPosition() != -1500:
                    stepper3.setSpeed(1500)
                    stepper3.runSpeed()
                    stepper4.setSpeed(-1500)
                    stepper4.runSpeed()
                time.sleep(1)
                while stepper3.currentPosition() != 0 and stepper4.currentPosition() != 0:
                    stepper3.setSpeed(-1500)
                    stepper3.runSpeed()
                    stepper4.setSpeed(1500)
                    stepper4.runSpeed()

                ser.write(b'compost\n')
                """
        print('%s detected: = %.5f' % (class_label, confidence))

        # Display the frame with the confidence value
        cv2.putText(frame, "Confidence: %.2f" % confidence, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow('Object Detection', frame)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()
    """
    # Close the GPIO pins
    recycling_gpio.close()
    waste_gpio.close()
    compost_gpio.close()

"""


if __name__ == '__main__':
    """recycling_gpio, waste_gpio, compost_gpio, stepper1, stepper2, stepper3, stepper4 = setup()"""
    main()

"""
    # Define the pins for each stepper motor.
    # For stepper 1:
    #   GPIO pin 4 is connected to the first coil of the stepper motor.
    #   GPIO pin 17 is connected to the second coil of the stepper motor.
    #   GPIO pin 27 is connected to the third coil of the stepper motor.
    #   GPIO pin 22 is connected to the fourth coil of the stepper motor.
    stepper1_pins = (
        GPIO("/dev/gpiochip4", 4, "out"), GPIO("/dev/gpiochip4", 17, "out"), GPIO("/dev/gpiochip4", 27, "out"),
        GPIO("/dev/gpiochip4", 22, "out"))

    # For stepper 2:
    #   GPIO pin 5 is connected to the first coil of the stepper motor.
    #   GPIO pin 6 is connected to the second coil of the stepper motor.
    #   GPIO pin 13 is connected to the third coil of the stepper motor.
    #   GPIO pin 19 is connected to the fourth coil of the stepper motor.
    stepper2_pins = (
        GPIO("/dev/gpiochip4", 5, "out"), GPIO("/dev/gpiochip4", 6, "out"), GPIO("/dev/gpiochip4", 13, "out"),
        GPIO("/dev/gpiochip4", 19, "out"))

    # For stepper 3:
    #   GPIO pin 18 is connected to the first coil of the stepper motor.
    #   GPIO pin 23 is connected to the second coil of the stepper motor.
    #   GPIO pin 24 is connected to the third coil of the stepper motor.
    #   GPIO pin 25 is connected to the fourth coil of the stepper motor.
    stepper3_pins = (
        GPIO("/dev/gpiochip4", 18, "out"), GPIO("/dev/gpiochip4", 23, "out"), GPIO("/dev/gpiochip4", 24, "out"),
        GPIO("/dev/gpiochip4", 25, "out"))

    # For stepper 4:
    #   GPIO pin 12 is connected to the first coil of the stepper motor.
    #   GPIO pin 16 is connected to the second coil of the stepper motor.
    #   GPIO pin 20 is connected to the third coil of the stepper motor.
    #   GPIO pin 21 is connected to the fourth coil of the stepper motor.
    stepper4_pins = (
        GPIO("/dev/gpiochip4", 12, "out"), GPIO("/dev/gpiochip4", 16, "out"), GPIO("/dev/gpiochip4", 20, "out"),
        GPIO("/dev/gpiochip4", 21, "out"))
"""
