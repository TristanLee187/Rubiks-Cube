from FastCube import FastCube
from FullSolve import full_solve
from sys import argv


def scramble_num_to_str(scramble):
    ans = ''
    moves = ['U', 'F', 'R', 'B', 'L', 'D']
    for num in scramble:
        add = moves[num // 3]
        add += ['', '\'', '2'][num % 3]
        ans += add + ' '
    return ans


def solver(layout):
    cube = FastCube(layout)
    ans = full_solve(cube)
    return scramble_num_to_str(ans)


if __name__ == '__main__':
    print(solver(argv[1]))
