# Driver file, which supports:
# 1) scrambling: generating a random scramble,
#                reading a scramble from a text file in cube notation,
#                reading colors of "stickers" in a flat layout from a text file.
#    The resulting cube object is printed in a flat layout
# 2) interaction, which supports a variety of functions

from sys import argv
from interact import *
from scrambler import *

def run():
    cube = Cube()
    mode = argv[1]
    s=['?']
    if mode=='interact':
        interact()
        return
    if mode=='see':
        see_scramble(cube,argv[2])
    else:
        if mode=='random':
            s = gen_scramble(int(argv[2]))
        elif mode=='read':
            s = read_scramble(argv[2])
        else:
            print('Invalid command')
            return
        scrambler(cube,s)
    print()
    print("Scramble:",*s)
    print()
    print(cube)

run()