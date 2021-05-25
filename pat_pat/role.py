from enum import Enum, auto


class ActionType(Enum):
    MAKE_POWER = auto()
    ATTACK = auto()
    DEFEND = auto()


class Action:
    def __init__(self, action_type: ActionType, power: int):
        self.power = power
        self.action_type = action_type


class Role:
    def __init__(self, blood=1, power=0):
        self.blood = blood
        self.power = power
        self.history = []

    def copy(self):
        role_info = Role(self.blood, self.power)
        role_info.history = self.history.copy()
        return role_info

    def add_history(self, action: Action):
        self.history.append(action)

    def be_attacked(self, power=1):
        self.blood -= power

    def is_survival(self):
        """角色是否存活"""
        return self.blood > 0

    def add_power(self, power=1):
        self.power += power

    def use_power(self, power):
        if self.power >= power:
            self.power -= power
            return True
        else:
            return False
