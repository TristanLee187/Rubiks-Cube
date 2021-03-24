from cube import *
from scrambler import *

def interact():
    print('Hello There!')
    print('Getting your cube ready...')
    cube = Cube()
    print('Cube is ready! Type help to bring up the help menu')

    help_text = ['\'help\' brings up this menu',
                 '\'scramble\' followed by moves in cube notation (R, L, R\', R2, etc.) will scramble',
                 '\tthe cube accordingly; you can put multiple moves on the same line, separated by spaces',
                 '\'random n\' applies a random scramble of length n to the cube',
                 '\'read filename\' reads a scramble in cube notation from filename (a text file),',
                 '\tand applies the scramble to the cube',
                 '\'see filename\' gets the colors of the stickers of each face of the cube in a flat format',
                 '\tfrom filename (a text file), and assigns those colors to the cube',
                 '\'reset\' replaces the cube with new (solved) cube object',
                 '\'print\' prints the cube in a flat layout',
                 '\'quit\' stops the interaction']

    while True:
        command = input('>>>').split()
        if command[0]=='help':
            for line in help_text:
                print(line)
        elif command[0]=='scramble':
            scrambler(cube, command[1:])
        elif command[0]=='random':
            s=gen_scramble(int(command[1]))
            print('Scramble:',*s)
            scrambler(cube,s)
        elif command[0]=='read':
            s=read_scramble(command[1])
            scrambler(cube,s)
        elif command[0]=='see':
            see_scramble(cube, command[1])
        elif command[0]=='reset':
            cube=Cube()
        elif command[0]=='print':
            print()
            print(cube)
        elif command[0]=='quit':
            print('Goodbye!')
            break
        else:
            print('Invalid command')
