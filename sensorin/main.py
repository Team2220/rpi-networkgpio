import requests, signal, sys
import RPi.GPIO as GPIO

# The URL to post when a new score is recieved
# It will post this url, with "/(red|blue)/(# of points)" appended
POST_URL = "http://172.16.20.6/api/arena/points"

DEBOUNCE_TIME = 20

#GPIO pins for sensors
sensorB1 = 25
sensorB2 = 24
sensorB3 = 23
sensorB4 = 18

sensorR1 = 12
sensorR2 = 16
sensorR3 = 20
sensorR4 = 7

# Cleanup handler
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def send_score(alliance):
    print("Sending 1 point for " + alliance)
    r = requests.post(POST_URL + f"/{alliance}/1")
    print("Request sent with status " + str(r.status_code))

# Callbacks for sensors
def callback_red(channel):
    print("event on pin " + str(channel))
    send_score("red")

def callback_blue(channel):
    print("event on pin " + str(channel))
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

    GPIO.add_event_detect(sensorB1, GPIO.RISING, callback=callback_blue, bouncetime=DEBOUNCE_TIME)
    GPIO.add_event_detect(sensorB2, GPIO.RISING, callback=callback_blue, bouncetime=DEBOUNCE_TIME)
    GPIO.add_event_detect(sensorB3, GPIO.RISING, callback=callback_blue, bouncetime=DEBOUNCE_TIME)
    GPIO.add_event_detect(sensorB4, GPIO.RISING, callback=callback_blue, bouncetime=DEBOUNCE_TIME)

    GPIO.add_event_detect(sensorR1, GPIO.RISING, callback=callback_red, bouncetime=DEBOUNCE_TIME)
    GPIO.add_event_detect(sensorR2, GPIO.RISING, callback=callback_red, bouncetime=DEBOUNCE_TIME)
    GPIO.add_event_detect(sensorR3, GPIO.RISING, callback=callback_red, bouncetime=DEBOUNCE_TIME)
    GPIO.add_event_detect(sensorR4, GPIO.RISING, callback=callback_red, bouncetime=DEBOUNCE_TIME)

    signal.signal(signal.SIGINT, signal_handler)
    print("Sensor monitoring started. Press Ctrl+C to exit.")
    signal.pause()
