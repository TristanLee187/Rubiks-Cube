from subprocess import run, Popen
from Logic import logic
import time

s = logic.gen_scramble(20)
print('Scramble:', *s)

# PyPy3 time
print("PyPy3")
cube = logic.Cube()
logic.scrambler(cube, s)
t0 = time.time()
sol = run(['pypy3', 'Solver/solver.py', cube.__str__()], capture_output=True)
t1 = time.time()
sol = sol.stdout.decode('utf-8').strip()
print('Solution: ' + sol)
print("Time:", t1-t0, "seconds")

# CPP time
print("C++")
cube = logic.Cube()
logic.scrambler(cube, s)
t0 = time.time()
sol = run(['CPP_Solver/solver.out', *cube.__str__().split()], capture_output=True)
t1 = time.time()
sol = sol.stdout.decode('utf-8').strip()
print('Solution: ' + sol)
print("Time:", t1-t0, "seconds")
