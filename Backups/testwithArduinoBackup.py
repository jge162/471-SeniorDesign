import os
import pathlib
import cv2
from pycoral.utils import edgetpu
from pycoral.utils import dataset
from pycoral.adapters import common
from pycoral.adapters import classify
import serial
from periphery import GPIO
from time import time, sleep

# Set up the GPIO pin for the LED
led = GPIO("/dev/gpiochip2", 9, "out")  # P16_out
print("LED OK")
# Initialize the ultrasonic sensor
echo_pin = GPIO("/dev/gpiochip4", 12, "in")
trigger_pin = GPIO("/dev/gpiochip4", 10, "out")
print("Sensor OK")
trigger_pin.write(False)
sleep(2)

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

while True:
    # Send a 10us pulse to trigger the sensor
    trigger_pin.write(True)
    sleep(0.00001)
    trigger_pin.write(False)
    # print("Trigger setup")
    # Wait for the echo pin to go high
    pause_start_time = time()
    while echo_pin.read() == 0:
        if time() - pause_start_time > 1.0:
            # If the echo pin doesn't go high within 1 second, break the loop
            break
    else:
        # Record the start time if the echo pin went high
        pulse_start = time()

        # Wait for the echo pin to go low
        while echo_pin.read() == 1:
            pass

        # Record the end time when the echo pin went low
        pulse_end = time()

        # Calculate the pulse duration and the distance
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150

        # Check if a human is detected (distance < 100cm)
        if distance >= 65 or distance == 0:
            # Turn off the LED
            led.write(False)
            print("No human detected")
        else:
            # Turn on the LED
            led.write(True)
            print("Detected", distance, "cm")
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
                    print('%s detected: = %.5f' % (class_label, confidence))
                    if class_label == 'Base' and confidence > 0.80:
                        # Check if the camera is already paused
                        print("Base case here do nothing")
                        sleep(1)
                        # led.write(False)
                        break
                    elif class_label == 'Waste' and confidence > 0.80:
                        # Check if the camera is already paused
                        print("Trigger Arduino for Waste")
                        if not camera_paused:
                            # Pause the camera by setting the variable to True
                            camera_paused = True
                            # Trigger the recycling process
                            sleep(2)
                            ser.write(b'trash')
                            sleep(3)
                        # Exit the loop to prevent multiple instances of triggering
                        break
                    elif class_label == 'Recycling' and confidence > 0.80:
                        # Check if the camera is already paused
                        print("Trigger Arduino for recycle")
                        if not camera_paused:
                            # Pause the camera by setting the variable to True
                            camera_paused = True
                            # Trigger the recycling process
                            sleep(2)
                            ser.write(b'recycle')
                            sleep(3)
                        # Exit the loop to prevent multiple instances of triggering
                        break
                    elif class_label == 'Compost' and confidence > 0.80:
                        # Check if the camera is already paused
                        print("Compost Trigger Arduino ")
                        if not camera_paused:
                            # Pause the camera by setting the variable to True
                            camera_paused = True
                            # Trigger the recycling process
                            sleep(2)
                            ser.write(b'compost')
                            sleep(3)
                        # Exit the loop to prevent multiple instances of triggering
                        break
                # If the camera is not paused, display the frame and check for user input
                if not camera_paused:
                    print('%s detected: = %.5f' % (class_label, confidence))
                    # Display the frame with the confidence value
                    cv2.putText(frame, "Confidence: %.2f" % confidence, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 0, 255), 2)
                    cv2.imshow('Object Detection', frame)

                    # Exit on 'c' key
                    if cv2.waitKey(1) & 0xFF == ord('c'):
                        break

                # If the camera is paused, wait for a key press to resume
                else:
                    # Display a message indicating that the camera is paused
                    cv2.putText(frame, "Camera paused. Waiting for 3 seconds to resume...", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                (0, 0, 255), 2)
                    cv2.imshow('Object Detection', frame)

                    # Wait for 3 seconds
                    if not pause_start_time:
                        pause_start_time = time()
                    elif time() - pause_start_time >= 3:
                        pause_start_time = None
                        camera_paused = False

                    # Exit on 'c' key
                if cv2.waitKey(1) & 0xFF == ord('c'):
                    break

                    # Release the camera and close the window
            cap.release()
            cv2.destroyAllWindows()
            ser.close()
            break

    break
# Wait a short period before reading again
# sleep(2)
