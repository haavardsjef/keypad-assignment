"""" LedBoard class"""

class LedBoard:
    """ LedBoard class"""

    def setup(self):
        """ setup - Set the proper mode via: GPIO.setmode(GPIO.BCM) """

    def light_led(self, led, k):
        """ light led - Turn on one of the 6 LEDs by making the appropriate combination of input and
        output declarations, and then making the appropriate HIGH / LOW settings on the output
        pins. """
        print("Lighting led #", led, "for", k, "seconds.")

    def flash_all_leds(self, k):
        """ flash all leds - Flash all 6 LEDs on and off for k seconds, where k is an argument of the
        method."""

    def twinkle_all_leds(self, k):
        """ twinkle all leds - Turn all LEDs on and off in sequence for k seconds, where k is an argument
        of the method. """

    def power_up(self):
        print("Powering up!")

    def power_down(self):
        print("Powering down!")
        pass

    def success(self):
        """ SUCCESS LIGHT DISPLAY """
        print("----- SUCCESSFULLY LOGGED IN -----")
        pass

    def failure(self):
        """ FAIL LIGHT DISPLAY """
        print("----- FAILED TO LOG IN -----")
        pass
