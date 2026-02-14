"""A program to control BEVRLink Relay 8 HAT via a simple API

Exposes a single endpoint: / set / <relay (int, 1 to 8)> / <state (on|off|blink)>
Example: /set/1/on

The relay number should be between 1 and 8, and the state should be either
"on", "off", or "blink". It will be mapped to the relevant GPIO pin.
"""

import RPi.GPIO as GPIO
from flask import Flask
import threading
import time
import requests

PING_URL = "http://172.16.20.6/api/arena/stack/home"

# GPIO output mode
GPIO.setmode(GPIO.BCM)

# Pin Aliases:
pin_alias = {
    "stack_red": 1,
    "stack_blue": 2,
    "stack_yellow": 3,
    "stack_white": 4,
    "stack_green": 5,
    "hub_red": 7,
    "hub_blue": 8,
}

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

# Dictionary to track which relays should blink
blink_states = {relay: False for relay in pin_mapping.keys()}
blink_lock = threading.Lock()

def blink_thread():
    """Single thread that handles blinking for all relays"""
    blink_phase = False
    while True:
        time.sleep(0.5)
        blink_phase = not blink_phase

        with blink_lock:
            for relay, should_blink in blink_states.items():
                if should_blink:
                    GPIO.output(pin_mapping[relay], GPIO.HIGH if blink_phase else GPIO.LOW)

# Create Flask app and endpoint
app = Flask(__name__)

@app.post("/set/<int:relay>/<string:state>")
def set_pin(relay: int, state: str):
    # Make sure that the inputs are valid
    if relay not in pin_mapping or state not in ["on", "off", "blink"]:
        return "Invalid relay or state", 400

    with blink_lock:
        if state == "blink":
            blink_states[relay] = True
        else:
            blink_states[relay] = False
            # Convert state to GPIO.HIGH or GPIO.LOW
            pin_state = GPIO.HIGH if state == "on" else GPIO.LOW
            # Drive the pin
            GPIO.output(pin_mapping[relay], pin_state)

    return "OK"


@app.post("/set/<string:relay>/<string:state>")
def set_pin_alias(relay: str, state: str):
    if relay not in pin_alias:
        return "Invalid relay alias", 400

    return set_pin(pin_alias[relay], state)

if __name__ == "__main__":
    # Set the status LED to high when app starts
    GPIO.output(status_pin, GPIO.HIGH)

    # Start the blink thread
    blink_worker = threading.Thread(target=blink_thread)
    blink_worker.daemon = True
    blink_worker.start()

    # ping host server on startup
    try:
        requests.get(PING_URL)
    except Exception:
        print("failed to ping server")
    
    app.run(host="0.0.0.0", port=80)

    # Set the status LED to low when app stops
    GPIO.output(status_pin, GPIO.LOW)
