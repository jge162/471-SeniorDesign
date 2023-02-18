"""
# This is a sample Python script.
import os
import pathlib
from pycoral.utils import edgetpu
from pycoral.utils import dataset
from pycoral.adapters import common
from pycoral.adapters import classify
from PIL import Imagesudo

# Specify the TensorFlow model, labels, and image
script_dir = pathlib.Path(__file__).parent.absolute()
model_file = os.path.join(script_dir, 'mobilenet_v2_1.0_224_quant_edgetpu.tflite')
label_file = os.path.join(script_dir, 'imagenet_labels.txt')
image_file = os.path.join(script_dir, 'parrot.jpg')

# Initialize the TF interpreter
interpreter = edgetpu.make_interpreter(model_file)
interpreter.allocate_tensors()

# Resize the image
size = common.input_size(interpreter)
image = Image.open(image_file).convert('RGB').resize(size, Image.ANTIALIAS)

# Run an inference
common.set_input(interpreter, image)
interpreter.invoke()
classes = classify.get_classes(interpreter, top_k=1)

# Print the result
labels = dataset.read_label_file(label_file)
for c in classes:
  print('%s: %.5f' % (labels.get(c.id, c.id), c.score))
"""
"""
import tflite_runtime.interpreter as tflite
import numpy as np
import cv2
import serial
import time
import platform

EDGETPU_SHARED_LIB = {
    'Linux': 'libedgetpu.so.1',
    'Darwin': 'libedgetpu.1.dylib',
    'Windows': 'edgetpu.dll'
}[platform.system()]


def make_interpreter(model_file):
    model_file, *device = model_file.split('@')
    return tflite.Interpreter(
        model_path=model_file,
        experimental_delegates=[
            tflite.load_delegate(EDGETPU_SHARED_LIB,
                                 {'device': device[0]} if device else {})
        ])


# Load the TensorFlow Lite object detection model
interpreter = make_interpreter("2-17model.tflite")
interpreter.allocate_tensors()

# Get the input and output tensors from the model
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Open the USB camera
cap = cv2.VideoCapture(1)

# Set up the serial connection to the Arduino
# ser = serial.Serial('/dev/ttyACM0', 9600)

# Define the class labels and the corresponding trigger actions
labels = {
    'Base': b'A',
    'Recycling': b'B',
    'Waste': b'C'
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
    max_conf = 10
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
    # ser.write(trigger)

    # Give the Arduino some time to process the data
    time.sleep(1)

# Release the camera and close the serial connection
cap.release()
ser.close()
"""

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
""" 
import os
import pathlib
from pycoral.utils import edgetpu
from pycoral.utils import dataset
from pycoral.adapters import common
from pycoral.adapters import classify
from PIL import Image
import cv2


# Specify the TensorFlow model, labels, and image
script_dir = pathlib.Path(__file__).parent.absolute()
model_file = os.path.join(script_dir, 'demo_files/mobilenet_v2_1.0_224_quant_edgetpu.tflite')
label_file = os.path.join(script_dir, 'demo_files/imagenet_labels.txt')
# image_file = os.path.join(script_dir, 'coke.jpg')
# Open the USB camera
cap = cv2.VideoCapture(1)

# Initialize the TF interpreter
interpreter = edgetpu.make_interpreter(model_file)
interpreter.allocate_tensors()

# Resize the image
size = common.input_size(interpreter)
image = Image.open(image_file).convert('RGB').resize(size, Image.ANTIALIAS)

# Run an inference
common.set_input(interpreter, image)
interpreter.invoke()
classes = classify.get_classes(interpreter, top_k=1)

# Print the result
labels = dataset.read_label_file(label_file)
for c in classes:
  print('%s: %.5f' % (labels.get(c.id, c.id), c.score))
"""

import tflite_runtime.interpreter as tflite
import cv2
import numpy as np
import serial
import platform

EDGETPU_SHARED_LIB = {
    'Linux': 'libedgetpu.so.1',
    'Darwin': 'libedgetpu.1.dylib',
    'Windows': 'edgetpu.dll'
}[platform.system()]


def make_interpreter(model_file):
    model_file, *device = model_file.split('@')
    return tflite.Interpreter(
        model_path=model_file,
        experimental_delegates=[
            tflite.load_delegate(EDGETPU_SHARED_LIB,
                                 {'device': device[0]} if device else {})
        ])


# Load the TensorFlow Lite object detection model
interpreter = make_interpreter("2-17model.tflite")
interpreter.allocate_tensors()


# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Define the preprocess function to resize the frame and normalize the pixel values
def preprocess_frame(frame):
    frame = cv2.resize(frame, (input_details[0]['shape'][2], input_details[0]['shape'][1]))
    frame = frame.astype(np.float32) / 255.0
    frame = (frame * 255).astype(np.uint8)
    frame = np.expand_dims(frame, axis=0)
    return frame

# Define the postprocess function to decode the output tensor and filter low-confidence detections
def postprocess_output(output_data):
    threshold = 0.5
    detections = []
    for i in range(output_data.shape[0]):
        confidence = output_data[i, 2]
        if confidence > threshold:
            class_id = int(output_data[i, 2])
            label = labels[class_id]
            detections.append({'label': label, 'confidence': confidence})
    return detections

# Open the camera and set the resolution
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Define the labels for the classes in your model
labels = ['Base', 'Recycling', 'Waste']

# Loop through frames and run the model on each one
while True:
    # Capture a frame from the camera
    ret, frame = cap.read()

    # Preprocess the frame
    input_data = preprocess_frame(frame)

    # Set the input tensor data
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Run the model
    interpreter.invoke()

    # Get the output tensor data
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # Postprocess the output tensor data
    detections = postprocess_output(output_data)

    # Print high-confidence detections
    for detection in detections:
        if detection['confidence'] > 0.8:
            print("Detected {}: {:.2f}%".format(detection['label'], detection['confidence'] * 100))

    # Display the frame with the detected objects
    cv2.imshow('frame', frame)

    # Wait for a key press and exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
