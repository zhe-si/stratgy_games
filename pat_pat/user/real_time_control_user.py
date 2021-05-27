import os
import shutil

import pygame
import cv2 as cv
from pygame import Surface

from pat_pat.role import Role, Action, ActionType
from pat_pat.user.interface import UserInterface


class RealTimeCMDControlUser(UserInterface):
    def __init__(self):
        self.__user_name = self._get_user_name_by_cmd()
        self.__role_id = None

    @staticmethod
    def _get_user_name_by_cmd():
        user_name = input("请输入用户名：")
        return user_name

    def decision(self, my_role: Role, enemies_role: list[tuple[str, Role]]) -> Action:
        while True:
            choose = input("user <{}>: "
                           "\n1. choose action"
                           "\n2. check data"
                           "\n\nyour choice: ".format(self.__user_name))
            if choose == "1":
                action_choose = input("user <{}>: "
                                      "\n1. attack"
                                      "\n2. defend"
                                      "\n3. make power"
                                      "\n\nyour action and power (such as '1 3' to choose attack with 3 power): "
                                      .format(self.__user_name))
                action_choose = action_choose.split()
                if len(action_choose) == 2 and action_choose[0].isdigit() and action_choose[1].isdigit():
                    if action_choose[0] == "1":
                        print("you attack with power {}".format(action_choose[1]))
                        return Action(ActionType.ATTACK, int(action_choose[1]))
                    elif action_choose[0] == "2":
                        print("you defend with power {}".format(action_choose[1]))
                        return Action(ActionType.DEFEND, int(action_choose[1]))
                    elif action_choose[0] == "3":
                        print("you make one power")
                        return Action(ActionType.MAKE_POWER, 1)
                    else:
                        print("please choose in range")
                        continue
                elif len(action_choose) == 1 and action_choose[0].isdigit():
                    if action_choose[0] == "3":
                        print("you make one power")
                        return Action(ActionType.MAKE_POWER, 1)
                    else:
                        print("please choose in right format")
                        continue
                else:
                    print("please choose in right format")
                    continue
            elif choose == "2":
                self._show_role_info("your", my_role)
                for name, role in enemies_role:
                    self._show_role_info(name, role)
                continue
            else:
                print("please choose in range")
                continue
        return Action(ActionType.MAKE_POWER, 1)

    @staticmethod
    def _show_role_info(name, role: Role):
        print("info > {} power: {}".format(name, role.power))
        print("info > {} actions: {}".format(name, role.history))
        print("info > {} blood: {}".format(name, role.blood))
        print()

    def get_user_name(self) -> str:
        return self.__user_name

    def get_role_id(self, roles_pics: list[list[Surface]]) -> int:
        if self.__role_id is None:
            cash_path = os.path.join(".", ".cash", "roles_pic")
            if not os.path.exists(cash_path):
                os.makedirs(cash_path)
            for role_id, role_pics in enumerate(roles_pics):
                pygame.image.save(role_pics[0], os.path.join(cash_path, str(role_id) + ".png"))

            print("user {}: please choose role".format(self.__user_name))
            print("usage > click key l to last role picture, r to next role picture, enter to choose")
            im_id = 0
            while True:
                im = cv.imread(os.path.join(cash_path, str(im_id) + ".png"))
                cv.imshow(str(im_id), im)
                while True:
                    key = cv.waitKey(0)
                    if key == ord('l'):
                        im_id = (im_id - 1) % len(roles_pics)
                        break
                    elif key == ord('r'):
                        im_id = (im_id + 1) % len(roles_pics)
                        break
                    elif key == ord('\r'):
                        self.__role_id = im_id
                        cv.destroyAllWindows()
                        shutil.rmtree(cash_path)
                        return self.__role_id
                cv.destroyAllWindows()
        else:
            return self.__role_id


def main():
    # print(RealTimeCMDControlUser.get_user_name_by_cmd())
    pass


if __name__ == '__main__':
    main()
