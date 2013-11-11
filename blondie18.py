#!/home/kiru/pyenv/neuro2/bin/python

import sys
import copy
import argparse

import runner
from blondie18 import BlondieBrain

DEBUG = False

def sayit(t):
    sys.stderr.write('%s\n' % t)
    sys.stderr.flush()

def debugit(t):
    if DEBUG:
        sayit("> [%s]" % t)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play Connect-4')
    parser.add_argument('--printit',required=False,action='store_true')
    parser.add_argument('--debug',required=False,action='store_true')
    parser.add_argument('--moves',required=False)
    parser.add_argument('--autopilot',required=False)
    parser.add_argument('--blondiebrain',required=True)
    args = vars(parser.parse_args())

    blondie = BlondieBrain(paramfile=args['blondiebrain'])
    
    if args['autopilot']:
        autopilotn = int(args['autopilot'])
    else:
        autopilotn = 0
    
    DEBUG = args['debug']
    
    #if moves are supplied, play them
    if args['moves']:
        moves  = args['moves'].split(',')
    else:
        moves = []
        
    game = runner.Game()
    while not sys.stdin.closed:
        if len(moves) > 0:
            line = moves.pop(0)
            sayit(line)
        elif autopilotn > 0:
            autopilotn -= 1
            line = ''
        else:
            line = sys.stdin.readline()
        if line.strip() == 'printit':
            args['printit'] = True
            continue
        try:
            l = int(line)
        except ValueError:
            pass
        else:
            game.push_move(l)
        m = blondie.nextmove(game)
        err = False
        try:
            game.push_move(m)
        except ValueError:
            err = True
        else:
            # output move
            print m
        if err:
            print m
            print "I made an illegal move :-("

        if args['printit']:
            game.print_grid()
            
        sys.stdout.flush()
