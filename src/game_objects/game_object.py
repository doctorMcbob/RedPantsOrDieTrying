from src.lib import utils

class GameObject(object):
    def __init__(self, state_template):
        self.state = state_template.copy()

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state

        return self.get_state()

    def print_state(self):
        utils.print_state(self.get_state())
