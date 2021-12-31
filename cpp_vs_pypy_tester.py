# Script for comparing pypy3 and c++ solvers
# Takes an integer (as a command line argument) as input and runs that many random scrambles of
# length 20

from subprocess import run
from Logic import logic
from sys import argv
import time

n = int(argv[1])
py_times = []
cpp_times = []
for i in range(n):
    s = logic.gen_scramble(20)
    print('Scramble {}: '.format(i+1), *s)

    # PyPy3 time
    cube = logic.Cube()
    logic.scrambler(cube, s)
    t0 = time.time()
    pysol = run(['pypy3', 'Solver/solver.py', cube.__str__()], capture_output=True)
    t1 = time.time()
    pysol = pysol.stdout.decode('utf-8').strip()
    # print('Solution: ' + pysol)
    print("PyPy3 Time:", t1-t0, "seconds")
    py_times.append(t1-t0)

    # CPP time
    cube = logic.Cube()
    logic.scrambler(cube, s)
    t0 = time.time()
    cppsol = run(['CPP_Solver/solver.out', *cube.__str__().split()], capture_output=True)
    t1 = time.time()
    cppsol = cppsol.stdout.decode('utf-8').strip()
    # print('Solution: ' + cppsol)
    print("C++ Time:", t1-t0, "seconds")
    cpp_times.append(t1-t0)

    if pysol == cppsol:
        print("Solutions match")
        print('Solution: ' + pysol)
    else:
        print("Solutions do not match!")
        print('PyPy Solution: ' + pysol)
        print('C++ Solution: ' + cppsol)
    print()

print('Summary:')
print("Average PyPy3 time: {}".format(sum(py_times)/n))
print("Average C++ time: {}".format(sum(cpp_times)/n))
