"""KPC class"""

from .keypad import Keypad
from .ledboard import LEDboard


def signal_is_digit(signal):
    return 48 <= ord(signal) <= 57


class KPC:
    """The keypad controller agent that coordinates activity between the other 3 classes along
    with veryifying and changing passwords."""

    def __init__(self):
        self.keypad = Keypad()
        self.LED = LEDboard()
        self.pw_file = "password.txt"
        self.CP = self.get_password_from_file()  # kan man kjøre denne her før init er ferdig?
        self.CUMP = ""
        self.CUMP_OLD = ""
        self.override_signal = None
        self.seconds = ""
        self.LED_nr = ""

    def get_password_from_file(self):
        """REad password from file"""
        file = open(self.pw_file, "r")
        cp = file.readline()
        file.close()
        return cp

    def save_password(self, symbol):
        """Save new password in file"""
        if self.validate_passcode_change() and self.CUMP == self.CUMP_OLD:
            file = open(self.pw_file, 'w')
            file.write(self.CUMP)
            file.close()
            return True

        return False

    def init_passcode_entry(self):
        """Clear the passcode - buffer and initiate a ”power up” lighting sequence on the LED Board.
        This should be done when the user first presses the keypad"""
        self.reset_CUMP()
        self.LED.power_on()

    def get_next_signal(self):
        """Return the override - signal, if it is non-blank; otherwise query the keypad for the next pressed key"""
        if self.override_signal is not None:
            return self.override_signal
        else:
            self.keypad.get_next_signal()

    def verify_login(self, symbol):
        """Check that the password just entered via the keypad matches that in the password file.Store the result(Y
        or N) in the override - signal.Also, this should call the LED Board to initiate the appropriate lighting
        pattern for login success or failure. """
        if self.CUMP == self.CP:
            self.override_signal = "Y"
            self.LED.logged_in()
        else:
            self.override_signal = "N"
            self.LED.flash_all_leds(0.5)

    def validate_passcode_change(self):
        """Check that the new password is legal. If so, write the new password in the password file.A legal password
        should be at least 4 digits long and should contain no symbols other than the digits 0 - 9. As in verify
        login, this should use the LED-Board to signal success or failure in changing the password. Returns False if
        password is not valid. """
        if len(self.CUMP) > 3:
            for symbol in self.CUMP:
                if not signal_is_digit(symbol):
                    self.LED.flash_all_leds(0.5)
                    return False
            self.LED.logged_in()
            return True
        self.LED.flash_all_leds(0.5)
        return False

    def light_one_led(self):
        """Using values stored in the LED_nr and "seconds" slots, call the LED Board and request that LED  # LED_nr be
        turned on for "seconds" seconds. """
        self.LED.light_led(self.LED_nr, self.seconds)

    def flash_leds(self):
        """Call the LED-Board and request the flashing of all LEDs."""
        self.LED.flash_all_leds()

    def twinkle_leds(self):
        """Call the LED Board and request the twinkling of all LEDs."""
        self.LED.twinkle_all_leds()

    def reset_CUMP(self, symbol):
        """Resets CUMP"""
        self.CUMP = ""

    def append_next_digit(self, digit):
        """Add next digit to CUMP"""
        self.CUMP += digit

    def reset_agent(self, symbol):
        """Reset CUMP and CUMP_OLD"""
        self.override_signal = None
        self.reset_CUMP()
        self.reset_seconds()
        self.CUMP_OLD = ""

    def reset_seconds(self):
        """Resetting seconds"""
        self.seconds = ""

    def append_next_seconds_digit(self, symbol):
        """Register a time interval"""
        self.seconds += symbol

    def cache_password(self, symbol):
        """Set CUMP_OLD to CUMP, and reset CUMP"""
        self.CUMP_OLD = self.CUMP
        self.reset_CUMP()

    def cache_LED_nr(self, symbol):
        """Saves LED number"""
        self.LED_nr = symbol

    def blink_LEDs(self, symbol):
        """Turn on LED-nr in self.seconds seconds"""
        self.LED.turn_on_led(self.LED_nr, self.seconds)
        self.reset_agent()

    def shutdown(self):
        """Turn off the LEDs"""
        self.LED.power_off()

    def power_up(self, symbol):
        """Turn on LED"""
        self.LED.power_on()

    def nothing(self, symbol):
        """No action"""

    def log_out(self, symbol):
        """Log out"""
        self.shutdown()
