from exception import LogicException
from pat_pat.user.interface import UserInterface
from role import Role, ActionType


class Game:
    def __init__(self, user1: UserInterface, user2: UserInterface, *users):
        self.__players = [(Role(), user1), (Role(), user2)]
        for user in users:
            self.__players.append((Role(), user))
        self.__now_players_action = []
        self.__are_players_survival = [True for _ in range(len(self.__players))]
        self.__winner_info = None

    def run_one_round(self):
        has_attack, max_attack_power = self.__run_all_decisions()
        self.__judge_actions_result(has_attack, max_attack_power)

    def get_players_num(self):
        return len(self.__players)

    def get_players_info(self):
        return [player[1].get_user_name() for player in self.__players]

    def get_now_action(self):
        """action 若为None，表明该玩家以阵亡"""
        return self.__now_players_action.copy()

    def get_players_survival_state(self):
        return self.__are_players_survival.copy()

    def is_game_finished(self):
        if self.__winner_info is None:
            return False
        else:
            return True

    def get_winner_info(self):
        return self.__winner_info

    def __judge_actions_result(self, has_attack, max_attack_power):
        if len(self.__now_players_action) == 0:
            raise LogicException("didn't get this round's players actions, action list is empty")
        for player_id in range(len(self.__now_players_action)):
            action = self.__now_players_action[player_id]
            if action is None:
                continue
            if action.action_type.value == ActionType.MAKE_POWER.value:
                self._rule_make_power(action, player_id)
                if has_attack:
                    self._rule_be_attacked(action.power, max_attack_power, player_id)
            elif action.action_type.value == ActionType.ATTACK.value:
                self._rule_use_power(action.power, player_id)
                if has_attack:
                    self._rule_attack_crash(action.power, max_attack_power, player_id)
            elif action.action_type.value == ActionType.DEFEND.value:
                self._rule_use_power(action.power, player_id)
                if has_attack:
                    self._rule_defend_attack(action.power, max_attack_power, player_id)
            else:
                raise Exception("action type {} is unknown".format(action.action_type))
        survival_num = len(self.__players)
        first_survival_id = None
        for player_id in range(len(self.__players)):
            if not self.__players[player_id][0].is_survival():
                self.__are_players_survival[player_id] = False
            if not self.__are_players_survival[player_id]:
                survival_num -= 1
            elif first_survival_id is None:
                first_survival_id = player_id
        if survival_num == 1:
            self.__winner_info = (first_survival_id, self.__players[first_survival_id][1].get_user_name())
        elif survival_num < 1:
            raise LogicException("survival players num is less than 1")

    def __run_all_decisions(self):
        has_attack = False
        max_attack_power = -1
        self.__now_players_action.clear()

        for player_id in range(len(self.__players)):
            if not self.__are_players_survival[player_id]:
                self.__now_players_action.append(None)
                continue
            role, user = self.__players[player_id]
            action = user.decision(role.copy(), [player[0].copy() for player in self.__players if player[0] != role])
            print("player {}: action {}, power {}".format(user.get_user_name(), action.action_type, action.power))
            self.__now_players_action.append(action)

            if action.action_type.value == ActionType.ATTACK.value:
                has_attack = True
                if action.power > max_attack_power:
                    max_attack_power = action.power
        return has_attack, max_attack_power

    def _rule_defend_attack(self, this_defend_power, max_attack_power, player_id):
        if max_attack_power > self._rule_defend_attack_power(this_defend_power):
            self.__players[player_id][0].be_attacked()

    @staticmethod
    def _rule_defend_attack_power(defend_power):
        return (defend_power + 1) * 3

    def _rule_attack_crash(self, this_attack_power, max_attack_power, player_id):
        if this_attack_power < max_attack_power:
            self.__players[player_id][0].be_attacked()

    def _rule_use_power(self, use_power, player_id):
        if not self.__players[player_id][0].use_power(use_power):
            self.__players[player_id][0].be_attacked()

    def _rule_be_attacked(self, make_power_num, max_attack_power, player_id):
        self.__players[player_id][0].be_attacked()

    def _rule_make_power(self, action, player_id):
        action.power = 1
        self.__players[player_id][0].add_power(action.power)
