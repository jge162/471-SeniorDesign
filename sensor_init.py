
from periphery import GPIO
from time import time, sleep


# Initialize the ultrasonic sensor
def volume_sensor_trash ():
    echo_pin_1 = GPIO("/dev/gpiochip4", 12, "in") #22
    trigger_pin_1 = GPIO("/dev/gpiochip4", 10, "out") #18
    print("Sensor_1 OK")
    trigger_pin_1.write(False)
    sleep(0.5)

    while True:
        # Send a 10us pulse to trigger the sensor
        trigger_pin_1.write(True)
        sleep(0.00001)
        trigger_pin_1.write(False)
        print("Trigger setup")
        # Wait for the echo pin to go high
        pause_start_time_1 = time()
        while echo_pin_1.read() == 0:
            if time() - pause_start_time_1 > 1.0:
                # If the echo pin doesn't go high within 1 second, break the loop
                break
        else:
            # Record the start time if the echo pin went high
            pulse_start_1 = time()

            # Wait for the echo pin to go low
            while echo_pin_1.read() == 1:
                pass

            # Record the end time when the echo pin went low
            pulse_end_1 = time()

            # Calculate the pulse duration and the distance
            pulse_duration_1 = pulse_end_1 - pulse_start_1
            distance_1 = pulse_duration_1 * 17150

            return distance_1

def volume_sensor_recycle():
    echo_pin_2 = GPIO("/dev/gpiochip0", 6, "in") #13
    trigger_pin_2 = GPIO("/dev/gpiochip2", 9, "out") #16
    print("Sensor_2 OK")
    trigger_pin_2.write(False)
    sleep(0.5)

    while True:
        # Send a 10us pulse to trigger the sensor
        trigger_pin_2.write(True)
        sleep(0.00001)
        trigger_pin_2.write(False)
        print("Trigger setup")
        # Wait for the echo pin to go high
        pause_start_time_2 = time()
        while echo_pin_2.read() == 0:
            if time() - pause_start_time_2 > 1.0:
                # If the echo pin doesn't go high within 1 second, break the loop
                break
        else:
            # Record the start time if the echo pin went high
            pulse_start_2 = time()

            # Wait for the echo pin to go low
            while echo_pin_2.read() == 1:
                pass

            # Record the end time when the echo pin went low
            pulse_end_2 = time()

            # Calculate the pulse duration and the distance
            pulse_duration_2 = pulse_end_2 - pulse_start_2
            distance_2 = pulse_duration_2 * 17150

            return distance_2

def volume_sensor_compost():
    echo_pin_3 = GPIO("/dev/gpiochip0", 7, "in") #29
    trigger_pin_3 = GPIO("/dev/gpiochip0", 8, "out") #31
    print("Sensor_3 OK")
    trigger_pin_3.write(False)
    sleep(0.5)

    while True:
        # Send a 10us pulse to trigger the sensor
        trigger_pin_3.write(True)
        sleep(0.00001)
        trigger_pin_3.write(False)
        print("Trigger setup")
        # Wait for the echo pin to go high
        pause_start_time_3 = time()
        while echo_pin_3.read() == 0:
            if time() - pause_start_time_3 > 1.0:
                # If the echo pin doesn't go high within 1 second, break the loop
                break
        else:
            # Record the start time if the echo pin went high
            pulse_start_3 = time()

            # Wait for the echo pin to go low
            while echo_pin_3.read() == 1:
                pass

            # Record the end time when the echo pin went low
            pulse_end_3 = time()

            # Calculate the pulse duration and the distance
            pulse_duration_3 = pulse_end_3 - pulse_start_3
            distance_3 = pulse_duration_3 * 17150

            return distance_3
