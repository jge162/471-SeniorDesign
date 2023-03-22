
from pynput import keyboard
import image_capture


def on_press(key):
    try:
        if key.char == 'p':
            image_capture.capture_image()
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
