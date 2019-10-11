"""LED-classes"""
import time
import RPi.GPIO as GPIO


class LEDboard:
    """interface to the physical, Charlieplexed LED board"""

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.ledInterface = LedInterface(Pin(13), Pin(19), Pin(26))

    def light_led(self, led, duration):
        """Turn on one of the 6 LEDs by making the appropriate combination of input and
        output declarations, and then making the appropriate HIGH / LOW settings on the output
        pins."""
        self.ledInterface.loop([int(led)], duration)

    def flash_all_leds(self, wait_time):
        """Flash all 6 LEDs on and off for k seconds, where k is an argument of the
        method."""
        self.ledInterface.loop([1, 2, 3, 4, 5, 6], wait_time)

    def twinkle_all_leds(self):
        """Turn all LEDs on and off in sequence for k seconds, where k is an argument
        of the method."""
        leds = [1, 2, 3, 4, 5, 6]
        while leds:
            self.ledInterface.loop(leds, 2)
            leds.pop()

    def power_on(self):
        """Light signalizing power on"""
        self.ledInterface.loop([1, 2, 3], 4)
        self.ledInterface.loop([1, 2], 2)
        self.ledInterface.loop([1], 2)

    def power_off(self):
        """Light signalizing power off"""
        self.ledInterface.loop([1, 2], 2)
        self.ledInterface.loop([1], 2)

    def logged_in(self):
        """Signalizing correct login"""
        self.ledInterface.loop([1, 2], 1)
        self.ledInterface.loop([3, 4], 1)
        self.ledInterface.loop([5, 6], 1)
        self.ledInterface.loop([1, 2, 3, 4, 5, 6, ], 2)




class Pin:
    def __init__(self, pin):
        self.pin = pin

        self.off()

    def low(self):
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def high(self):
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.setup(self.pin, GPIO.IN)


class LedInterface:
    def __init__(self, pin_A, pin_B, pin_C):
        self.pinA = pin_A
        self.pinB = pin_B
        self.pinC = pin_C

    def off(self):
        self.pinA.off()
        self.pinB.off()
        self.pinC.off()

    def led1(self):
        self.pinA.low()
        self.pinB.high()
        self.pinC.off()

    def led2(self):
        self.pinA.low()
        self.pinB.off()
        self.pinC.high()

    def led3(self):
        self.pinA.high()
        self.pinB.off()
        self.pinC.low()

    def led4(self):
        self.pinA.high()
        self.pinB.low()
        self.pinC.off()

    def led5(self):
        self.pinA.off()
        self.pinB.low()
        self.pinC.high()

    def led6(self):
        self.pinA.off()
        self.pinB.high()
        self.pinC.low()

    def loop(self, leds, wait_time):
        timeout = time.time() + float(wait_time)
        while True:
            if time.time() > timeout:
                break
            if 1 in leds:
                self.led1()
            if 2 in leds:
                self.led2()
            if 3 in leds:
                self.led3()
            if 4 in leds:
                self.led4()
            if 5 in leds:
                self.led5()
            if 6 in leds:
                self.led6()
        self.off()
