import subprocess
s = subprocess.run(['pypy3', 'Solver/test.py'], capture_output=True)
out = s.stdout.decode('utf-8')
print(out)
