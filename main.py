# Driver file, which supports:
# 1) scrambling: generating a random scramble,
#                reading a scramble from a text file in cube notation,
#                reading colors of "stickers" in a flat layout from a text file.
#    The resulting cube object is printed in a flat layout

from sys import argv, path
path.append('./Logic')
from cube import *
from scrambler import *
from interact import *

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
        scrambler(cube,s)
    print()
    print("Scramble:",*s)
    print()
    print(cube)

run()