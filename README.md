# EGCP471
Senior design project

[GPIO for Dev board](https://coral.ai/docs/dev-board/gpio/#program-gpios-with-libgpiod)

python3 -m pip install python-periphery

[Connect to dev board serially with mac](https://coral.ai/docs/dev-board/serial-console/#connect-with-macos)

```python
import requests

# Set the URL for the Coral development board
url = "http://<coral-board-ip-address>/model"

# Read in the tflite file
with open("model.tflite", "rb") as f:
    data = f.read()

# Send the tflite file to the Coral board
r = requests.post(url, data=data)

# Print the response from the Coral board
print(r.text)
# Note that you will need to replace <coral-board-ip-address> with the IP address of your Coral development board. Also, you may also need to install requests library using pip install requests

# This code snippet uses the requests library to send a POST request to the Coral board with the tflite file as the data. The response from the Coral board # is then printed to the console.
import serial
import time

# Set the serial port for the Arduino
arduino = serial.Serial('COM3', 9600)

# Wait for the Arduino to initialize
time.sleep(2)

# Send a command to the Arduino to turn on an LED connected to pin 13
arduino.write(b'13,1')

# Wait for the command to be executed
time.sleep(1)

# Send a command to the Arduino to turn off the LED
arduino.write(b'13,0')

# Close the serial port
arduino.close()
You would need to install pyserial library using pip install pyserial

This code snippet uses the pyserial library to communicate with the Arduino over a serial connection. The Serial class is used to open a connection to the Arduino on the specified serial port (in this case, COM3) at a baud rate of 9600. The code sends a command to the Arduino to turn on an LED connected to pin 13, waits for the command to be executed, and then sends a command to turn off the LED.

It is important to note that, in order for the Arduino to receive the commands from the Coral board, you will need to have the appropriate code loaded on the Arduino that listens for serial commands and controls the GPIO pins accordingly. The above code is just for sending the commands from Coral Dev board to Arduino.




```
