import random

from pygame import Surface

from pat_pat.role import Role, Action, ActionType
from pat_pat.user.interface import UserInterface
from pat_pat.user.remote_user import SendUserProxy, ReceiveUserProxy


class TestUser(UserInterface):
    user_id = 0

    def __init__(self):
        self.id = TestUser.user_id
        self.game_time = 0
        self.now_power = 0
        TestUser.user_id += 1

    def decision(self, my_role: Role, enemies_role: list[tuple[str, Role]]) -> Action:
        self.game_time += 1
        if self.game_time == 1:
            return Action(ActionType.MAKE_POWER, 1)

        choose = random.randint(0, 5)
        if choose == 0:
            if self.now_power == 0:
                self.now_power += 1
                return Action(ActionType.MAKE_POWER, 1)
            else:
                power = random.randint(1, self.now_power)
                self.now_power -= power
                return Action(ActionType.ATTACK, power)
        elif choose == 1:
            return Action(ActionType.DEFEND, 0)
        else:
            self.now_power += 1
            return Action(ActionType.MAKE_POWER, 1)

    def get_user_name(self) -> str:
        return "TestUser {}".format(self.id)

    def get_role_id(self, roles_pics: list[list[Surface]]) -> int:
        return self.id % len(roles_pics)


if __name__ == '__main__':
    s_p = SendUserProxy(TestUser(), "localhost", ReceiveUserProxy.BIND_PORT)
    s_p.run()
