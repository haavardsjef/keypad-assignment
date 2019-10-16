"""Rule class"""


class Rule:
    """Rules class"""

    def __init__(self, state1, state2, signal, action):
        self.set_state1(state1)
        self.set_state2(state2)
        self.set_signal(signal)
        self.set_action(action)

    def set_state1(self, state1):
        """ Sets state1 """
        self.state1 = state1

    def set_state2(self, state2):
        """ Sets set_state2 """
        self.state2 = state2

    def set_signal(self, signal):
        """ Sets signal """
        self.signal = signal

    def set_action(self, action):
        """ Sets action """
        self.action = action

    def __str__(self):
        """ Tostring method """
        return "Rule: " + (self.state1) + " => " + str(self.state2) \
        + ", " + str(self.signal) + ", " + str(self.action)
