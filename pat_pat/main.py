from pat_pat.game import Game
from pat_pat.user.test_user import TestUser
from pat_pat.user.real_time_control_user import RealTimeCMDControlUser
from pat_pat.view import View


def main():
    # game = Game(TestUser(), TestUser(), TestUser(), TestUser(), TestUser())
    game = Game(TestUser(), RealTimeCMDControlUser())
    view = View(game)
    while True:
        game.run_one_round()
        if not view.run_one_round():
            break
        if game.is_game_finished():
            break


if __name__ == '__main__':
    main()
