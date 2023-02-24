
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
                ser = serial.Serial('/dev/ttyACM0', 9600)
                ser.write(b'trash\n')
                time.sleep(3)
                ser.close()

            elif class_label == 'Water Bottle' and confidence * 100 >= 99:
                print("Trigger Arduino to recycle Water Bottle")
                ser = serial.Serial('/dev/ttyACM0', 9600)
                ser.write(b'compost\n')
                ser.close()

            elif class_label == 'Paper plate' and confidence * 100 >= 99:
                print("Trigger Arduino to trash Paper plate")
                ser = serial.Serial('/dev/ttyACM0', 9600)
                ser.write(b'composting\n')
                ser.close()

            # time.sleep(0.2)  # slowdown camera

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


if __name__ == '__main__':
    main()
