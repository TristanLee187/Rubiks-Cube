import time
from FastCube import FastCube
from G1 import *
from itertools import accumulate
import operator


def speed_check(f, *args):
    t0 = time.time()
    f(*args)
    t1 = time.time()
    print("Time:", t1 - t0)


def rta(c):
    i = 0
    while i < 10 ** 7:
        i += 1
        c.move(0)


def scrambler(c, scramble):
    s = scramble.split()
    for move in s:
        if move[-1] != '2':
            eval('c.{}({})'.format(move[0], len(move) == 1))
        else:
            eval('c.{}({})'.format(move[0], True))
            eval('c.{}({})'.format(move[0], True))
    return c


def scramble_num_to_str(scramble):
    ans = ''
    moves = ['U', 'F', 'R', 'B', 'L', 'D']
    for num in scramble:
        add = moves[num // 3]
        add += ['', '\'', '2'][num % 3]
        ans += add + ' '
    return ans


if __name__ == '__main__':
    cube = FastCube()
    s = input('Scramble: ')
    scrambler(cube, s)
    sol = []
    speed_check(id_dfs, cube, 0, sol)
    # speed_check(rta, cube)
    print(cube)
    print(sol)
    print(scramble_num_to_str(sol))
