from action import Action

class Item:

    def __init__(self, placeholder):
        self.placeholder = placeholder
        self.action = Action.NONE

    def intoEnvironment(self, env):
        self.environment = env

    