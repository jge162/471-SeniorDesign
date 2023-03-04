"""
git clone https://github.com/jge162/Senior.git
type this into terminal once Andrew uploads zip files
sudo rm -rf Senior

mdt push PycharmProjects/InferenceCoral/main.py
"""

""" 
import os
import pathlib
import time
import cv2
from pycoral.utils import edgetpu
from pycoral.utils import dataset
from pycoral.adapters import common
from pycoral.adapters import classify
import serial

# Specify the TensorFlow model, labels, and camera device
script_dir = pathlib.Path(__file__).parent.absolute()
model_file = os.path.join(script_dir, 'Senior/model_edgetpu.tflite')
label_file = os.path.join(script_dir, 'Senior/labelss.txt')
device = 0
width = 640
height = 480

# Initialize the TF interpreter
interpreter = edgetpu.make_interpreter(model_file)
interpreter.allocate_tensors()

# Open the camera device
cap = cv2.VideoCapture(device)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


# ser = serial.Serial('/dev/ttyACM0', 9600)


def main():
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
            print('%s detected: %.2f%%' % (class_label, confidence * 100))

            if class_label == 'Toilet Paper' and confidence * 100 >= 99:
                print("HERE IS BASE CASE DO NOTHING WITH ARDUINO")

            elif class_label == 'SodaCan' and confidence * 100 >= 99.60:
                print("Trigger Arduino to recycle SodaCan")
                time.sleep(3)

        # Display the frame with the confidence value if Coral is connected to a monitor
        cv2.putText(frame, "Confidence: %.3f%%" % (confidence * 100), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 2)
        cv2.imshow('Object Detection', frame)

        # Exit on 'c' key
        if cv2.waitKey(1) & 0xFF == ord('c'):
            break

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()
    # ser.close()


if __name__ == '__main__':
    main()
"""

import os
import pathlib
import time
import cv2
from pycoral.utils import edgetpu
from pycoral.utils import dataset
from pycoral.adapters import common
from pycoral.adapters import classify
import serial

# Specify the TensorFlow model, labels, and camera device
script_dir = pathlib.Path(__file__).parent.absolute()
model_file = os.path.join(script_dir, 'Senior/model_edgetpu.tflite')
label_file = os.path.join(script_dir, 'Senior/labels.txt')
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
ser = serial.Serial('/dev/ttyACM0', 9600)


def main():
    # Call the setup function to initialize the GPIO pins and stepper motors.
    # Loop over frames from the camera
    camera_paused = False
    pause_start_time = None  # Initialize pause_start_time to None
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

            if class_label == 'Base' and confidence > 0.80:
                # Check if the camera is already paused
                print("Base case here do nothing")

            elif class_label == 'Waste' and confidence > 0.80:
                # Check if the camera is already paused
                print("Trigger Arduino for Waste")
                if not camera_paused:
                    # Pause the camera by setting the variable to True
                    camera_paused = True
                    # Trigger the recycling process
                    time.sleep(2)
                    ser.write(b'trash')
                    time.sleep(3)
                # Exit the loop to prevent multiple instances of triggering
                break
            elif class_label == 'Recycling' and confidence > 0.80:
                # Check if the camera is already paused
                print("Trigger Arduino for recycle")
                if not camera_paused:
                    # Pause the camera by setting the variable to True
                    camera_paused = True
                    # Trigger the recycling process
                    time.sleep(2)
                    ser.write(b'recycle')
                    time.sleep(3)
                # Exit the loop to prevent multiple instances of triggering
                break

            elif class_label == 'Compost' and confidence > 0.80:
                # Check if the camera is already paused
                print("Compost Trigger Arduino ")
                if not camera_paused:
                    # Pause the camera by setting the variable to True
                    camera_paused = True
                    # Trigger the recycling process
                    time.sleep(2)
                    ser.write(b'compost')
                    time.sleep(3)
                # Exit the loop to prevent multiple instances of triggering
                break

            time.sleep(0.5)

        # If the camera is not paused, display the frame and check for user input
        if not camera_paused:
            # time.sleep(2)
            print('%s detected: = %.5f' % (class_label, confidence))
            # Display the frame with the confidence value
            cv2.putText(frame, "Confidence: %.2f" % confidence, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Object Detection', frame)

            # Exit on 'c' key
            if cv2.waitKey(1) & 0xFF == ord('c'):
                break

        # If the camera is paused, wait for a key press to resume
        else:
            # Display a message indicating that the camera is paused
            cv2.putText(frame, "Camera paused. Waiting for 3 seconds to resume...", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255), 2)
            cv2.imshow('Object Detection', frame)

            # Wait for 3 seconds
            if not pause_start_time:
                pause_start_time = time.time()
            elif time.time() - pause_start_time >= 3:
                pause_start_time = None
                camera_paused = False

            # Exit on 'c' key
        if cv2.waitKey(1) & 0xFF == ord('c'):
            break

            # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()
    ser.close()


if __name__ == '__main__':
    main()

# --------------------------------------------
