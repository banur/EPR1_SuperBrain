# -*- coding: utf-8 -*-

# Superbrain: Mastermind with altered ruleset
# stones consisting of unique colour and unique shape combination
#
# github at https://github.com/banur/EPR1_SuperBrain
#
# Superbrain v0.1: working input and gamestate
# Superbrain v0.2: working comparison and output
# Superbrain v0.3: working colours / shapes, OS independent
# Superbrain v0.4: objectified
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


class Superbrain(object):

    __cheat = 1  # set to 0

    __rnd_code = []
    # colour - shape - both right
    __code_hint = [0, 0, 0]
    __tries = []
    __max_tries = 8
    __solved = 0
    # red, green, yellow, magenta
    __d_colour = {1: '\033[31;1m', 2: '\033[32;1m', 3: '\033[33;1m',
                  4: '\033[35;1m'}
    __d_alt_colour = {1: 'red ', 2: 'green ', 3: 'yellow ', 4: 'magenta '}
    # hearts, clubs, spades, diamonds __OR__ %, # !, &
    __d_shape = {1: '\u2665', 2: '\u2663', 3: '\u2660', 4: '\u2666'}
    __d_alt_shape = {1: '\u0025', 2: '\u0023', 3: '\u0021', 4: '\u0026'}

    def start_game(self):
        play_again = "y"
        while play_again == "y":
            self.__reset_game()
            while self.__is_playable():
                self.__get_input()
            play_again = input("play again? [y/n] ")

    def __reset_game(self):
        """Reset the game."""
        self.__rnd_code = self.__rnd_fill(4, 4, 4)
        if self.__cheat:
            print(self.__rnd_code)
        self.__tries.clear()
        self.__solved = 0

    def __is_playable(self):
        """ Return 0 when solved or no tries are left. Return 1 otherwise."""
        if len(self.__tries) < self.__max_tries and (
                not self.__solved):
            return 1
        else:
            return 0

    def __rnd_fill(self, colours, shapes, stones):
        """ Generate the random code, return the list. """
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

    def __compare_solution(self, test_solution):
        """ Compare the input to the code and generate match-based hints. """
        if test_solution == self.__rnd_code:
            self.__solved = 1
        else:
            right_guess = 0
            right_colour = 0
            right_shape = 0

            for bracket in range(len(self.__rnd_code)):

                if self.__rnd_code[bracket] == test_solution[bracket]:
                    right_guess += 1
                else:
                    for i in range(len(self.__rnd_code[bracket])):
                        if self.__rnd_code[bracket][
                                i] == test_solution[bracket][i]:
                            right_colour += 1
                        elif self.__rnd_code[bracket][i] == test_solution[bracket][i]:
                            right_shape += 1

            self.__code_hint[0],
            self.__code_hint[1],
            self.__code_hint[2] = right_guess, right_colour, right_shape

    def __colourise(self, array):
        """ Convert the input into colours / shapes or their alternative. """
        colour = 0
        shape = 0

        if not no_colours:
            colour = self.__d_colour[array[0]]
        else:
            colour = self.__d_alt_colour[array[0]]

        if not no_shapes:
            shape = self.__d_shape[array[1]]
        else:
            shape = self.__d_alt_shape[array[1]]

        return colour + shape + '\033[0m'

    def __update_UI(self):
        """ Output all tries, if won or otherwise hints. """
        for unsuccessful in self.__tries:
            print(
                self.__colourise(unsuccessful[0]),
                self.__colourise(unsuccessful[1]),
                self.__colourise(unsuccessful[2]),
                self.__colourise(unsuccessful[3]))

        if self.__solved:
            print("You won!")
        else:
            print(
                "R %s, C %s, F %s, tries left: %s" % (
                    self.__code_hint[0],
                    self.__code_hint[1],
                    self.__code_hint[2],
                    self.__max_tries - len(self.__tries)))

    if not no_shapes:
        def __getchar(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(3)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

    symbols = [
        "\u25B2", "\u25C6", "\u25CF", "\u2605",
        "\u2660", "\u2663", "\u2665", "\u2666"]
    colours = [
            "\033[94;2m  \033[0m", "\033[43;2m  \033[0m", "\033[41;2m  \033[0m",
            "\033[41;2m  \033[0m", "\033[44;2m  \033[0m", "\033[42;2m  \033[0m",
            "\033[46;2m  \033[0m", "\033[45;2m  \033[0m"]


    def __get_input(self):
        """ Query the user for input. """
        nope = 0
        # if not no_shapes:
        a = 0
        b = 0
        while True:
            k = self.__getchar()
            if k != '':
                break
            if k == '\x1b[A':
                a += 1
            elif k == '\x1b[B':
                a -= 1
            elif k == '\x1b[C':
                b += 1
            elif k == '\x1b[D':
                b -= 1
            elif k == 'ccc':
                print("c")
            else:
                print("not an arrow key!: ", k)
            print(symbols[a])
            print(colours[b])


        #self.__tries.append(eval(input("Try your best!:\n")))

        if nope:
            self.__compare_solution(self.__tries[-1])
            self.__update_UI()
        else:
            print("invalid input, use [[], [], [], []] - or run on linux")





new_game = Superbrain().start_game()
