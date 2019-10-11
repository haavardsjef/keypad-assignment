"""FSM-class"""

from rule import Rule
from kpc import KPC


class FSM:
    """Finite State Machine"""
    all = "#*0123456789N"

    def __init__(self):
        self.agent = KPC()
        self.rules = []
        self.state = "S-INIT"
        self.curr_sig = ""
        self.action = {"A0": self.agent.power_up,
                       "A1": self.agent.reset_CUMP,
                       "A2": self.agent.append_next_digit,
                       "A3": self.agent.verify_login,
                       "A4": self.agent.reset_agent,
                       "A6": self.agent.reset_agent,
                       "A7": self.agent.cache_password,
                       "A8": self.agent.save_password,
                       "A9": self.agent.cache_LED_nr,
                       "A10": self.agent.nothing,
                       "A11": self.agent.append_next_seconds_digit,
                       "A12": self.agent.blink_LEDs,
                       "A13": self.agent.log_out
                       }
        # RULES LOG IN
        rule_1 = Rule("S-INIT", "S-READ", FSM.all, self.action["A0"])
        rule_2 = Rule("S-READ", "S-READ", "0123456789", self.action["A2"])
        rule_3 = Rule("S-READ", "S-VERIFY", "*", self.action["A3"])
        rule_4 = Rule("S-READ", "S-INIT", FSM.all, self.action["A4"])
        rule_5 = Rule("S-VERIFY", "S-ACTIVE", "Y", self.action["A10"])  # ???
        rule_6 = Rule("S-VERIFY", "S-INIT", FSM.all, self.action["A4"])
        # RULES CHANGE PASSWORD
        rule_7 = Rule("S-ACTIVE", "S-READ-2", "*", self.action["A1"])
        rule_8 = Rule("S-READ-2", "S-READ-2", "0123456789", self.action["A2"])
        rule_9 = Rule("S-READ-2", "S-READ-3", "*", self.action["A7"])
        rule_10 = Rule("S-READ-2", "S-ACTIVE", FSM.all, self.action["A6"])
        rule_11 = Rule("S-READ-3", "S-READ-3", "0123456789", self.action["A2"])
        rule_12 = Rule("S-READ-3", "S-ACTIVE", "*", self.action["A8"])
        rule_13 = Rule("S-READ-3", "S-ACTIVE", FSM.all, self.action["A6"])
        # LED RULES
        rule_14 = Rule("S-ACTIVE", "S-LED", "012345", self.action["A9"])
        rule_15 = Rule("S-LED", "S-TIME", "*", self.action["A10"])
        rule_16 = Rule("S-LED", "S-ACTIVE", FSM.all, self.action["A4"])
        rule_17 = Rule("S-TIME", "S-TIME", "0123456789", self.action["A11"])
        rule_18 = Rule("S-TIME", "S-ACTIVE", "*", self.action["A12"])
        rule_19 = Rule("S-TIME", "S-ACTIVE", FSM.all, self.action["A6"])
        #LOG OUT
        rule_20 = Rule("S-ACTIVE", "S-LOGOUT", "#", self.action["A13"])

        self.add_rule(
            rule_1,
            rule_2,
            rule_3,
            rule_4,
            rule_5,
            rule_6,
            rule_7,
            rule_8,
            rule_9,
            rule_10,
            rule_11,
            rule_12,
            rule_13,
            rule_14,
            rule_15,
            rule_16,
            rule_17,
            rule_18,
            rule_19,
            rule_20)

    def add_rule(self, *rules):
        """ add a new rule to the end of the FSM’s rule list."""
        for rule in rules:
            self.rules.append(rule)

    def get_next_signal(self):
        """query the agent for the next signal."""
        return self.agent.get_next_signal()

    def run_rules(self):
        """go through the rule set, in order, applying each rule until one of the rules is fired."""
        for rule in self.rules:
            if self.apply_rule(rule):
                self.fire_rule(rule)
                break

    def apply_rule(self, rule):
        """check whether the conditions of a rule are met."""
        if rule.state_1 == self.state and self.curr_sig == rule.signal:
            return True

    def fire_rule(self, rule):
        """use the consequent of a rule to a) set the next state of the FSM, and b) call the
        appropriate agent action method."""
        self.state = rule.state_2
        rule.action(self.curr_sig)

    def main_loop(self):
        """begin in the FSM’s default initial state and then repeatedly call get next signal
        and run rules until the FSM enters its default final state"""
        while self.state != "S_LOGOUT":
            self.curr_sig = self.get_next_signal()
            self.run_rules()
