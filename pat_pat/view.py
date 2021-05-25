import math

import pygame
import pygame.display
from pygame.surface import Surface

from pat_pat.game import Game
from pat_pat.role import ActionType
from pat_pat.user.user_test import TestUser


class GameView:
    def __init__(self, screen: Surface, game: Game):
        self.__screen = screen
        self.__screen_size = self.__screen.get_size()
        self.__game = game
        self.__load_pics_path()
        self.__load_pics()
        self.__load_players_names()

    def __load_players_names(self):
        font = pygame.font.SysFont("simhei", 18)
        roles_names = self.__game.get_players_info()
        self.__players_names = [font.render(name, True, (255, 255, 255)) for name in roles_names]

    def __load_pics(self):
        self.__background_pos = 0
        self.__background = [
            pygame.transform.smoothscale(pygame.image.load(b).convert(), self.__screen_size)
            for b in self.__backgrounds_pics[0]]

        role_num = self.__game.get_players_num()
        self.__role_pos = 0
        self.__role = [pygame.image.load(role).convert_alpha() for role in self.__roles_pics[0]]
        self.__role_g = [pygame.image.load(role[:-4] + "_g.png").convert_alpha() for role in self.__roles_pics[0]]
        role_size_for_num = lambda n: (1 / n - 1 / 3) / 2
        tar_role_h = int(self.__screen_size[1] * (1 / 4 + role_size_for_num(role_num)))
        for pic_id in range(len(self.__role)):
            pic_size = self.__role[pic_id].get_size()
            self.__role[pic_id] = pygame.transform.smoothscale(
                self.__role[pic_id], (int(pic_size[0] / pic_size[1] * tar_role_h), tar_role_h))
            self.__role_g[pic_id] = pygame.transform.smoothscale(
                self.__role_g[pic_id], (int(pic_size[0] / pic_size[1] * tar_role_h), tar_role_h))

        self.__attack_pos = 0
        self.__attack = [pygame.image.load(attack).convert_alpha() for attack in self.__attack_pics[0]]

        self.__defend_pos = 0
        tar_defend_h = int(tar_role_h * (3 / 5))
        self.__defend = [pygame.image.load(defend).convert_alpha() for defend in self.__defend_pics[0]]
        for pic_id in range(len(self.__defend)):
            pic_size = self.__defend[pic_id].get_size()
            self.__defend[pic_id] = pygame.transform.smoothscale(
                self.__defend[pic_id], (int(pic_size[0] / pic_size[1] * tar_defend_h), tar_defend_h))

        self.__make_power_pos = 0
        self.__make_power = [pygame.image.load(mp).convert_alpha() for mp in self.__make_power_pics[0]]

    def __load_pics_path(self):
        pic_p = "../pic/pat_pat/"
        self.__backgrounds_pics = [
            [pic_p + "background/bg11.png"],
            [pic_p + "background/bg01.png"],
            [pic_p + "background/bg21.png"],
            [pic_p + "background/bg31.png"],
            [pic_p + "background/bg41.png"],
            [pic_p + "background/bg51.png"]]
        self.__roles_pics = [
            [pic_p + "role/hero_juntuan.png"],
            [pic_p + "role/hero_nvwang.png"],
            [pic_p + "role/hero_nvzhu.png"],
            [pic_p + "role/hero_one.png"],
            [pic_p + "role/hero_panguan.png"],
            [pic_p + "role/hero_pingmin.png"],
            [pic_p + "role/hero_tanlanzhanshu.png"],
            [pic_p + "role/hero_tianshi.png"],
            [pic_p + "role/teach_hero.png"]]
        self.__attack_pics = [
            [pic_p + "attack/attack1.png"],
            [pic_p + "attack/attack2.png"],
            [pic_p + "attack/attack3.png"],
            [pic_p + "attack/attack4.png"]]
        self.__defend_pics = [
            [pic_p + "defend/d1.png"],
            [pic_p + "defend/d2.png"],
            [pic_p + "defend/d3.png"],
            [pic_p + "defend/d4.png"],
            [pic_p + "defend/d5.png"],
            [pic_p + "defend/d6.png"],
            [pic_p + "defend/d7.png"],
            [pic_p + "defend/d8.png"],
            [pic_p + "defend/d9.png"]]
        self.__make_power_pics = [
            [pic_p + "make_power/p1.png", pic_p + "make_power/p2.png"],
            [pic_p + "make_power/p3.png", pic_p + "make_power/p5.png", pic_p + "make_power/p4.png"]]

    def draw(self):
        self._draw_background()
        roles_pos = self._draw_all_roles()
        self._draw_all_defends(roles_pos)
        self._draw_all_make_powers(roles_pos, 2)

    def _draw_background(self, frequency=1):
        self.__screen.blit(self.__background[self.__background_pos // frequency % len(self.__background)], (0, 0))
        self.__background_pos += 1

    def _draw_all_roles(self, frequency=1):
        roles_num = self.__game.get_players_num()
        is_survivals = self.__game.get_players_survival_state()

        mid_point = (self.__screen_size[0] / 2, self.__screen_size[1] * (3 / 4 - 0.1))
        a = self.__screen_size[0] * (1 / 2 - 0.1)
        b = self.__screen_size[1] * (1 / 4 - 0.08)

        radians_dis = math.pi * 2 / roles_num
        if roles_num == 3:
            roles_rad = [0, -math.pi / 2, math.pi]
        elif roles_num == 5:
            roles_rad = [0, -math.pi / 3, -math.pi / 3 * 2, math.pi, math.pi / 2]
        else:
            roles_rad = [i * radians_dis for i in range(roles_num)]
        roles_point = []
        roles_position = []
        for role_rad in roles_rad:
            # 计算每一个角色的位置中心点
            roles_point.append(
                (self.__ellipse_x(role_rad, a) + mid_point[0], self.__ellipse_y(role_rad, b) + mid_point[1]))
        for role_id in range(roles_num):
            m_p = roles_point[role_id]
            if is_survivals[role_id]:
                _, role_size = self._draw_role(m_p, self.__role, self.__players_names[role_id], frequency)
            else:
                _, role_size = self._draw_role(m_p, self.__role_g, self.__players_names[role_id], frequency)
            roles_position.append((m_p, role_size))
        self.__role_pos += 1
        return roles_position

    def _draw_role(self, mid_pos, role_pics, player_name, frequency=1):
        role_pic = role_pics[self.__role_pos // frequency % len(role_pics)]
        first_pic = role_pics[0]
        self.__screen.blit(role_pic, (mid_pos[0] - role_pic.get_width() / 2, mid_pos[1] - role_pic.get_height() / 2))
        self.__screen.blit(player_name,
                           (mid_pos[0] - player_name.get_width() / 2, mid_pos[1] + first_pic.get_height() / 2))
        return mid_pos, role_pic.get_size()

    def _draw_make_power(self, role_id: int, make_power_pics: list[Surface], roles_position: list, frequency=1):
        role_pos = roles_position[role_id]
        make_power_pic = make_power_pics[self.__make_power_pos // frequency % len(make_power_pics)]
        self.__screen.blit(make_power_pic, (role_pos[0][0] - make_power_pic.get_width() / 2,
                                            role_pos[0][1] + role_pos[1][1] / 2 - make_power_pic.get_height()))

    def _draw_all_make_powers(self, roles_position: list, frequency=1):
        actions = self.__game.get_now_action()
        for player_id in range(len(actions)):
            if actions[player_id] is not None:
                if actions[player_id].action_type.value == ActionType.MAKE_POWER.value:
                    self._draw_make_power(player_id, self.__make_power, roles_position, frequency)
        self.__make_power_pos += 1

    def _draw_attack(self):
        pass

    def _draw_defend(self, role_id: int, defend_pics, roles_position: list, frequency=1):
        role_pos = roles_position[role_id]
        defend_pic = defend_pics[self.__defend_pos // frequency % len(defend_pics)]
        self.__screen.blit(defend_pic,
                           (role_pos[0][0] - defend_pic.get_width() / 2, role_pos[0][1] - defend_pic.get_height() / 2))

    def _draw_all_defends(self, roles_position: list):
        actions = self.__game.get_now_action()
        for player_id in range(len(actions)):
            if actions[player_id] is not None:
                if actions[player_id].action_type.value == ActionType.DEFEND.value:
                    self._draw_defend(player_id, self.__defend, roles_position)
        self.__defend_pos += 1

    @staticmethod
    def __ellipse_x(r, a):
        return a * math.cos(r)

    @staticmethod
    def __ellipse_y(r, b):
        return b * math.sin(r)


class View:
    def __init__(self, game: Game):
        pygame.init()

        self.screen_size = (1200, 700)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("pat pat")
        self.clock = pygame.time.Clock()

        self.game = game
        self.game.run_one_round()

        self.game_view = GameView(self.screen, self.game)

    def run(self):
        while True:
            self.clock.tick(30)
            for user_event in pygame.event.get():
                if user_event.type == pygame.QUIT:
                    return
            self.game_view.draw()
            pygame.display.update()


if __name__ == '__main__':
    view = View(Game(TestUser(), TestUser()))
    view.run()
