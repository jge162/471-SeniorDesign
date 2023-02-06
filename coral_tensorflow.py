import tensorflow as tf
import numpy as np
import cv2
import serial
import time

# Load the TensorFlow Lite object detection model
interpreter = tf.lite.Interpreter(model_path="detection_model.tflite")
interpreter.allocate_tensors()

# Get the input and output tensors from the model
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Open the USB camera
cap = cv2.VideoCapture(0)

# Set up the serial connection to the Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)

# Define the class labels and the corresponding trigger actions
labels = {
    'dog': b'A',
    'cat': b'B',
    'car': b'C'
}

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()

    # Resize the frame to match the input size of the model
    frame = cv2.resize(frame, (input_details[0]['shape'][2], input_details[0]['shape'][1]))

    # Add an extra dimension to the frame to match the input shape of the model
    frame = np.expand_dims(frame, axis=0)

    # Run the TensorFlow Lite object detection model on the frame
    interpreter.set_tensor(input_details[0]['index'], frame)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])

    # Extract the detection results
    detections = output[0]

    # Find the class label with the highest confidence score
    max_conf = 0
    detected_class = None
    for detection in detections:
        conf = detection[2]
        if conf > max_conf:
            max_conf = conf
            class_id = int(detection[1])
            detected_class = labels[class_id]

    # Look up the corresponding trigger action for the detected class
    trigger = labels.get(detected_class)

    # Send the trigger action over the serial connection to the Arduino
    ser.write(trigger)

    # Give the Arduino some time to process the data
    time.sleep(1)

# Release the camera and close the serial connection
cap.release()
ser.close()


"""
pip install opencv-python
python3 -m pip install tensorflow

"""

"""

To run the TensorFlow Lite object detection model on the Google Coral Dev Board, you'll need to install the Edge TPU 
runtime and TensorFlow Lite library on the board.
Here is an overview of how you would run the model on the Coral Dev Board:

* Connect the Coral Dev Board to your computer using a USB cable.

* Flash the latest version of the Debian-based operating system to the board using the instructions provided by Google.

*Connect the USB camera to the Coral Dev Board.

*Copy the TensorFlow Lite object detection model and the Python code to the Coral Dev Board. You can use a tool such as 
scp to copy the files over a secure shell connection.

*Install the required libraries on the Coral Dev Board, including TensorFlow Lite, OpenCV, and PySerial.

*Run the Python code on the Coral Dev Board using the Python interpreter.

*The code will use the TensorFlow Lite library to run the object detection model on each frame captured from the camera.
The results of the object detection will be sent over the serial connection to the Arduino using the PySerial library.

*Note that you may need to modify the code slightly to run on the Coral Dev Board, depending on the specific 
configuration and setup of your device.

"""
