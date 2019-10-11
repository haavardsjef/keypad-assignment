"""Rule class"""


class Rule:
    """Rules are made here"""

    def __init__(self, state1, state2, signal, action):
        self.state_1 = state1  # triggering state
        self.state_2 = state2  # new state om rule "fires"
        self.signal = signal  # triggering signal
        self.action = action
