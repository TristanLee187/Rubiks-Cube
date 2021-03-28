# file for storing the various scrambling functions

from moves import *
from random import choice, random

# generate a random scramble of length n, with the following specifications:
# 1) No two consecutive moves will rotate the same face, i.e., the segment "R R" and "U U2" could not
# appear.
# 2) For any rotation axis, the length of a contiguous segment of moves in the scramble that rotate
# about that axis is at most 2. For example, R and L moves (as well as their prime and 180 degree
# turn versions) both rotate about the x-axis. Therefore, the segment "R L" and "R2 L'" could appear,
# but "R L R" and "L' R2 L" could not.
# 3) For any point in the scramble, of the moves allowed by the above two rules, each will be chosen with
# equal probability. For example, if the allowed moves are [R, L, U, D], each has a 1/4 chance of being chosen.
# 4) Each move has a 1/3 chance of being counterclockwise and 1/3 chance of being a 180 degree turn. Specifically,
# a move has a 1/3 chance of being counterclockwise; if it is not counterclockwise, then it has a 1/2 chance of
# being 180 degrees.
def gen_scramble(n):
    moves=['R','L','U','D','F','B']
    scramble=[]
    for i in range(n):
        poss=list(range(6))
        if len(scramble)>0:
            poss.remove(scramble[-1])
        if len(scramble)>1 and scramble[-1]//2 == scramble[-2]//2:
            poss.remove(scramble[-2])
        scramble.append(choice(poss))
    scramble=list(map(lambda x: moves[x], scramble))
    for i in range(n):
        r=random()
        if r<1/3:
            scramble[i]=scramble[i]+'\''
        elif r<2/3:
            scramble[i]=scramble[i]+'2'
    return scramble

# read the scramble from a given file.
# the scramble should be on a single line, with each move separated by white space, like the following:
# "R U L2 D'"
def read_scramble(filename):
    try:
        file = open(filename,'r')
    except:
        print('File not found')
        return []
    scramble = file.readline().split()
    return scramble

# read a scrambled cube given the flat layout of the colors on each face from a text file,
# then apply it to the given cube
def see_scramble(cube, filename):
    try:
        file = open(filename,'r')
    except:
        print('File not found')
        return
    # top face
    for i in range(3):
        row = file.readline().split()
        for j in range(3):
            cube.pieces[0][i][j].top=row[j]
    file.readline()

    # left, front, right, and back faces
    for i in range(3):
        row = file.readline().split()

        for j in range(3):
            # left face
            cube.pieces[i][j][0].left = row[j]
            # front face
            cube.pieces[i][2][j].front = row[j+3]
            # right face
            cube.pieces[i][2-j][2].right = row[j+6]
            # back face
            cube.pieces[i][0][2-j].back = row[j+9]
    file.readline()

    # bottom face
    for i in range(3):
        row = file.readline().split()
        for j in range(3):
            cube.pieces[2][2-i][j].bottom = row[j]

# apply a scramble (in the form of an array of strings) to the given cube.
def scrambler(cube,s):
    moves = 'RLUDFBrludfbMESxyz'

    for move in s:
        if move[0] in moves:
            if len(move)==1:
                eval(move+'(cube, True)')
            elif len(move)==2 and move[-1]=='\'':
                eval(move[0]+'(cube, False)')
            elif move[-1]=='2':
                eval(move[0] + '(cube, True)')
                eval(move[0] + '(cube, True)')
            else:
                print('Invalid move found:', move)
                return
        else:
            print('Invalid move found:', move)
            return
