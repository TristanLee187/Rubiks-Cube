# Terminal based interactive script

from Logic import logic
from subprocess import run


def interact():
    print('Hello There!')
    cube = logic.Cube()
    print('Your cube is ready! Type \'help\' to bring up the help menu')

    help_text = ['`help` brings up this menu',
                 '`scramble` followed by moves in cube notation (R, L, R\', R2, etc.) will scramble',
                 '\tthe cube accordingly; you can put multiple moves on the same line, separated by spaces',
                 '\tsupported moves include: the outer face turns (R, L, U, D, F, B), their corresponding',
                 '\twide moves (r, l, u, d, f, b), slice moves (M, E, S), and cube rotations (x, y, z)',
                 '`random n` applies a random scramble of length n to the cube',
                 '`read filename` reads a scramble in cube notation from filename (a text file),',
                 '\tand applies the scramble to the cube (see scramble.txt for an example)',
                 '`see filename` gets the colors of the stickers of each face of the cube in a flat format',
                 '\tfrom filename (a text file), and assigns those colors to the cube (see layout.txt for an example)',
                 '`reset` replaces the cube with a new (solved) cube object',
                 '`solve` uses the solver in the Solver package to get a solution to the scrambled cube, and prints it'
                 '`print` prints the cube in a flat layout',
                 '`quit` stops the interactive script']

    while True:
        command = input('>>>').split()
        if not command:
            pass
        elif command[0] == 'help':
            for line in help_text:
                print(line)
        elif command[0] == 'scramble':
            logic.scrambler(cube, command[1:])
        elif command[0] == 'random':
            s = logic.gen_scramble(int(command[1]))
            print('Scramble:', *s)
            logic.scrambler(cube, s)
        elif command[0] == 'read':
            s = logic.read_scramble(command[1])
            logic.scrambler(cube, s)
        elif command[0] == 'see':
            logic.see_scramble(cube, command[1])
        elif command[0] == 'reset':
            cube = logic.Cube()
        elif command[0] == 'solve':
            sol = run(['pypy3', 'Solver/solver.py', cube.__str__()], capture_output=True)
            sol = sol.stdout.decode('utf-8').strip()
            print('Solution: ' + sol)
            logic.scrambler(cube, sol.split())
        elif command[0] == 'print':
            print()
            print(cube)
        elif command[0] == 'quit':
            print('Goodbye!')
            break
        else:
            print('Invalid command')


if __name__ == '__main__':
    interact()
