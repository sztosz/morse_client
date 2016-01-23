import RPi.GPIO as GPIO
import time

time_unit = 0.5
dash = '-'
dot = '.'


def send_morse_to_pi(message):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.output(17, False)

    print(message)

    for literal in message:
        for sign in literal:
            if sign is dash:
                print(dash)
                GPIO.output(17, True)
                time.sleep(time_unit * 3)
                GPIO.output(17, False)
            elif sign is dot:
                print(dot)
                GPIO.output(17, True)
                time.sleep(time_unit * 1)
                GPIO.output(17, False)
            else:
                print('NOT A DASH NOT A DOT which basically mean error')
            time.sleep(time_unit * 1)
        time.sleep(time_unit * 3)
    print('END')
