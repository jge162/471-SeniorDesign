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
import serial
from periphery import GPIO
from flask import Flask, Response, render_template, request
from threading import Thread
from queue import Queue
import numpy as np

button = GPIO("/dev/gpiochip0", 6, "in")

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
ser = serial.Serial('/dev/ttyACM0', 9600)

# Initialize the Flask app
app = Flask(__name__)
detected_message = ""  # empty string to hold messages
detection_queue = Queue(maxsize=1)  # queue to hold most recent detection


def draw_bounding_box(frame, class_label, confidence, color=(0, 255, 0), thickness=2):
    height, width, _ = frame.shape
    left = int(width / 4)
    top = int(height / 4)
    right = int(3 * width / 4)
    bottom = int(3 * height / 4)

    cv2.rectangle(frame, (left, top), (right, bottom), color, thickness)
    label_text = f"{class_label}: {confidence:.2%}"
    cv2.putText(frame, label_text, (left + 5, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    return frame


def main():
    global detected_message
    camera_paused = False
    pause_start_time = None  # Initialize pause_start_time to None
    while True:

        if button.read():  # if (button press == true) enter case
            print(button.read())
            # print True in console
            timestamp = time.strftime("%m%d%Y-%H%M%S")
            # assign value of timestamp
            original_file_path = "Senior/captured_images/sort.jpg"
            # define OG file here
            problem_file_path = f"Senior/captured_images/sort_problem_{timestamp}.jpg"
            # define new file path here
            if os.path.exists(original_file_path):
                # if OG file exist enter case else print failed
                os.rename(original_file_path, problem_file_path)
                # rename OG file here
                print("Successfully renamed file")
                # print success
            else:
                print("Failed to rename file")
                # print failed

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
            print('%s detected: Confidence = %.2f%%' % (class_label, confidence * 100))
            detected_message = ('%s detected: Confidence = %.2f%%' % (class_label, confidence * 100))
            detection = (class_label, confidence)
            if detection_queue.full():
                detection_queue.get_nowait()
            detection_queue.put_nowait(detection)

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
                    if ret and frame is not None:
                        cv2.imwrite('Senior/captured_images/sort.jpg', frame)
                        print("image captured sort.jpg")
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
                    if ret and frame is not None:
                        cv2.imwrite('Senior/captured_images/sort.jpg', frame)
                        print("image captured sort.jpg")
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
                    if ret and frame is not None:
                        cv2.imwrite('Senior/captured_images/sort.jpg', frame)
                        print("image captured sort.jpg")
                    ser.write(b'compost')
                    time.sleep(3)
                # Exit the loop to prevent multiple instances of triggering
                break

            time.sleep(0.25)

        # If the camera is not paused, display the frame and check for user input
        if not camera_paused:
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


def gen_video_feed():
    global detection_queue
    last_detection = None
    while True:
        # Capture the current frame from the camera
        ret, frame = cap.read()

        if not detection_queue.empty():
            last_detection = detection_queue.get_nowait()

        if last_detection:
            class_label, confidence = last_detection
            frame = draw_bounding_box(frame, class_label, confidence)

        # Convert the frame to JPG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame to the Flask app to see on web feed
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


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
    return Response(gen_video_feed(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/message_stream')
def message_stream_route():
    # Stream the Message feed from the detection cases
    return Response(message_stream(), content_type='text/event-stream')


if __name__ == '__main__':
    main_thread = Thread(target=main)
    main_thread.start()
    app.run(host='0.0.0.0', debug=False)
