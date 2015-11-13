# -*- coding: utf-8 -*-

# Superbrain: Mastermind with altered ruleset
# stones consisting of unique colour and unique shape combination
#
# github at https://github.com/banur/EPR1_SuperBrain
#
# Superbrain v0.1: working input and gamestate
# Superbrain v0.2: working comparison and output
__author__ = ""


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
    __code_hint = [[], [], []]    # colour - shape - both right
    __tries = 8
    __solved = 0

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
        game_state.__player_input = game_state.rnd_fill(4, 4, 4)
        print(game_state.__rnd_code)
        game_state.__tries = 8
        game_state.__solved = 0

    def is_playable():
        if game_state.__tries and (not game_state.__solved):
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

    def compare_solution(test_solution):
        if test_solution == game_state.__rnd_code:
            print("great")
            game_state.__solved = 1
        else:
            game_state.__tries -= 1
            game_state.hints(test_solution)
            print(
                "R %s, C %s, F %s, tries left: %s" %
                (game_state.__code_hint[0],
                 game_state.__code_hint[1],
                 game_state.__code_hint[2],
                 game_state.__tries))

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
        print(
            game_state.colourise(
                game_state.__player_input[0]), game_state.colourise(
                game_state.__player_input[1]), game_state.colourise(
                game_state.__player_input[2]), game_state.colourise(
                    game_state.__player_input[3]))

    def get_input():
        game_state.__player_input = eval(input("Try your best!:\n"))
        game_state.compare_solution(game_state.__player_input)
        game_state.update_UI()

play_again = "y"

while play_again == "y":
    game_state.reset_game()
    while game_state.is_playable():
        game_state.get_input()

    play_again = input("play again? [y/n] ")
