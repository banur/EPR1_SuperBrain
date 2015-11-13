# -*- coding: utf-8 -*-

# Superbrain: Mastermind with altered ruleset
# stones consisting of unique colour and unique shape combination
#
# github at https://github.com/banur/EPR1_SuperBrain
#
# Superbrain v0.1: working input and gamestate
# Superbrain v0.2: working comparison and output
__author__ = " "


from random import choice as random_choice
no_colours = 0
no_shapes = 0

try:
    import colorama
except ImportError:
    no_colours = 1

try:
    import sys
    import tty
    import termios
    import itertools
except ImportError:
    no_shapes = 1


class game_state:
    __rnd_code = []
    __code_hint = [0, 0, 0]    # colour - shape - both right
    __tries = []
    __max_tries = 8
    __solved = 0
# hax! ########
    __cheat = 1  # set to 0
###############

    __d_colour = {
        1: '\033[31;1m',
        2: '\033[32;1m',
        3: '\033[33;1m',
        4: '\033[35;1m'}  # red, green, yellow, magenta
    __d_alt_colour = {1: 'red ', 2: 'green ', 3: 'yellow ', 4: 'magenta '}
    __d_shape = {1: '\u2665', 2: '\u2663', 3: '\u2660', 4: '\u2666'}
    __d_alt_shape = {1: '\u0025', 2: '\u0023', 3: '\u0021', 4: '\u0026'}

    def reset_game():
        game_state.__rnd_code = game_state.rnd_fill(4, 4, 4)
        if game_state.__cheat:
            print(game_state.__rnd_code)
        game_state.__tries.clear
        game_state.__solved = 0

    def is_playable():
        if len(game_state.__tries) < game_state.__max_tries and (
                not game_state.__solved):
            return 1
        else:
            return 0

    def rnd_fill(colours, shapes, stones):
        """Colour and shapes must be at least equal to 'stone'
        """

        if colours <= stones >= shapes:
            colour_list = []
            shapes_list = []
            rnd_list = []
            for i in range(1, colours + 1):
                colour_list += str(i)

            for i in range(1, shapes + 1):
                shapes_list += str(i)

            for i in range(1, stones + 1):
                rnd_colour = random_choice(colour_list)
                rnd_shape = random_choice(shapes_list)

                rnd_list.append([int(rnd_colour), int(rnd_shape)])
                colour_list.remove(rnd_colour)
                shapes_list.remove(rnd_shape)
            return rnd_list

    def compare_solution(test_solution):
        if test_solution == game_state.__rnd_code:
            print("great")
            game_state.__solved = 1
        else:
            game_state.hints(test_solution)

    def hints(test_solution):
        right_guess = 0
        right_colour = 0
        right_shape = 0

        for bracket in range(len(game_state.__rnd_code)):

            if game_state.__rnd_code[bracket] == test_solution[bracket]:
                right_guess += 1
            else:
                for i in range(len(game_state.__rnd_code[bracket])):
                    if game_state.__rnd_code[bracket][
                            i] == test_solution[bracket][i]:
                        right_colour += 1
                    elif game_state.__rnd_code[bracket][i] == test_solution[bracket][i]:
                        right_shape += 1

        game_state.__code_hint[0], game_state.__code_hint[
            1], game_state.__code_hint[2] = right_guess, right_colour, right_shape

    def colourise(array):
        colour = 0
        shape = 0

        if not no_colours:
            colour = game_state.__d_colour[array[0]]
        else:
            colour = game_state.__d_alt_colour[array[0]]

        if not no_shapes:
            shape = game_state.__d_shape[array[1]]
        else:
            shape = game_state.__d_alt_shape[array[1]]

        return colour + shape + '\033[0m'

    def update_UI():
        for unsuccessful in game_state.__tries:
            print(
                game_state.colourise(
                    unsuccessful[0]), game_state.colourise(
                    unsuccessful[1]), game_state.colourise(
                    unsuccessful[2]), game_state.colourise(
                        unsuccessful[3]))
        print(
            "R %s, C %s, F %s, tries left: %s" %
            (game_state.__code_hint[0],
             game_state.__code_hint[1],
             game_state.__code_hint[2],
             game_state.__max_tries - len(game_state.__tries)))
###########################
# experimental
    symbols = [
        "\u25B2",
        "\u25C6",
        "\u25CF",
        "\u2605",
        "\u2660",
        "\u2663",
        "\u2665",
        "\u2666"]
    colours = [
        "\033[94;2m  \033[0m",
        "\033[43;2m  \033[0m",
        "\033[41;2m  \033[0m",
        "\033[41;2m  \033[0m",
        "\033[44;2m  \033[0m",
        "\033[42;2m  \033[0m",
        "\033[46;2m  \033[0m",
        "\033[45;2m  \033[0m"]

    def _Getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(3)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    list_position = 0
    colours = 0

    def get():
        inkey = _Getch()
        while(1):
            k = inkey()
            if k != '':
                break
        if k == '\x1b[A':
            status.list_position += 1
        elif k == '\x1b[B':
            status.list_position -= 1
        elif k == '\x1b[C':
            status.colours += 1
        elif k == '\x1b[D':
            status.colours -= 1
        elif k == 'c':
            print("c")
        else:
            print("not an arrow key!: ", k)


##################################

    def get_input():
        nope = 1
       # if not no_shapes:

        game_state.__tries.append(eval(input("Try your best!:\n")))

        if nope:
            game_state.compare_solution(game_state.__tries[-1])
            game_state.update_UI()
        else:
            print("invalid input, use [[], [], [], []] - or run on linux")

play_again = "y"

while play_again == "y":
    game_state.reset_game()
    while game_state.is_playable():
        game_state.get_input()

    play_again = input("play again? [y/n] ")
