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
from flask import Flask, Response, render_template, request
import serial
import image_capture2

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
# ser = serial.Serial('/dev/ttyACM0', 9600)

# Initialize the Flask app
app = Flask(__name__)
detected_message = ""  # empty string to hold messages


def gen_frames():
    global detected_message
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
            print('%s detected: = %.5f' % (class_label, confidence))
            if class_label == 'Base' and confidence > 0.80:
                # Check if the camera is already paused
                print("Base case here do nothing")
                time.sleep(1)
                detected_message = "Base case here, do nothing."

            elif class_label == 'Waste' and confidence > 0.80:
                # Check if the camera is already paused
                print("Trigger Arduino for Waste")
                if not camera_paused:
                    # Pause the camera by setting the variable to True
                    camera_paused = True
                    # Trigger the Waste process
                    # ser.write(b'trash')
                    detected_message = "Trigger Arduino for Waste."
                    time.sleep(3)
                    detected_message = "Sorting complete"
                # Exit the loop to prevent multiple instances of triggering
                break

            elif class_label == 'Recycling' and confidence > 0.80:
                # Check if the camera is already paused
                print("Trigger Arduino for recycle")
                # print('%s detected trigger Arduino : = %.5f' % (class_label, confidence))
                if not camera_paused:
                    # Pause the camera by setting the variable to True
                    camera_paused = True
                    # Trigger the recycling process
                    # ser.write(b'recycle')
                    detected_message = "Trigger Arduino for recycling."
                    image_capture2.capture_image()
                    time.sleep(3)

                # Exit the loop to prevent multiple instances of triggering
                break

            elif class_label == 'Compost' and confidence > 0.80:
                # Check if the camera is already paused
                print("Compost Trigger Arduino ")
                if not camera_paused:
                    # Pause the camera by setting the variable to True
                    camera_paused = True
                    # Trigger the Compost process
                    # ser.write(b'compost')
                    detected_message = "Trigger Arduino for Compost."
                    time.sleep(3)
                # Exit the loop to prevent multiple instances of triggering
                break

            # time.sleep(0.5)

        # Convert the frame to JPG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame to the Flask app
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        # If the camera is not paused, display the frame and check for user input
        if not camera_paused:
            # Exit on 'c' key
            if cv2.waitKey(1) & 0xFF == ord('c'):
                break

        # If the camera is paused, wait for 3 seconds to resume
        else:
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
    # ser.close()


def message_stream():
    global detected_message
    while True:
        # Stream the Message feed from the detection cases
        if detected_message:
            yield f'data: {detected_message}\n\n'
            detected_message = ""  # empty string
        time.sleep(0.25)


@app.route('/')
def index():
    # Render the HTML template with the video feed
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    # Stream the video feed from the camera
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/message_stream')
def message_stream_route():
    # Stream the Message feed from the detection cases
    return Response(message_stream(), content_type='text/event-stream')


@app.route('/capture_problem_image', methods=['POST'])
def capture_problem_image():
    global cap
    print("Received capture_problem_image request")

    # Capture the current frame from the camera
    ret, frame = cap.read()

    # Get the filename from the request
    data = request.get_json()
    filename = data.get('filename', f"problem_{int(time.time())}.jpg")

    # Save the frame as an image
    image_file = os.path.join(script_dir, 'captured_images', filename)
    cv2.imwrite(image_file, frame)

    return {'status': 'success', 'message': f'Image captured and saved as {filename}.'}


@app.route('/capture_sort_image', methods=['POST'])
def capture_sort_image():
    global cap
    print("Received capture_sort_image request")

    # Capture the current frame from the camera
    ret, frame = cap.read()

    # Get the filename from the request
    data = request.get_json()
    filename = data.get('filename', f"sort.jpg")

    # Save the frame as an image
    image_file = os.path.join(script_dir, 'captured_images', filename)
    cv2.imwrite(image_file, frame)

    return {'status': 'success', 'message': f'Image captured and saved as {filename}.'}


if __name__ == '__main__':
    # Start the Flask app
    app.run(host='0.0.0.0', debug=False)

"""
git commands to use -> 

cp -r /home/mendel/captured_images /home/mendel/Senior/ 
Cd Senior
git add .
git commit -m "Added captured images"
git push origin main

"""

"""
to update after changing the model use this

git pull origin main

"""


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
