
import sensor_init as sr
from periphery import GPIO

led_trash = GPIO("/dev/gpiochip2", 9, "out")  # P16_out
led_recycle = GPIO("/dev/gpiochip2", 9, "out")  # P16_out
led_compost = GPIO("/dev/gpiochip2", 9, "out")  # P16_out

def check_for_trash():

    while True:
        trash_bin = sr.volume_sensor_trash()
        recycle_bin = sr.volume_sensor_recycle()
        compost_bin = sr.volume_sensor_compost()
        # print(bin_1)

        if trash_bin <= 10:
            led_trash.write(True)
            print("Trash bin is full")
        #   ser.write(b'trash_full')
        else:
            led_trash.write(False)

        if recycle_bin <= 10:
            led_recycle.write(True)
            print("Recycle bin is full")
        #    ser.write(b'recycle_full')
        else:
            led_recycle.write(False)

        if compost_bin <= 10:
            led_compost.write(True)
            print("Compost bin is full")
        #    ser.write(b'compost_full')
        else:
            led_compost.write(False)

    sleep(2)