# Using this tester:
# Mass testing of the solver from FullSolve: pypy3 tester.py Tests n, where n is the number of random scrambles to test
# Single test of the solver from FullSolve: pypy3 tester.py full, then enter the scramble on the next line
# Single test of a solver using each of the individual stage files, which also shows the time taken and solution for
# each stage: pypy3 tester.py 4, then enter the scramble on the next line


from G1 import *
from G2 import *
from G3 import *
from G4 import *
from FullSolve import *
import time
from random import choice, random
from sys import argv
import cProfile


def speed_check(f, *args):
    t0 = time.time()
    ans = f(*args)
    t1 = time.time()
    return t1 - t0, ans


def rta():
    cube = FastCube()
    for i in range(10**6):
        for j in range(18):
            cube.move(j)
    return 0


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


def gen_scramble(n):
    moves = ['R', 'L', 'U', 'D', 'F', 'B']
    scramble = []
    for i in range(n):
        poss = list(range(6))
        if len(scramble) > 0:
            poss.remove(scramble[-1])
        if len(scramble) > 1 and scramble[-1] // 2 == scramble[-2] // 2:
            poss.remove(scramble[-2])
        scramble.append(choice(poss))
    scramble = list(map(lambda x: moves[x], scramble))
    for i in range(n):
        r = random()
        if r < 1 / 3:
            scramble[i] = scramble[i] + '\''
        elif r < 2 / 3:
            scramble[i] = scramble[i] + '2'
    return scramble


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
    print('Solution:', scramble_num_to_str(final), '({} moves)'.format(len(final)))

    return total, scramble_num_to_str(final)


def test_full(cube):
    t0 = time.time()
    ans = full_solve(cube)
    t1 = time.time()
    total = t1 - t0
    final = scramble_num_to_str(ans)
    print('Total Time:', total)
    print('Solution:', final, '({} moves)'.format(len(ans)))
    return total, final


def mass_testing(moves):
    tests = int(argv[2])
    times = []
    lengths = []
    for _ in range(tests):
        cube = FastCube()
        s = ' '.join(gen_scramble(20))
        print('Scramble {}:'.format(_), s)
        s = scramble_str_to_num(s)
        scrambler(cube, s)

        t, f = test_full(cube)
        print()
        times.append(t)
        lengths.append(len(f.split()))

        moves.clear()
        moves += [
            set(range(3, 18)),  # U face
            {0, 1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17},  # F face
            {0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17},  # R face
            {0, 1, 2, 6, 7, 8, 12, 13, 14, 15, 16, 17},  # B face
            {0, 1, 2, 3, 4, 5, 9, 10, 11, 15, 16, 17},  # L face
            set(range(3, 15)),  # D face
            set(range(18))  # all allowed moves starting from no moves
        ]

    print('Average time:', sum(times) / tests)
    print('Average solution length:', sum(lengths) / tests)


def debug():
    ans = speed_check(rta)
    print(ans[1])
    print(ans[0])


def main():
    mode = argv[1]
    if mode == 'debug':
        debug()
    elif mode == 'Tests':
        mass_testing(ALLOWED_MOVES)
    else:
        cube = FastCube()
        s = input('Scramble: ')
        s = scramble_str_to_num(s)
        scrambler(cube, s)
        if mode == '4':
            test_4(cube)
        if mode == 'full':
            test_full(cube)


if __name__ == '__main__':
    main()
    # cProfile.run('main()')
