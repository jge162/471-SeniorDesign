# scp /Users/csuftitan/PycharmProjects/pythonProject2/main.py mendel@192.168.100.2:/home/mendel
# ssh mendel@192.168.100.2
# sudo passwd mendel
# sudo nano /etc/ssh/sshd_config
"""
PasswordAuthentication yes
ChallengeResponseAuthentication no
UsePAM yes
"""
# sudo systemctl restart sshd

import os
import pathlib
import time
import cv2
from pycoral.utils import edgetpu
from pycoral.utils import dataset
from pycoral.adapters import common
from pycoral.adapters import classify
from flask import Flask, Response, render_template

# Specify the TensorFlow model, labels, and camera device
script_dir = pathlib.Path(__file__).parent.absolute()
model_file = os.path.join(script_dir, 'Senior/model_edgetpu.tflite')
label_file = os.path.join(script_dir, 'Senior/labels.txt')
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

# Initialize the Flask app
app = Flask(__name__)


def gen_frames():
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

            elif class_label == 'Recycling' and confidence > 0.80:
                # Check if the camera is already paused
                print("Trigger Arduino to recycle")

        # Convert the frame to JPG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame to the Flask app
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    # Render the HTML template with the video feed
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    # Stream the video feed from the camera
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # Start the Flask app
    app.run(host='0.0.0.0', debug=False)

""" 
<!DOCTYPE html>
<html>
  <head>
    <title>Camera Streaming</title>
  </head>
  <body>
    <h1>Camera Streaming</h1>
    <img src="{{ url_for('video_feed') }}">
  </body>
</html>
"""

"""
edgetpu_detect
sudo apt-get install python3-pycoral
sudo apt-get install python3-edgetpu


pip install Flask
sudo apt-get install python3-opencv
only use below is needed 
sudo apt-get remove libedgetpu1-std
sudo apt-get remove python3-tflite-runtime
sudo apt-get autoremove
sudo apt-get update
sudo apt-get install libedgetpu1-std python3-tflite-runtime


"""

"""
$ cd /path/to/main.py
$ mkdir templates
$ nano templates/index.html

"""
