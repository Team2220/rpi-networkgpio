"""A program to control BEVRLink Relay 8 HAT via a simple API

Exposes a single endpoint: / set / <relay (int, 1 to 8)> / <state (on|off)>
Example: /set/1/on

The relay number should be between 1 and 8, and the state should be either
"on" or "off". It will be mapped to the relevant GPIO pin.
"""

import RPi.GPIO as GPIO
from flask import Flask

# GPIO output mode
GPIO.setmode(GPIO.BCM)

# Map relay numbers to GPIO pins
pin_mapping = {
    1: 5,
    2: 6,
    3: 13,
    4: 16,
    5: 19,
    6: 20,
    7: 21,
    8: 26
}

status_pin = 12

# Set pins as output
for pin in pin_mapping.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

GPIO.setup(status_pin, GPIO.OUT)
GPIO.output(status_pin, GPIO.LOW)


# Create Flask app and endpoint
app = Flask(__name__)


@app.post("/set/<int:relay>/<str:state>")
def set_pin(relay: int, state: str):
    # Make sure that the inputs are valid
    if relay not in pin_mapping or state not in ["on", "off"]:
        return "Invalid relay or state", 400

    # Convert state to GPIO.HIGH or GPIO.LOW
    pin_state = GPIO.HIGH if state == "on" else GPIO.LOW

    # Drive the pin
    GPIO.output(pin_mapping[relay], pin_state)
    return "OK"

if __name__ == "__main__":
    # Set the status LED to high when app starts
    GPIO.output(status_pin, GPIO.HIGH)

    app.run(host="0.0.0.0")

    # Set the status LED to low when app stops
    GPIO.output(status_pin, GPIO.LOW)