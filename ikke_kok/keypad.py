"""Class for handling keypad"""
import time
#import RPi.GPIO as GPIO


class KeyPad:

    def __init__(self):
        key_pairs = {(18, 17): 1,
                     (18, 27): 2,
                     (18, 22): 3,
                     (23, 17): 4,
                     (23, 27): 5,
                     (23, 22): 6,
                     (24, 17): 7,
                     (24, 27): 8,
                     (24, 22): 9,
                     (25, 17): '*',
                     (25, 27): 0,
                     (25, 22): '#'}

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
                x = 0
                while GPIO.input(item_2) == GPIO.HIGH:
                    time.sleep(0.01)
                    x += 1
                    if x == 10:
                        GPIO.output(item_1, GPIO.LOW)
                        return (item_1, item_2)
            GPIO.output(item_1, GPIO.LOW)
            return None

    def get_next_signal(self):
        y = None
        while y is None:
            y = self.do_polling()
        return self.key_pairs.get(y)
