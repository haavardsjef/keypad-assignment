"""Finite state machine"""
from inspect import isfunction
from kpc import Kpc
from rule import Rule
from keypad import KeyPad
# Functions
def signal_is_digit(signal):
    """ Checks to see whether the signal is a digit. """
    return 48 <= ord(signal) <= 57

def signal_is_led(signal):
    """ Checks to see whether the signal is a valid led #. """
    return signal in "123456"


def all_symbols(signal):
    """ Checks to see whether the signal is a symbol. """
    return signal in "*#0123456789N"


# Classes
class Fsm:
    """Finite state machine"""

    def __init__(self):
        # Initialize agent, keypad and LED board
        self.agent = Kpc()
        self.keypad = KeyPad()

        # Create all rule objects for the FSM - and insure they are listed in the desired order.
        self.rules = []
        actions = {"A0": self.agent.init_passcode_entry,
                   "A2": self.agent.append_next_digit,
                   "A3": self.agent.verify_login,
                   "A6": self.agent.reset_agent,
                   "A7": self.agent.cache_password,
                   "A8": self.agent.validate_passcode_change,
                   "A9": self.agent.cache_led,
                   "A10": self.agent.nothing,
                   "A11": self.agent.append_next_seconds_digit,
                   "A12": self.agent.light_one_led,
                   "A13": self.agent.exit_action}

                 # RULES LOG IN
        rules = [Rule("S-INIT", "S-READ", all_symbols, actions["A0"]),
                 Rule("S-READ", "S-READ", signal_is_digit, actions["A2"]),
                 Rule("S-READ", "S-VERIFY", "*", actions["A3"]),
                 Rule("S-READ", "S-INIT", all_symbols, actions["A10"]),
                 Rule("S-VERIFY", "S-ACTIVE", "Y", actions["A10"]),
                 Rule("S-VERIFY", "S-INIT", all_symbols, actions["A10"]),
                 # RULES CHANGE PASSWORD
                 Rule("S-ACTIVE", "S-READ-2", "*", actions["A6"]),
                 Rule("S-READ-2", "S-READ-2", signal_is_digit, actions["A2"]),
                 Rule("S-READ-2", "S-READ-3", "*", actions["A7"]),
                 Rule("S-READ-2", "S-ACTIVE", all_symbols, actions["A6"]),
                 Rule("S-READ-3", "S-READ-3", signal_is_digit, actions["A2"]),
                 Rule("S-READ-3", "S-ACTIVE", "*", actions["A8"]),
                 Rule("S-READ-3", "S-ACTIVE", all_symbols, actions["A6"]),
                 # LED RULES
                 Rule("S-ACTIVE", "S-LED", signal_is_led, actions["A9"]),
                 Rule("S-LED", "S-TIME", "*", actions["A10"]),
                 Rule("S-LED", "S-ACTIVE", all_symbols, actions["A6"]),
                 Rule("S-TIME", "S-TIME", signal_is_digit, actions["A11"]),
                 Rule("S-TIME", "S-ACTIVE", "*", actions["A12"]),
                 Rule("S-TIME", "S-ACTIVE", all_symbols, actions["A6"]),
                 # LOG OUT
                 Rule("S-ACTIVE", "S-INIT", "#", actions["A13"])]

        self.add_rule(*rules)
        self.state = "S-INIT"
        self.signal = None

    def add_rule(self, *rules):
        """add rule - add a new rule to the end of the FSM’s rule list."""
        for rule in rules:
            self.rules.append(rule)

    def get_next_signal(self):
        """ get next signal - query the agent for the next signal. """
        return self.agent.get_next_signal()

    def run_rules(self, debug=False):
        """ run rules - go through the rule set, in order, applying each
        rule until one of the rules is fired. """
        ran = False
        index = 0
        for rule in self.rules:
            index += 1
            if self.apply_rule(rule):
                self.fire_rule(rule)
                if debug:
                    print("Ran rule " + str(index) + ": " + str(rule))
                ran = True
                break
        if not ran and debug:
            print("No rules matched!")

    def apply_rule(self, rule):
        """apply rule - check whether the conditions of a rule are met."""
        matches = False
        if isfunction(rule.signal) and rule.signal(self.signal) and self.state == rule.state1:
            matches = True
        elif self.signal == rule.signal and self.state == rule.state1:
            matches = True
        return matches

    def fire_rule(self, rule):
        """ fire rule - use the consequent of a rule to
            a) set the next state of the FSM, and
            b) call the appropriate agent action method. """
        # a)
        self.state = rule.state2

        # b)
        rule.action(self.signal) # Calls the action with same name as signal

    def __str__(self):
        """ Tostring method"""
        temp_string = ""
        for rule in self.rules:
            temp_string += str(rule)
            temp_string += "\n"
        temp_string += "-----"
        temp_string += "\nState: " + str(self.state)
        temp_string += "\nSignal: " + str(self.signal)
        return temp_string


    def main_loop(self):
        """ main loop - begin in the FSM’s default initial state and then
        repeatedly call get next signal  and run rules until the FSM enters
        its default final state. """

        while self.state != "S-LOGOUT":
            self.signal = self.get_next_signal()
            self.run_rules(True)


if __name__ == "__main__":
    FSM = Fsm()
    FSM.main_loop()
