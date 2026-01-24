import requests, signal, sys
import RPi.GPIO as GPIO

#GPIO pins for sensors
sensorB1 = 0
sensorB2 = 0
sensorB3 = 0

sensorR1 = 0
sensorR2 = 0
sensorR3 = 0

# Cleanup handler
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def send_score(alliance):
    r = requests.post('0.0.0.0', json=alliance)
    print("Request sent with status " + r.status_code)

# Callbacks for sensors
def callback_red():
    send_score("red")

def callback_blue():
    send_score("blue")

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensorB1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(sensorB2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(sensorB3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.setup(sensorR1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(sensorR2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(sensorR3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(sensorB1, GPIO.RISING, callback=callback_blue, bouncetime=300)
    GPIO.add_event_detect(sensorB2, GPIO.RISING, callback=callback_blue, bouncetime=300)
    GPIO.add_event_detect(sensorB3, GPIO.RISING, callback=callback_blue, bouncetime=300)

    GPIO.add_event_detect(sensorR1, GPIO.RISING, callback=callback_red, bouncetime=300)
    GPIO.add_event_detect(sensorR2, GPIO.RISING, callback=callback_red, bouncetime=300)
    GPIO.add_event_detect(sensorR3, GPIO.RISING, callback=callback_red, bouncetime=300)