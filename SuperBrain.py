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
        self.__tries = [[[1,1],[2,2],[3,3],[4,4]]]
        self.__solved = 0
        print('\033[2J')

    def __is_playable(self, quit=0):
        """ Return 0 when solved or no tries are left. Return 1 otherwise."""
        if len(self.__tries) >= self.__max_tries or (self.__solved) or quit:
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

            self.__code_hint[0], self.__code_hint[1], self.__code_hint[2] =                       right_guess, right_colour, right_shape

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
        """ Print all tries, if won and otherwise hints. """
        for unsuccessful in self.__tries:
            print('\033['+str(len(self.__tries)+3)+';10H',
                self.__colourise(unsuccessful[0]),
                self.__colourise(unsuccessful[1]),
                self.__colourise(unsuccessful[2]),
                self.__colourise(unsuccessful[3]))

        if self.__solved:
            print("You won!")
        else:
            position = str(len(self.__tries)+3)
            position_str = '\033['+position+';7H {0} \033['+position+';20H R {1}, C {2}, S {3}'
            print(position_str.format(self.__max_tries - len(self.__tries), self.__code_hint[0], self.__code_hint[1], self.__code_hint[2]))
        self.__tries.append([[1,1],[2,2],[3,3],[4,4]])



##########
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

    def __get_input(self):
        """ Query the user for input. """
        nope = 1
        meh_test = 1
        # if not no_shapes:
        test_position = len(self.__tries)
        print('\033[2;8HT  1 2 3 4\033['+str(test_position+2)+';10H',self.__colourise(self.__tries[-1][0]),
                self.__colourise(self.__tries[-1][1]),
                self.__colourise(self.__tries[-1][2]),
                self.__colourise(self.__tries[-1][3]))
        while meh_test:
            while meh_test:
                k = self.__getchar()
                if k != '':
                    break
            if k == 'c':
                self.__tries[-1][self.__bracket][0] = self.__tries[-1][self.__bracket][0]%4 + 1
            elif k == 'f':
                self.__tries[-1][self.__bracket][1] = self.__tries[-1][self.__bracket][1]%4 + 1
            elif k == 'r':
                self.__reset_game()
            elif k == 'g':
                continue
            elif k == 'q':
                break
            elif k == '1' or k == '2' or k == '3' or k == '4':
                self.__bracket = int(k) - 1
            else:
                print("\033[10;4H 1/2/3/4 for the stone\n\033[4C(c)olour rotation\n\033[4C(s)hape rotation\n\033[4C(g)uess\n\033[4C(r)estart or (q)uit")

            print('\033[3;10H',self.__colourise(self.__tries[-1][0]),
                self.__colourise(self.__tries[-1][1]),
                self.__colourise(self.__tries[-1][2]),
                self.__colourise(self.__tries[-1][3])+' ')




        #self.__tries.append(eval(input("Try your best!:\n")))

        if nope:	
            self.__compare_solution(self.__tries[-1])
            self.__update_UI()
        else:
            print("invalid input, use [[], [], [], []] - or run on linux")





new_game = Superbrain().start_game()
