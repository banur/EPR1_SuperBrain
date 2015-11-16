""" Superbrain: Mastermind with altered ruleset

Stones consists of unique colour and unique shape combination.
Four Stones, four colours, four shapes, eight chances.
Feedback through printed hints, control through OS matched interface.

"""

from random import choice as random_choice
import re
# variables to control the nature of the OS running this programm
no_colour_support = 1
no_shape_support = 0
install_loop = ""

try:
    import sys
    import tty
    import termios
    import itertools
except ImportError:
    no_shape_support = 1


def install_and_import(package):
    """ Try to load module or try to download and load module otherwise. """
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

while no_colour_support:
    install_and_import('colorama')
    try:
        colorama.init()
        no_colour_support = 0
    except:
        print("Please install colorama.\nEither connect to the Internet and run\
 again or install\nmanually from https://pypi.python.org/pypi/colorama")
        install_loop = input("\nTry again? ('q' to quit)\n")
    if install_loop.lower() == "q":
        exit()

__author__ = ": Vincent Kühn, 6192860: Georg Schuhardt"
__copyright__ = "Copyright 2015/2016 – EPR-Goethe-Uni"
__credits__ = "Jonathan Hartley for colorama"
__email__ = "georg.schuhardt@gmail.com"
__github__ = "https://github.com/banur/EPR1_SuperBrain"


class Superbrain(object):
    """ Create the game and have it running until the user exits. """
    __cheat_enabled = 0
    __play_again = "y"
    __rnd_code = []
    # both right - colour - shape
    __code_hint = [0, 0, 0]
    __tries = []
    __max_tries = 8
    __solved = 0
    # red, green, yellow, magenta __OR__ r, g, y, m
    __d_colour = {1: '\033[31;1m', 2: '\033[32;1m', 3: '\033[33;1m',
                  4: '\033[35;1m', 5: '\u001E\033[0m'}
    __d_alt_colour = {1: 'r', 2: 'g', 3: 'y', 4: 'm', 5: ""}
    # hearts, clubs, spades, diamonds __OR__ %, # !, &
    __d_shape = {1: '\u2665', 2: '\u2663', 3: '\u2660', 4: '\u2666'}
    __d_alt_shape = {1: '\u0025', 2: '\u0024', 3: '\u0021', 4: '\u0026'}

    def start_game(self):
        """ Loop the games subroutines until the player quits. """
        while self.__play_again == "y":
            self.__reset_game()
            while self.__is_playable():
                self.__get_input()
                self.__compare_solution(self.__tries[-1])
                self.__update_UI()
        self.__exit_game()

    def __reset_game(self):
        """ Reset the game. """
        self.__rnd_code = self.__rnd_fill(4, 4, 4)
        self.__tries = [[[1, 1], [2, 2], [3, 3], [4, 4]]]
        self.__build_UI()
        self.__solved = 0

    def __is_playable(self):
        """ Return 0 when solved or no tries are left. Return 1 otherwise."""
        if len(self.__tries) > self.__max_tries or (self.__solved):
            return 0
        else:
            return 1

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
        right_guess = 0
        right_colour = 0
        right_shape = 0

        for bracket in range(len(self.__rnd_code)):
            if self.__rnd_code[bracket] == test_solution[bracket]:
                right_guess += 1
            else:
                if self.__rnd_code[bracket][0] == test_solution[bracket][0]:
                    right_colour += 1
                elif self.__rnd_code[bracket][1] == test_solution[bracket][1]:
                    right_shape += 1

        self.__code_hint[0], self.__code_hint[1], self.__code_hint[
            2] = right_guess, right_colour, right_shape
        if self.__code_hint[0] == 4:
            self.__solved = 1

    def __colourise(self, array):
        """ Convert and return input as colours/shapes or alternative. """
        colour = 0
        shape = 0
        coloured_result = ""
        for bracket in array:
            if no_colour_support:
                colour = self.__d_alt_colour[bracket[0]]
            else:
                colour = self.__d_colour[bracket[0]]

            if no_shape_support:
                shape = self.__d_alt_shape[bracket[1]]
            else:
                shape = self.__d_shape[bracket[1]]

            coloured_result += colour + shape + '\033[0m '

        return coloured_result

    def __cheat(self):
        """ Assist the fellow nerd. """
        print("\033[5;8H{0}".format(self.__colourise(self.__rnd_code)))
        print("\033[17;1H\033[2K\033[16;1H")
        self.__cheat_enabled = 1

    def __build_UI(self):
        """ Print the basic UI. """
        UI_elements = {"clear": '\033[2J',
                       "header": '\033[6;5HT  1 2 3 4  |  R  C  S',
                       "intro": "\033[3;3HIn eight attempts, find the "+
                       "right code with unique colours and unique shapes!",
                       "options": "\033[22;25Hoptions: new, quit"}
        print(
            UI_elements["clear"],
            UI_elements["header"],
            UI_elements["intro"])
        if not no_shape_support:
            print('\033[7;7H', self.__colourise(self.__tries[-1]))
        else:
            print(UI_elements["options"])
        if self.__cheat_enabled:
            self.__cheat()
        self.__help()
        print("\033[16;1H")

    def __update_UI(self):
        """ Print the latest attempt, if won or hints. Prepare next round. """

        position = str(len(self.__tries) + 6)
        print('\033[' + position + ';7H',
              self.__colourise(self.__tries[-1]))

        position_str = '\033[' + position + \
            ';5H{0} \033[' + position + ';17H|  {1}  {2}  {3}'
        print(position_str.format(len(self.__tries),
                                  self.__code_hint[0], self.__code_hint[1],
                                  self.__code_hint[2]))
        if self.__solved:
            print("\033[19;25HYou won!")
        elif (self.__max_tries - len(self.__tries)) <= 0:
            print("\033[19;25HBetter luck next time!")
        if self.__solved or (self.__max_tries - len(self.__tries)) <= 0:
            print("\033[20;25Hplay again? [y/n]\033[17;1H\033[2K\033[16;1H")
            self.__play_again = input().lower()

        if no_shape_support:
            self.__tries.append([[1, 1], [2, 2], [3, 3], [4, 4]])
        else:
            self.__tries.append(self.__tries[-1])
            print('\033[' + str(len(self.__tries) + 6) + ';7H',
                  self.__colourise(self.__tries[-1]))
        print('\033[17;1H\033[2K\033[16;1H')

    def __exit_game(self):
        """ Clear the screen and exit. """
        print('\033[2J\033[0;0H')
        exit()

    def __help(self):
        """ Print the help text matching the input method. """
        if no_shape_support:
            help_text = \
                "\033[6;33HTry running with Unicode and proper terminal." + \
                "\033[7;33HInput a single line of eight numbers," + \
                "\033[8;33Halternating colour and shape." + \
                "\033[10;33H1: {0}{8}, 2: {1}{8}, 3: {2}{8}, 4: {3}{8}" + \
                "\033[11;33H1: {4}, 2: {5}, 3: {6}, 4: {7}" + \
                "\033[12;33HThus 11223344 results in {9}" + \
                "\033[14;33HR: both right, C: colour right, S: shape right"+ \
                "\033[16;1H\033[2K\033[16;1H"
            if no_colour_support:
                colour = self.__d_alt_colour
            else:
                colour = self.__d_colour
            shape = self.__d_alt_shape
        else:
            help_text = "\033[6;33HUse 1/2/3/4 to select stone," + \
                "\033[7;33H(c) to rotate colours," + \
                "\033[8;33H(s) to rotate shapes," + \
                "\033[9;33H(g) to guess," + \
                "\033[10;33H(r) to restart," + \
                "\033[11;33H(q) to quit" + \
                "\033[14;33HR: both right, C: colour right, S: shape right"
                "\033[16;1H"
            colour = self.__d_colour
            shape = self.__d_shape

        print(help_text.format(colour[1], colour[2], colour[3], colour[4],
                               shape[1], shape[2], shape[3],
                               shape[4], colour[5],
                               self.__colourise([[1, 1], [2, 2],
                                                 [3, 3], [4, 4]])))

    def __fallback_input(self):
        """ Take an input string and convert to the input list."""
        not_empty = 1
        while not_empty:
            user_input = input()
            if user_input.lower() == "new":
                self.__reset_game()
            elif user_input.lower() == "quit":
                self.__exit_game()
            elif user_input == "IDDQD" or\
                    user_input == "UPUPDOWNDOWNLEFTRIGHTLEFTRIGHTBASTART":
                self.__cheat()
            else:
                user_input = re.sub("[^1-4]", "", user_input)
                if len(user_input) == 8:
                    for num_bracket in range(len(self.__tries[-1])):
                        self.__tries[-1][num_bracket][0] = \
                            int(list(user_input[:2])[:1][0])
                        self.__tries[-1][num_bracket][1] = \
                            int(list(user_input[:2])[1:][0])
                        user_input = user_input[2:]
                    not_empty = 0

            print('\033[17;1H\033[2K\033[16;1H')

    # only when the needed modules are loaded
    if not no_shape_support:
        def __get_char(self, char_count=1):
            """ Listen to pressed keys and return as string. """
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(char_count)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

    def __complex_input(self):
        """ Use key listener to allow on-the-fly input. """
        bracket = 0
        if not no_shape_support:
            while True:
                while True:
                    k = self.__get_char()
                    if k != '':
                        break
                if k.lower() == 'c':
                    self.__tries[-1][bracket][
                        0] = self.__tries[-1][bracket][0] % 4 + 1
                elif k.lower() == 's':
                    self.__tries[-1][bracket][
                        1] = self.__tries[-1][bracket][1] % 4 + 1
                elif k.lower() == 'r':
                    self.__reset_game()
                elif k.lower() == 'g':
                    break
                elif k.lower() == 'q':
                    self.__exit_game()
                elif k == '^':
                    extra_input = input('~')
                    if extra_input == "IDDQD" or extra_input ==\
                            "UPUPDOWNDOWNLEFTRIGHTLEFTRIGHTBASTART":
                        self.__cheat()
                    else:
                        print('\033[17;1H\033[2K\033[16;1H')
                elif k == '1' or k == '2' or k == '3' or k == '4':
                    bracket = int(k) - 1

                print('\033[' + str(len(self.__tries) + 6) + ';8H{0}\
                 \033[16;1H'.format(self.__colourise(self.__tries[-1])))

    def __get_input(self):
        """ Query the user for input. """
        if not no_shape_support:
            self.__complex_input()
        else:
            self.__fallback_input()


new_game = Superbrain().start_game()
