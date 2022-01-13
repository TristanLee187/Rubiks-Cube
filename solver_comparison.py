# Script for comparing the different solvers (pypy and c++)
# Takes an integer (as a command line argument) as input and runs that many random scrambles of
# length 20

from subprocess import run
from Logic import logic
from sys import argv
import time

n = int(argv[1])
py_times = []
cpp_fast_times = []
py_lengths = []
cpp_lengths = []
for i in range(n):
    s = logic.gen_scramble(20)
    print('Scramble {}: '.format(i + 1), *s)

    # PyPy3 Solver time
    cube = logic.Cube()
    logic.scrambler(cube, s)
    t0 = time.time()
    pysol = run(['pypy3', 'Solver/solver.py', cube.__str__()], capture_output=True)
    t1 = time.time()
    pysol = pysol.stdout.decode('utf-8').strip()
    # print('Solution: ' + pysol)
    print("PyPy3 Solver Time:", t1 - t0, "seconds")
    py_times.append(t1 - t0)
    py_lengths.append(len(pysol.split()))

    # CPP_FastSolver time
    cube = logic.Cube()
    logic.scrambler(cube, s)
    t0 = time.time()
    cppfsol = run(['CPP_FastSolver/solver.out', *cube.__str__().split()], capture_output=True)
    t1 = time.time()
    cppfsol = cppfsol.stdout.decode('utf-8').strip()
    # print('Solution: ' + cppfsol)
    print("CPP_FastSolver Time:", t1 - t0, "seconds")
    cpp_fast_times.append(t1 - t0)
    cpp_lengths.append(len(cppfsol.split()))

    print('PyPy Solution: ' + pysol)
    print('CPP_FastSolver Solution: ' + cppfsol)
    if pysol == cppfsol:
        print('Solutions match')
    else:
        print('Solutions do not match')
    print()

print('Summary:')
print("Average PyPy3 time: {}".format(sum(py_times) / n))
print("Average PyPy3 solution length: {}".format(sum(py_lengths) / n))
print("Average C++ time: {}".format(sum(cpp_fast_times) / n))
print("Average C++ solution length: {}".format(sum(cpp_lengths) / n))
