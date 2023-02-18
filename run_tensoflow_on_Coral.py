import os
import pathlib
import cv2
from pycoral.utils import edgetpu
from pycoral.utils import dataset
from pycoral.adapters import common
from pycoral.adapters import classify

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

    # Print the result
    labels = dataset.read_label_file(label_file)
    for c in classes:
        print('%s: %.5f' % (labels.get(c.id, c.id), c.score))

    # Display the frame with the confidence value
    cv2.putText(frame, "Confidence: %.2f" % c.score, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Object Detection', frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
