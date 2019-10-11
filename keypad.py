"""Keypad-class"""
import time
import RPi.GPIO as GPIO


class Keypad:
    """Interface to the physical keypad"""

    def __init__(self):
        self.keys = [["1", "2", "3"],
                     ["4", "5", "6"],
                     ["7", "8", "9"],
                     ["*", "0", "#"]]

        self.row_pins = [18, 23, 24, 25]
        self.col_pins = [17, 27, 22]

    def setup(self):
        """Set the proper mode via: GPIO.setmode(GPIO.BCM). Also, use GPIO functions to
        set the row pins as outputs and the column pins as inputs."""
        GPIO.setmode(GPIO.BCM)
        for pin in self.row_pins:
            GPIO.setup(pin, GPIO.OUT)

        for pin in self.col_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def do_polling(self):
        """Use nested loops (discussed above) to determine the key currently being pressed
        on the keypad."""
        for i in range(len(self.row_pins)):
            row_pin = self.row_pins[i]
            GPIO.output(row_pin, GPIO.HIGH)
            for j in range(len(self.col_pins)):
                col_pin = self.col_pins[j]
                counter = 0
                while GPIO.input(col_pin) == GPIO.HIGH:
                    time.sleep(0.01)
                    counter += 1
                    if counter >= 20:
                        return self.keys[i][j]
            GPIO.output(row_pin, GPIO.LOW)
        return None

    def get_next_signal(self):
        """This is the main interface between the agent and the keypad. It should
        initiate repeated calls to do polling until a key press is detected."""
        k_pad = Keypad()
        number = None
        while number is None:
            number = k_pad.do_polling()

        return number
