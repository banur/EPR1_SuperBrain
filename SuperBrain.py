# -*- coding: utf-8 -*-

# Superbrain: Mastermind with altered ruleset
# stones consisting of unique colour and unique form combination
# 
# github at https://github.com/banur/EPR1_SuperBrain
# 
# Superbrain v0.1: working input and gamestate
# Superbrain v0.2: working comparison and output
__author__ = 


from random import *
import colorama, sys, tty, termios
colorama.init()
import itertools

class game_state:
    __rnd_code = []
    __code_hint = [[],[],[]]    # colour - form - both right
    __player_input = [[],[],[],[]]
    __tries = 8
    __solved = 0

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
        
    def rnd_fill(colours, forms, stones):
        """Colour and forms must be at least equal to 'stone'
        """


        if colours <= stones >= forms:
            colour_list = []
            forms_list = []
            rnd_list = []
            for i in range(1, colours + 1):
                colour_list += str(i)
            
            for i in range(1, forms + 1):
                forms_list += str(i)

            for i in range(1, stones + 1):
                rnd_colour = colour_list[randint(1, len(colour_list)) - 1]
                rnd_form = forms_list[randint(1, len(forms_list)) - 1]

                rnd_list.append([int(rnd_colour), int(rnd_form)])
                colour_list.remove(rnd_colour)
                forms_list.remove(rnd_form)
            return rnd_list

    def hints(test_solution):
        right_guess = 0
        right_colour = 0
        right_form = 0

        for bracket in range(len(game_state.__rnd_code)):

            if game_state.__rnd_code[bracket] == test_solution[bracket]:
                right_guess += 1
            else:
                for i in range(len(game_state.__rnd_code[bracket])):
                    if game_state.__rnd_code[bracket][i] == test_solution[bracket][i]:
                        right_colour += 1
                    elif game_state.__rnd_code[bracket][i] == test_solution[bracket][i]:
                        right_form += 1

        game_state.__code_hint[0], game_state.__code_hint[1], game_state.__code_hint[2] = right_guess, right_colour, right_form
            
    def compare_solution(test_solution):
        if test_solution == game_state.__rnd_code:
            print("great")
            game_state.__solved = 1
        else:
            game_state.__tries -= 1
            game_state.hints(test_solution)
            print("R %s, C %s, F %s, tries left: %s" % (game_state.__code_hint[0], game_state.__code_hint[1], game_state.__code_hint[2], game_state.__tries))

    def colourise(array):
        colour = 0
        form = 0
        
        if array[0] == 1:
            colour = '\033[31;1m' # red
        if array[0] == 2:
            colour = '\033[32;1m' # green
        if array[0] == 3:
            colour = '\033[33;1m' # yellow
        if array[0] == 4:
            colour = '\033[35;1m' # magenta
            
        if array[1] == 1:
            form = '\u0023' # symbol1
        if array[1] == 2:
            form = '\u0024' # symbol
        if array[1] == 3:
            form = '\u0026' # symbol
        if array[1] == 4:
            form = '\u0025' # symbol

        return colour + form + '\033[0m'

    def update_UI():
        print(game_state.colourise(game_state.__player_input[0]), game_state.colourise(game_state.__player_input[1]), game_state.colourise(game_state.__player_input[2]), game_state.colourise(game_state.__player_input[3]))

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
