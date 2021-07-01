from FastCube import *
from G1 import *
from G2 import *
from G3 import *
from G4 import *
from FullSolve import *
import time


def speed_check(f, *args):
    t0 = time.time()
    f(*args)
    t1 = time.time()
    print("Time:", t1 - t0)
    return t1 - t0


def rta(c):
    d = FastCube()
    s = set()
    i = 0
    while i < 10 ** 6:
        d = c.__copy__()
        if d not in s:
            s.add(d)
        i += 1


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
    t0 = time.time()
    final = ''

    sol1 = []
    speed_check(g1_id_dfs, cube, 0, sol1)
    final += scramble_num_to_str(sol1)
    print(scramble_num_to_str(sol1))
    # print(cube)

    sol2 = []
    speed_check(g2_id_dfs, cube, 0, sol2)
    final += scramble_num_to_str(sol2)
    print(scramble_num_to_str(sol2))
    # print(cube)

    sol3 = []
    speed_check(g3_id_dfs, cube, 0, sol3)
    final += scramble_num_to_str(sol3)
    print(scramble_num_to_str(sol3))
    # print(cube)

    sol4 = []
    speed_check(g4_id_dfs, cube, 0, sol4)
    final += scramble_num_to_str(sol4)
    print(scramble_num_to_str(sol4))
    # print(cube)

    total = time.time() - t0

    print()
    print('Total Time:', total)
    print('Final Solution:', final)


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

# Test scramble: F' B R L U L' R2 U' D' R' F2 U2 L2 U' F2 U' B U' D' L
# time to beat: around 21-22 sec for 4, 24-25 for full
