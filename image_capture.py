# image_capture.py
import requests
import time

ngrok_url = 'https://82a8-47-155-83-198.ngrok.io'


def capture_image():
    print("Capturing problem image...")
    timestamp = time.strftime("%Y%m%d-%H%M%S")  # Add this line to get the current timestamp in the desired format
    filename = f"problem_{timestamp}.jpg"
    response = requests.post(f'{ngrok_url}/capture_problem_image', json={'filename': filename})
    if response.status_code == 200:
        print(response.json()['message'])
    else:
        print("Error capturing image.")
