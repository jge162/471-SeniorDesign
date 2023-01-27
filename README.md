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
Note that you will need to replace <coral-board-ip-address> with the IP address of your Coral development board. Also, you may also need to install requests library using pip install requests

This code snippet uses the requests library to send a POST request to the Coral board with the tflite file as the data. The response from the Coral board is then printed to the console.
```
