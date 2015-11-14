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
    if install_loop == "q":
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

    def __reset_game(self):
        """Reset the game."""
        self.__rnd_code = self.__rnd_fill(4, 4, 4)
        self.__build_UI()
        self.__solved = 0
        self.__tries = [[[1, 1], [2, 2], [3, 3], [4, 4]]]

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

            self.__code_hint[0], self.__code_hint[1], self.__code_hint[
                2] = right_guess, right_colour, right_shape

    def __colourise(self, array):
        """ Convert the input into colours / shapes or their alternative. """
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

    def __build_UI(self):
        UI_elements = {"clear":'\033[2J',
                       "header":'\033[3;8HT  1 2 3 4  |  R  C  S',
                       "intro":"\033[13;3HTry your best!",
                       "options":"\033[22;25Hoptions: help, new, exit"}
        print(UI_elements["clear"],UI_elements["header"], UI_elements["intro"],
        UI_elements["options"])
        print("\033[13;1H")
        if self.__cheat_enabled:
            print("\033[14;1H\033[2K\033[13;1H".
            format(self.__colourise(self.__rnd_code)))
        
    def __cheat(self):
        print("\033[3;33H{0}".
        format(self.__colourise(self.__rnd_code)))
        print("\033[14;1H\033[2K\033[13;1H")
        self.__cheat_enabled = 1
            

    def __update_UI(self):
        """ Print all tries, if won and otherwise hints. """
        
        print('\033[' + str(len(self.__tries) + 3) + ';10H',
                self.__colourise(self.__tries[-1]))

        position = str(len(self.__tries) + 3)
        position_str = '\033[' + position + \
                ';7H {0} \033[' + position + ';20H|  {1}  {2}  {3}'
        print(position_str.format(self.__max_tries - len(self.__tries) + 1,
                                  self.__code_hint[0], self.__code_hint[1],
                                  self.__code_hint[2]))
        if self.__solved:
            print("\033[19;25HYou won!")
        elif (self.__max_tries - len(self.__tries)) <= 0:
            print("\033[19;25HBetter luck next time!")
        if self.__solved or (self.__max_tries - len(self.__tries)) <= 0:
            print("\033[20;25Hplay again? [y/n]\033[14;1H\033[2K\033[13;1H")
            self.__play_again = input()
        
        print('\033[14;1H\033[2K\033[13;1H')
        self.__tries.append([[1, 1], [2, 2], [3, 3], [4, 4]])

    def __help(self):
        if no_shapes:
            help_text = "\033[6;33HThis is the less comfortable version.\
                  \033[7;33HTry running with Unicode and proper terminal.\
                  \033[9;33HInput a single line of eight numbers,\
                  \033[10;33Halternating colour and shape.\
                  \033[12;33H1: {0}{8}, 2: {1}{8}, 3: {2}{8}, 4: {3}{8}\
                  \033[13;33H1: {4}, 2: {5}, 3: {6}, 4: {7}\
                  \033[15;33HThus 11223344 results in {9}\
                  \033[14;1H\033[2K\033[13;1H"
            if no_colours:
                colour = self.__d_alt_colour
            else:
                colour = self.__d_colour
            shape = self.__d_alt_shape
        else:
            colour = self.__d_colour
            shape = self.__d_shape
        
        help_text += ""
        print(help_text.format(colour[1], colour[2], colour[3], colour[4],
                  shape[1], shape[2], shape[3], shape[4], colour[5],
                  self.__colourise([[1,1],[2,2],[3,3],[4,4]])))
                  
    def __fallback_input(self):
        """ Take an input string and convert to the input list."""
        not_empty = 1
        while not_empty:
            user_input = input()
            
            if user_input == "help":
                self.__help()
            elif user_input == "new":
                self.__reset_game()
            elif user_input == "quit":
                exit()
            elif user_input == "IDDQD":
                self.__cheat()
            else:
                user_input = re.sub("[^1-4]", "", user_input)
                if len(user_input) == 8:
                    for num_bracket in range(len(self.__tries[-1])):
                        self.__tries[-1][num_bracket][0] = int(list(user_input[:2])[:1][0])
                        self.__tries[-1][num_bracket][1] = int(list(user_input[:2])[1:][0])
                        user_input = user_input[2:]
                    not_empty = 0
                else:
                    self.__help()    
                    
                    
    if not no_shapes:
        def __getchar(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

        symbols = [
            "\u25B2", "\u25C6", "\u25CF", "\u2605",
            "\u2660", "\u2663", "\u2665", "\u2666"]
        colours = [
            "\033[94;2m  \033[0m", "\033[43;2m  \033[0m", "\033[41;2m  \033[0m",
            "\033[44;2m  \033[0m", "\033[42;2m  \033[0m", "\033[46;2m  \033[0m",
            "\033[45;2m  \033[0m"]

        a = 0
        __bracket = 0

    def __complex_input(self):
        nope = 1
        meh_test = 1
        test_position = len(self.__tries)
        print('\033[2;8HT  1 2 3 4\033[' + str(test_position + 2) + ';10H', self.__colourise(self.__tries[-1]))
        if not no_shapes:
            while meh_test:
                while meh_test:
                    k = self.__getchar()
                    if k != '':
                        break
                if k == 'c':
                    self.__tries[-1][self.__bracket][
                        0] = self.__tries[-1][self.__bracket][0] % 4 + 1
                elif k == 'f':
                    self.__tries[-1][self.__bracket][
                        1] = self.__tries[-1][self.__bracket][1] % 4 + 1
                elif k == 'r':
                    self.__reset_game()
                elif k == 'g':
                    continue
                elif k == 'q':
                    exit()
                elif k == '1' or k == '2' or k == '3' or k == '4':
                    self.__bracket = int(k) - 1
                else:
                    print(
                        "\033[10;4H 1/2/3/4 for the stone\n\033[4C(c)olour rotation\n\033[4C(s)hape rotation\n\033[4C(g)uess\n\033[4C(r)estart or (q)uit")

                print('\033[3;10H', self.__colourise(self.__tries[-1]) + ' ')

    def __get_input(self):
        """ Query the user for input. """
        if not no_shapes:
            self.__complex_input()
        else:
            self.__fallback_input()


new_game = Superbrain().start_game()
