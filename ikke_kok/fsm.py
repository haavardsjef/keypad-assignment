
class fsm:
    """Finite state machine"""

    def __init__(self):
        self.rules = []


    def add_rule(self, rule):
        """add rule - add a new rule to the end of the FSM’s rule list."""
        self.rules.append(rule)

    def get_next_signal(self):
        """ get next signal - query the agent for the next signal. """

    def run_rules(self):
        """ run rules - go through the rule set, in order, applying each rule until one of the rules is fired. """

    def apply_rule(self):
        """apply rule - check whether the conditions of a rule are met."""

    def fire_rule(self):
        """ fire rule - use the consequent of a rule to a) set the next state of the FSM, and b) call the
        appropriate agent action method. """

    def main_loop(self):
        """ main loop - begin in the FSM’s default initial state and then repeatedly call get next signal
        and run rules until the FSM enters its default final state. """
