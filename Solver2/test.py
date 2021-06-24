from FastCube import *
from G1 import *
import time


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
    for num in scramble:
        c.move(num)


def scramble_str_to_num(scramble):
    ans = []
    moves = ['U', 'F', 'R', 'B', 'L', 'D']
    for move in scramble.split():
        add = 3*moves.index(move[0])
        add += 1*(move[-1]=='\'') + 2*(move[-1]=='2')
        ans.append(add)
    return ans


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
    # speed_check(rta, cube)
    s = input('Scramble: ')
    s = scramble_str_to_num(s)
    scrambler(cube, s)

    sol = []
    speed_check(id_dfs, cube, 0, sol)
    print(cube)
    print(scramble_num_to_str(sol))
