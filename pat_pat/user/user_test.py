import random

from pat_pat.role import Role, Action, ActionType
from pat_pat.user.interface import UserInterface


class TestUser(UserInterface):
    user_id = 0

    def __init__(self):
        self.id = TestUser.user_id
        self.game_time = 0
        TestUser.user_id += 1

    def decision(self, my_role: Role, enemies_role: list[Role]) -> Action:
        self.game_time += 1
        if self.game_time == 1:
            return Action(ActionType.MAKE_POWER, 1)

        choose = random.randint(0, 5)
        if choose == 0:
            return Action(ActionType.ATTACK, 1)
        elif choose == 1:
            return Action(ActionType.DEFEND, 0)
        else:
            return Action(ActionType.MAKE_POWER, 1)

    def get_user_name(self) -> str:
        return "test user {}".format(self.id)
