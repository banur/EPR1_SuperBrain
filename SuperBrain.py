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
# Superbrain v0.5: working linux in- and output, slight control issues
# Superbrain v0.6: working windows in- and output, help text
# Superbrain v0.7: fixed logic issue
# Superbrain v0.8: fixed another logic issue, moved UI
# Superbrain v0.9: fixed windows UI
__author__ = " "


from random import choice as random_choice
import re
no_colours = 1
no_shapes = 0
install_loop = ""


def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

while no_colours:
    install_and_import('colorama')
    try:
        colorama.init()
        no_colours = 0
    except:
        print("Please install colorama.\nEither connect to the Internet and run\
 again or install\nmanually from https://pypi.python.org/pypi/colorama")
        install_loop = input("\nTry again? ('q' to quit)\n")
    if install_loop.lower() == "q":
        exit()

try:
    import sys
    import tty
    import termios
    import itertools
except ImportError:
    no_shapes = 1

class Superbrain(object):

    __cheat_enabled = 0  # set to 0
    __play_again = "y"
    __rnd_code = []
    # colour - shape - both right
    __code_hint = [0, 0, 0]
    __tries = []
    __max_tries = 8
    __solved = 0
    # red, green, yellow, magenta
    __d_colour = {1: '\033[31;1m', 2: '\033[32;1m', 3: '\033[33;1m',
                  4: '\033[35;1m', 5: '\u001E\033[0m'}
    __d_alt_colour = {1: 'r', 2: 'g', 3: 'y', 4: 'm', 5:""}
    # hearts, clubs, spades, diamonds __OR__ %, # !, &
    __d_shape = {1: '\u2665', 2: '\u2663', 3: '\u2660', 4: '\u2666'}
    __d_alt_shape = {1: '\u0025', 2: '\u0024', 3: '\u0021', 4: '\u0026'}

    def start_game(self):
        while self.__play_again == "y":
            self.__reset_game()
            while self.__is_playable():
                self.__get_input()
                self.__compare_solution(self.__tries[-1])
                self.__update_UI()
        self.__exit_game()

    def __reset_game(self):
        """Reset the game."""
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
                if self.__rnd_code[bracket][
                        0] == test_solution[bracket][0]:
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
            if no_colours:
                colour = self.__d_alt_colour[bracket[0]]
            else:
                colour = self.__d_colour[bracket[0]]

            if no_shapes:
                shape = self.__d_alt_shape[bracket[1]]
            else:
                shape = self.__d_shape[bracket[1]]

            coloured_result += colour + shape + '\033[0m '
            
        return coloured_result
        
    def __cheat(self):
        print("\033[5;8H{0}".format(self.__colourise(self.__rnd_code)))
        print("\033[17;1H\033[2K\033[16;1H")
        self.__cheat_enabled = 1

    def __build_UI(self):
        UI_elements = {"clear":'\033[2J',
                       "header":'\033[6;5HT  1 2 3 4  |  R  C  S',
                       "intro":"\033[3;3HFind the right code, generated" + \
                       " with unique colours and unique shapes!",
                       "options":"\033[22;25Hoptions: help, new, quit"}
        print(UI_elements["clear"],UI_elements["header"], UI_elements["intro"])
        if not no_shapes:
            print('\033[7;7H', self.__colourise(self.__tries[-1]))
        else:
            print(UI_elements["options"])
        if self.__cheat_enabled:
            self.__cheat()
        print("\033[16;1H")

    def __update_UI(self):
        """ Print all tries, if won and otherwise hints. """
        
        position = str(len(self.__tries) + 6)
        print('\033[' + position + ';7H',
                self.__colourise(self.__tries[-1]))

        position_str = '\033[' + position + \
                ';5H{0} \033[' + position + ';17H|  {1}  {2}  {3}'
        print(position_str.format(self.__max_tries - len(self.__tries) + 1,
                                  self.__code_hint[0], self.__code_hint[1],
                                  self.__code_hint[2]))
        if self.__solved:
            print("\033[19;25HYou won!")
        elif (self.__max_tries - len(self.__tries)) <= 0:
            print("\033[19;25HBetter luck next time!")
        if self.__solved or (self.__max_tries - len(self.__tries)) <= 0:
            print("\033[20;25Hplay again? [y/n]\033[17;1H\033[2K\033[16;1H")
            self.__play_again = input().lower()
        
        if no_shapes:
            self.__tries.append([[1, 1], [2, 2], [3, 3], [4, 4]])
        else:
            self.__tries.append(self.__tries[-1])
            print('\033[' + str(len(self.__tries) + 6) + ';7H',
                self.__colourise(self.__tries[-1]))
        print('\033[17;1H\033[2K\033[16;1H')

    def __exit_game(self):
        print('\033[2J\033[0;0H')
        exit()

    def __help(self):
        if no_shapes:
            help_text = "\033[6;33HThis is the less comfortable version." + \
            "\033[7;33HTry running with Unicode and proper terminal." + \
            "\033[8;33HInput a single line of eight numbers," + \
            "\033[9;33Halternating colour and shape." + \
            "\033[11;33H1: {0}{8}, 2: {1}{8}, 3: {2}{8}, 4: {3}{8}" + \
            "\033[12;33H1: {4}, 2: {5}, 3: {6}, 4: {7}" + \
            "\033[14;33HThus 11223344 results in {9}" + \
            "\033[16;1H\033[2K\033[16;1H"
            if no_colours:
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
                         "\033[16;1H"
            colour = self.__d_colour
            shape = self.__d_shape
        
        print(help_text.format(colour[1], colour[2], colour[3], colour[4],
                  shape[1], shape[2], shape[3], shape[4], colour[5],
                  self.__colourise([[1,1],[2,2],[3,3],[4,4]])))
                  
    def __fallback_input(self):
        """ Take an input string and convert to the input list."""
        not_empty = 1
        while not_empty:
            user_input = input()
            
            if user_input.lower() == "help":
                self.__help()
            elif user_input.lower() == "new":
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
                        self.__tries[-1][num_bracket][0] =\
                            int(list(user_input[:2])[:1][0])
                        self.__tries[-1][num_bracket][1] =\
                            int(list(user_input[:2])[1:][0])
                        user_input = user_input[2:]
                    not_empty = 0
                else:
                    self.__help()
            print('\033[17;1H\033[2K\033[16;1H')


    if not no_shapes:
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
        bracket = 0
        if not no_shapes:
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
                elif k.lower() == 'h':
                    self.__help()
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
                else:
                    self.__help()
                    
                print('\033['+ str(len(self.__tries) + 6) +';8H{0}\
                 \033[16;1H'.format(self.__colourise(self.__tries[-1])))

    def __get_input(self):
        """ Query the user for input. """
        if not no_shapes:
            self.__complex_input()
        else:
            self.__fallback_input()


new_game = Superbrain().start_game()
