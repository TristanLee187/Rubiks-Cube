from FastCube import *
from G1 import *
from G2 import *
from G3 import *
from G4 import *
from FullSolve import *
import time


def speed_check(f, *args):
    t0 = time.time()
    ans = f(*args)
    t1 = time.time()
    return t1 - t0, ans


def rta(c):
    a = 0
    i = 0
    while i < 10 ** 9:
        i += 1
        a |= 2


def scrambler(c, scramble):
    for num in scramble:
        c.move(num)


def scramble_str_to_num(scramble):
    ans = []
    moves = ['U', 'F', 'R', 'B', 'L', 'D']
    for move in scramble.split():
        add = 3 * moves.index(move[0])
        add += 1 * (move[-1] == '\'') + 2 * (move[-1] == '2')
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


def test_4(cube):
    g = FastCube()
    t1, sol1 = speed_check(g1_solve, cube, g)
    print("Time to G1:", t1)
    print(scramble_num_to_str(sol1), '({} moves)'.format(len(sol1)))

    t2, sol2 = speed_check(g2_solve, cube, g)
    print("Time to G2:", t2)
    print(scramble_num_to_str(sol2), '({} moves)'.format(len(sol2)))

    t3, sol3 = speed_check(g3_solve, cube, g)
    print("Time to G3:", t3)
    print(scramble_num_to_str(sol3), '({} moves)'.format(len(sol3)))

    t4, sol4 = speed_check(g4_solve, cube, g)
    print("Time to G4:", t4)
    print(scramble_num_to_str(sol4), '({} moves)'.format(len(sol4)))

    total = t1 + t2 + t3 + t4
    final = sol1 + sol2 + sol3 + sol4

    print()
    print("Total time:", total)
    print('Final solution:', scramble_num_to_str(final), '({} moves)'.format(len(final)))


def test_full(cube):
    t0 = time.time()
    ans = full_solve(cube)
    t1 = time.time()
    total = t1 - t0
    final = scramble_num_to_str(ans)
    print('Total Time:', total)
    print('Final Solution:', final)


if __name__ == '__main__':
    cube = FastCube()
    s = input('Scramble: ')
    s = scramble_str_to_num(s)
    scrambler(cube, s)

    mode = input('Mode: ')

    if mode == 'full':
        test_full(cube)
    if mode == '4':
        test_4(cube)
    # speed_check(rta, cube)

    # print(cube.ps)
    # print(cube.ops)

# Test scramble: F' B R L U L' R2 U' D' R' F2 U2 L2 U' F2 U' B U' D' L
