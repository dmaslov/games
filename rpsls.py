#!/usr/bin/env python

import os
import sys
import random

choice = ('rock', 'Spock', 'paper', 'lizard', 'scissors',)


def rpsls(name = None):
    player_number = choice.index(name) if name in choice else -1
    random.seed()
    comp_number = random.randrange(0, 5)
    comp_name = choice[comp_number]
    winner = None
    show_result = True

    if player_number < 0:
        show_result = False
        print '\n"%s" is unacceptable..\n' % str(name)
    elif player_number == comp_number:
        winner = 'You and I tie!'
    else:
        if (player_number - comp_number) % 5 in(1, 2):
            winner = 'You win!'
        else:
            winner = 'I win!'

    if show_result:
        print '\n', 'You chooses %s' % name
        print 'I choose %s' % comp_name
        print winner, '\n'

def run():
    input = raw_input("[rock/Spock/paper/lizard/scissors]?: ")
    rpsls(input)
    again = raw_input("Again?[y/n]:")
    if again == 'y':
        os.system('cls' if os.name == 'nt' else 'clear')
        run()
    else:
        print '\nBye~'
        exit()

run()
