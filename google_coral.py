"""
Yes, it is possible to use PyCoral to control the Google
Coral Dev Board in PyCharm. PyCoral is a Python library
that provides a convenient interface for interacting with
the Google Coral devices, including the Dev Board. To use
PyCoral in PyCharm, you will first need to install the library,
and then import it into your Python script. From there, you can
use the library's functions and classes to interact with the
Dev Board, such as performing inferences on TensorFlow Lite models
or controlling the device's peripherals.
"""
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

"""
Then you can use the above example code to load the model and perform inferences 
on the Dev Board. It's worth noting that, the Edge TPU provides faster
 inferencing than the host machine, so loading the model on the Edge TPU 
 would be beneficial if you are doing real-time inferencing or if the model is 
 too large to fit in the host machine's memory.
"""
