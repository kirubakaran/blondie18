#!/home/kiru/pyenv/neuro2/bin/python

import sys
import copy
import argparse
import os

import runner
from blondiegen import BlondieBrain

DEBUG = False
DATADIR = "/media/tera/blondiehome"

def sayit(t):
    sys.stderr.write('%s\n' % t)
    sys.stderr.flush()

def debugit(t):
    if DEBUG:
        sayit("> [%s]" % t)

def quit(t):
    sayit(t)
    sys.exit()
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play Connect-4')
    parser.add_argument('--printit',required=False,action='store_true')
    parser.add_argument('--debug',required=False,action='store_true')
    parser.add_argument('--moves',required=False)
    parser.add_argument('--autopilot',required=False)
    parser.add_argument('--blondiebrain',required=True,help='Provide file name of the blondie neural network to load. Enter "latest" to load the latest.')
    args = vars(parser.parse_args())

    if args['blondiebrain'] == 'latest':
        blondiefiles = sorted([ f for f in os.listdir(DATADIR) if f.startswith('blondie-')])
        blondiefile  = blondiefiles[-1]        
    else:
        blondiefile  = args['blondiebrain']
    sayit("Loading Blondie : %s"%(blondiefile,))
    blondie = BlondieBrain(paramfile=blondiefile)
    
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
    sayit("Ready")
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
            try:
                game.push_move(l)
            except ValueError:
                quit("You made an illegal move and lost.")
            if game.is_won():
                quit("You won!")
        m = blondie.nextmove(game)
        if m < 0 or m > 6:
            print m
            quit("I made an illegal move and lost.")
        err = False
        try:
            game.push_move(m)
        except ValueError:
            err = True
        else:
            # output move
            print m
            if game.is_won():
                quit("I won!")
        if err:
            print m
            quit("I made an illegal move and lost.")

        if args['printit']:
            game.print_grid()
            
        sys.stdout.flush()
