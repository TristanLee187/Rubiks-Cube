# Driver file, which supports:
# 1) scrambling: generating a random scramble,
#                reading a scramble from a text file in cube notation,
#                reading colors of "stickers" in a flat layout from a text file.
#    The resulting cube object is printed in a flat layout
# 2) interaction, which supports a variety of functions

from sys import argv
from Logic import logic
def run():
    cube = logic.Cube()
    mode = argv[1]
    s=['?']
    if mode=='interact':
        logic.interact()
        return
    if mode=='see':
        logic.see_scramble(cube, argv[2])
    else:
        if mode=='random':
            s = logic.gen_scramble(int(argv[2]))
        elif mode=='read':
            s = logic.read_scramble(argv[2])
        else:
            print('Invalid command')
            return
        logic.scrambler(cube, s)
    print()
    print("Scramble:",*s)
    print()
    print(cube)


run()
