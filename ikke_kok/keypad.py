"""Class for handling keypad"""
import RPi.GPIO as GPIO
import time

class Keypad:

    def __init__(self):
        key_pairs = {1:(18, 17), 2:(18, 27), 3:(18, 22), 4:(23, 17), 5:(23, 27), 6:(23, 22),
                        7:(24, 17), 8:(24, 27), 9:(24, 22), '*':(25, 17), 0:(25, 27), '#'(25, 22)}

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.out)
        GPIO.setup(23, GPIO.out)
        GPIO.setup(24, GPIO.out)
        GPIO.setup(25, GPIO.out)

        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def do_polling(self):
        for item_1 in [18, 23, 24, 25]:
            GPIO.output(item_1, HIGH)
            for item_2 in [17, 22, 27]:
                for i in range(10):
                    x = 0
                    if GPIO.input(item_2) == GPIO.HIGH:
                        time.sleep(10)
                        x += 1
                if x = 10:
                    GPIO.output(item_1, LOW)
                    return (item_1, item_2)
            GPIO.output(item_1, LOW)
            return None
