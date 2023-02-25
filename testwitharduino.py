from periphery import GPIO
from time import sleep, time

# Set up the GPIO pin for the LED
led = GPIO("/dev/gpiochip2", 9, "out")  # P16_out
print("LED OK")
# Initialize the ultrasonic sensor
echo_pin = GPIO("/dev/gpiochip4", 12, "in")
trigger_pin = GPIO("/dev/gpiochip4", 10, "out")
print("Sensor OK")
trigger_pin.write(False)
sleep(2)

while True:
    # Send a 10us pulse to trigger the sensor
    trigger_pin.write(True)
    sleep(0.00001)
    trigger_pin.write(False)
    # print("Trigger setup")
    # Wait for the echo pin to go high
    start_time = time()
    while echo_pin.read() == 0:
        if time() - start_time > 1.0:
            # If the echo pin doesn't go high within 1 second, break the loop
            break
    else:
        # Record the start time if the echo pin went high
        pulse_start = time()

        # Wait for the echo pin to go low
        while echo_pin.read() == 1:
            pass

        # Record the end time when the echo pin went low
        pulse_end = time()

        # Calculate the pulse duration and the distance
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150

        # Check if a human is detected (distance < 100cm)
        if distance >= 65 or distance == 0:
            # Turn off the LED
            led.write(False)
            print("No human detected")
        else:
            # Turn on the LED
            led.write(True)

            print("Detected", distance, "cm")

    # Wait a short period before reading again
    sleep(2)
