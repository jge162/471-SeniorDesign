
from pynput import keyboard
import requests


ngrok_url = 'https://028c-47-155-83-198.ngrok.io'  # Update this with the correct ngrok URL


def rename_sort_image():
    response = requests.post(f'{ngrok_url}/rename_sort_image')
    if response.status_code == 200:
        print(response.json()['message'])
    else:
        print("Error renaming image.")


def on_press(key):
    try:
        if key.char == 'p':
            rename_sort_image()
            print("Successfully renamed file")
        elif key.char == 'q':
            print("Exiting...")
            return False
    except AttributeError:
        pass


def main():
    print("Press 'p' to capture an image, or 'q' to exit.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()
