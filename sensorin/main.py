import requests, signal, sys
import RPi.GPIO as GPIO

# The URL to post when a new score is recieved
POST_URL = "http://0.0.0.0"

#GPIO pins for sensors
sensorB1 = 17
sensorB2 = 27
sensorB3 = 22
sensorB4 = 23

sensorR1 = 24
sensorR2 = 25
sensorR3 = 26
sensorR4 = 16

# Cleanup handler
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def send_score(alliance):
    print("Sending score for " + alliance)
    r = requests.post(POST_URL, json=alliance)
    print("Request sent with status " + r.status_code)

# Callbacks for sensors
def callback_red(channel):
    send_score("red")

def callback_blue(channel):
    send_score("blue")

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensorB1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(sensorB2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(sensorB3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(sensorB4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.setup(sensorR1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(sensorR2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(sensorR3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(sensorR4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(sensorB1, GPIO.RISING, callback=callback_blue, bouncetime=300)
    GPIO.add_event_detect(sensorB2, GPIO.RISING, callback=callback_blue, bouncetime=300)
    GPIO.add_event_detect(sensorB3, GPIO.RISING, callback=callback_blue, bouncetime=300)
    GPIO.add_event_detect(sensorB4, GPIO.RISING, callback=callback_blue, bouncetime=300)

    GPIO.add_event_detect(sensorR1, GPIO.RISING, callback=callback_red, bouncetime=300)
    GPIO.add_event_detect(sensorR2, GPIO.RISING, callback=callback_red, bouncetime=300)
    GPIO.add_event_detect(sensorR3, GPIO.RISING, callback=callback_red, bouncetime=300)
    GPIO.add_event_detect(sensorR4, GPIO.RISING, callback=callback_red, bouncetime=300)

    signal.signal(signal.SIGINT, signal_handler)
    print("Sensor monitoring started. Press Ctrl+C to exit.")
    signal.pause()
