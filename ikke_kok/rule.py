"""Rule class"""


class Rule:
    """Rules are made here"""

    def __init__(self, state1, state2, signal, action):
        self.set_state_1(state1)
        self.set_state_2(state2)
        self.set_signal(signal)
        self.set_action(action)

    def set_state_1(self, state_1):
        self.state_1 = state_1

    def set_state_2(self, state_2):
        self.state_2 = state_2

    def set_signal(self, signal):
        self.signal = signal

    def set_action(self, action):
        self.action = action
