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
import threading

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
app = Flask(__name__)  # will only run if you plug ip address into a web_browser
detected_message = ""  # empty string to hold messages


def gen_frames():
    global detected_message  # initialize a global variable for detected message
    camera_paused = False  # set boolean value to False by default
    pause_start_time = None  # initialize pause_start_time to None

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
                detected_message = "Trigger Arduino for Waste"
                if not camera_paused:
                    # Pause the camera by setting the variable to True
                    camera_paused = True
                    # Trigger the Waste process
                    ser.write(b'trash')
                    image_capture2.capture_image()
                    detected_message = "Sorting now..."
                    time.sleep(2)
                    detected_message = "Sorting complete"
                    time.sleep(1)
                # Exit case back to loop
                break

            elif class_label == 'Recycling' and confidence > 0.80:
                # Check if the camera is already paused
                print("Trigger Arduino for recycle")
                detected_message = "Trigger Arduino for recycling"
                if not camera_paused:
                    # Pause the camera by setting the variable to True
                    camera_paused = True
                    print("Pause camera for 3 seconds")
                    # Trigger the recycling process
                    ser.write(b'recycle')
                    image_capture2.capture_image()
                    detected_message = "Sorting now..."
                    time.sleep(2)
                    detected_message = "Sorting complete"
                    time.sleep(1)

                # Exit case back to loop
                break

            elif class_label == 'Compost' and confidence > 0.80:
                # Check if the camera is already paused
                print("Compost Trigger Arduino ")
                detected_message = "Trigger Arduino for Compost"
                if not camera_paused:
                    # Pause the camera by setting the variable to True
                    camera_paused = True
                    # Trigger the Compost process
                    ser.write(b'compost')
                    image_capture2.capture_image()
                    detected_message = "Sorting now..."
                    time.sleep(2)
                    detected_message = "Sorting complete"
                    time.sleep(1)

                # Exit case back to loop
                break

        # If the camera is not paused, display the frame and check for user input
        if not camera_paused:
            pass   # placeholder, can add print statement if you want.
            break  # break out of case, necessary to reach cap.release(), ser.close() etc...

        else:
            # If the camera is paused, wait for 3 seconds to resume
            if not pause_start_time:
                pause_start_time = time.time()
            elif time.time() - pause_start_time >= 3:
                pause_start_time = None
                camera_paused = False  # turn camera back on here, set pause = False

    # Release the camera, close the window and close serial connection
    cap.release()
    cv2.destroyAllWindows()
    ser.close()


def gen_video_feed():
    while True:
        # Capture the current frame from the camera
        ret, frame = cap.read()

        # Convert the frame to JPG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame to the Flask app to see on web feed
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def start_gen_frames():
    # dedicated thread to run, sorting functionality
    gen_frames_thread = threading.Thread(target=gen_frames)
    gen_frames_thread.daemon = True
    gen_frames_thread.start()  # start sorting once script is run here


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


@app.route('/rename_sort_image', methods=['POST'])
def rename_sort_image():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    original_file_path = "Senior/captured_images/sort.jpg"
    problem_file_path = f"Senior/captured_images/sort_problem_{timestamp}.jpg"

    if os.path.exists(original_file_path):
        os.rename(original_file_path, problem_file_path)
        return {'status': 'success', 'message': f'Image renamed to {problem_file_path}.'}
    else:
        return {'status': 'error', 'message': 'No image to rename.'}


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
    image_file = os.path.join(script_dir, 'Senior/captured_images', filename)
    cv2.imwrite(image_file, frame)

    return {'status': 'success', 'message': f'Image captured and saved as {filename}.'}


if __name__ == '__main__':
    start_gen_frames()  # auto start sorting function (dedicated thread)
    app.run(host='0.0.0.0', debug=False)  # Start the Flask app by entering http into a webpage

"""
git commands to use -> 

cp -r /home/mendel/captured_images /home/mendel/Senior/ 
cd Senior
git add .
git commit -m "Added captured images"
git push origin main

to update after changing the model use this

git pull origin main
