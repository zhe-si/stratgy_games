from pat_pat.game import Game
from pat_pat.user.user_test import TestUser
from pat_pat.view import View


def main():
    game = Game(TestUser(), TestUser(), TestUser(), TestUser())
    view = View(game)
    while True:
        game.run_one_round()
        if not view.run_one_round():
            break
        if game.is_game_finished():
            break


if __name__ == '__main__':
    main()
