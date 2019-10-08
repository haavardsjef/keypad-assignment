"""Setting up GPIO"""
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.out)
GPIO.setup(23, GPIO.out)
GPIO.setup(24, GPIO.out)
GPIO.setup(25, GPIO.out)

GPIO.setup(17, GPIO.IN, pull up down=GPIO.PUD DOWN)
GPIO.setup(27, GPIO.IN, pull up down=GPIO.PUD DOWN)
GPIO.setup(22, GPIO.IN, pull up down=GPIO.PUD DOWN)

def check_pressed():
    for item in [18,23,24,25]:
        GPIO.output(item, GPIO.HIGH)
        for item in [17, 22, 27]:
            for i in range(20):
                time.sleep(10)
                if GPIO.input(item) == GPIO.HIGH:
                        #Do something
        GPIO.output(item, GPIO.LOW)
