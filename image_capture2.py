# image_capture.py
import requests
import time

ngrok_url = 'https://82a8-47-155-83-198.ngrok.io'


def capture_image():
    print("Capturing sort image...")
    filename = f"sort.jpg"
    response = requests.post(f'{ngrok_url}/capture_sort_image', json={'filename': filename})
    if response.status_code == 200:
        print(response.json()['message'])
    else:
        print("Error capturing image.")
