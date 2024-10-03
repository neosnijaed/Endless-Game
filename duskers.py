"""Depending on Player's decision the game has different responses."""
from game_class import Game
import argparse


def get_args():
    """Check and evaluate arguments parsed and return them.

    Return Values:
    Tuple of String: random seed, Integer: minimum duration of animation, Integer: maximum duration of animation,
    String: names of locations seperated by comma.
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('clargs', nargs='*')
    args = arg_parser.parse_args()
    seed = args.clargs[0] if len(args.clargs) == 4 else 'None'
    ani_min_dur = int(args.clargs[1]) if len(args.clargs) == 4 else 'None'
    ani_max_dur = int(args.clargs[2]) if len(args.clargs) == 4 else 'None'
    if len(args.clargs) == 4 and all(not char.isdigit() for char in args.clargs[3]):
        loc_names = args.clargs[3]
    else:
        loc_names = 'Nuclear_power_plant_wreckage,Old_beach_bar'
    return seed, ani_min_dur, ani_max_dur, loc_names


def main() -> None:
    """Main function and control sequence of the Game."""
    args = get_args()
    game = Game(args[0], args[1], args[2], args[3])
    game.set_file()
    exit_game = False
    game_status = 'intro menu'
    while not exit_game:
        if game_status == 'intro menu':
            game_status = game.game_intro()
        elif game_status == 'enter game':
            game_status = game.enter_game()
        elif game_status == 'exit game':
            exit_game = True


if __name__ == '__main__':
    main()
