from FastCube import *
from G1 import *
from G2 import *
from G3 import *
from G4 import *
import time


def speed_check(f, *args):
    t0 = time.time()
    f(*args)
    t1 = time.time()
    print("Time:", t1 - t0)
    return t1 - t0


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


if __name__ == '__main__':
    cube = FastCube()
    # speed_check(rta, cube)
    s = input('Scramble: ')
    s = scramble_str_to_num(s)
    scrambler(cube, s)
    # print(cube)

    total = 0
    final = ''

    sol1 = []
    total += speed_check(g1_id_dfs, cube, 0, sol1)
    final += scramble_num_to_str(sol1)
    print(scramble_num_to_str(sol1))
    # print(cube)

    sol2 = []
    total += speed_check(g2_id_dfs, cube, 0, sol2)
    final += scramble_num_to_str(sol2)
    print(scramble_num_to_str(sol2))
    # print(cube)

    sol3= []
    total += speed_check(g3_id_dfs, cube, 0, sol3)
    final += scramble_num_to_str(sol3)
    print(scramble_num_to_str(sol3))
    # print(cube)

    sol4 = []
    total += speed_check(g4_id_dfs, cube, 0, sol4)
    final += scramble_num_to_str(sol4)
    print(scramble_num_to_str(sol4))
    # print(cube)

    print()
    print('Total Time:', total)
    print('Final Solution:', final)


# Test scramble: F' B R L U L' R2 U' D' R' F2 U2 L2 U' F2 U' B U' D' L
