
import pycoral.coral as coral
import numpy as np
import tensorflow as tf

# Create a new Edge TPU device
edgetpu_device = coral.Device()

# Load the TensorFlow Lite model
model = edgetpu_device.LoadTensorFlowModel("path/to/model.tflite")

# Perform inferences
input_tensor = model.get_input_tensor(0)
output_tensor = model.get_output_tensor(0)
results = model.RunInference(input_tensor)
print(results)



# Load the TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path="path/to/model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Create input data
input_data = np.array(...) # Replace with your input data

# Set the input tensor
interpreter.set_tensor(input_details[0]['index'], input_data)

# Perform inferences
interpreter.invoke()

# Get the output tensor
output_data = interpreter.get_tensor(output_details[0]['index'])

print(output_data)

scp model.tflite <username>@<ip-address-of-coral-dev-board>:/path/to/model.tflite

