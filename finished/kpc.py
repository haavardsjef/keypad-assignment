"""KPC Agent"""
from keypad import KeyPad
from led_board import LedBoard


class Kpc:
    """KPC Agent"""

    def __init__(self):
        self.keypad = KeyPad()
        self.led_board = LedBoard()
        self.passcode_buffer = "" # Ongoing password entry attempt
        self.old_passcode_buffer = None
        self.passcode_path = "passcode.txt"
        self.override_signal = None
        self.led_id = None
        self.led_duration = ""



    # Required methods
    def init_passcode_entry(self, signal):
        """  init passcode entry - Clear the passcode-buffer and initiate a ”power up”
        lighting sequence on the LED Board.
        This should be done when the user first presses the keypad. """
        self.passcode_buffer = ""
        self.led_board.power_up()

    def get_next_signal(self):
        """ get next signal - Return the override-signal,
        if it is non-blank; otherwise query the keypad
        for the next pressed key """
        if self.override_signal is not None:
            temp_signal = self.override_signal
            self.override_signal = None
            return temp_signal
        return self.keypad.get_next_signal()

    def verify_login(self, signal):
        """ verify login - Check that the password just entered via the keypad matches that
        in the password file. Store the result (Y or N) in the override-signal.
        Also, this should call the LED
        Board to initiate the appropriate lighting pattern for login success or failure."""
        file = open(self.passcode_path, "r")
        password = file.read()
        file.close()
        if password == self.passcode_buffer:
            self.override_signal = "Y"
            self.led_board.success()
        else:
            self.override_signal = "N"
            self.led_board.failure()
        self.passcode_buffer = ""

    def validate_passcode_change(self, signal):
        """ validate passcode change - Check that the new password is legal.
        If so, write the new password in the password file. A legal password should be at least
        4 digits long and should contain no symbols other than the digits 0-9. As in verify login,
        this should use the LED Board to signal success or failure in changing the password. """
        if self.passcode_buffer == self.old_passcode_buffer and len(self.passcode_buffer) >= 4:
            self.led_board.success()
            file = open(self.passcode_path, "w")
            file.write(self.passcode_buffer)
            file.close()
        else:
            self.led_board.failure()


    def light_one_led(self, signal):
        """ light one led - Using values stored in the Lid and Ldur slots,
        call the LED Board and request
        that LED number Lid be turned on for Ldur seconds """
        self.led_board.light_led(int(self.led_id), int(self.led_duration))
        self.led_duration = ""

    def flash_leds(self, signal):
        """ flash leds - Call the LED Board and request the flashing of all LEDs. """
        self.led_board.flash_all_leds(self.led_duration)

    def twinkle_leds(self, signal):
        """ Call the LED Board and request the twinkling of all LEDs."""
        self.led_board.twinkle_all_leds()

    def exit_action(self, signal):
        """ Call the LED Board to initiate the ”power down” lighting sequence."""
        self.led_board.power_down()

    def append_next_digit(self, signal):
        """ Append next digit to passcode buffer"""
        self.passcode_buffer += (signal)

    def reset_agent(self, signal):
        """ Reset the agents cache"""
        self.passcode_buffer = ""
        self.led_duration = ""

    def cache_password(self, signal):
        """Set old_passcode_buffer to passcode_buffer, and reset passcode_buffer"""
        self.old_passcode_buffer = self.passcode_buffer
        self.passcode_buffer = ""

    def cache_led(self, led_id):
        """Saves LED number"""
        self.led_id = led_id

    def nothing(self, signal):
        """No action"""

    def append_next_seconds_digit(self, digit):
        """Register a time interval"""
        self.led_duration += digit
