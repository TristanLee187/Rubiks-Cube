from moves import *
from cube import *
from random import choice, random
from sys import argv

# generate a random scramble of length n, with the following specifications:
# 1) No two consecutive moves will rotate the same face, i.e., the segment "R R" and "U U2" could not
# appear.
# 2) For any rotation axis, the length of a contiguous segment of moves in the scramble that rotate
# about that axis is at most 2. For example, R and L moves (as well as their prime and 180 degree
# turn versions) both rotate about the x-axis. Therefore, the segment "R L" and "R2 L'" could appear,
# but "R L R" and "L' R2 L" could not.
# 3) For any point in the scramble, of the moves allowed by teh above two rules, each will be chosen with
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

# apply a scramble (in the form of an array of strings) to the given cube.
def scrambler(cube,s):
    for move in s:
        if move=='R':
            R(cube,True)
        elif move=='R\'':
            R(cube,False)
        elif move=='R2':
            for i in range(2):
                R(cube,True)
        elif move=='L':
            L(cube,True)
        elif move=='L\'':
            L(cube,False)
        elif move=='L2':
            for i in range(2):
                L(cube,True)
        elif move == 'U':
            U(cube, True)
        elif move == 'U\'':
            U(cube, False)
        elif move == 'U2':
            for i in range(2):
                U(cube, True)
        elif move=='D':
            D(cube,True)
        elif move=='D\'':
            D(cube,False)
        elif move=='D2':
            for i in range(2):
                D(cube,True)
        elif move=='F':
            F(cube,True)
        elif move=='F\'':
            F(cube,False)
        elif move=='F2':
            for i in range(2):
                F(cube,True)
        elif move=='B':
            B(cube,True)
        elif move=='B\'':
            B(cube,False)
        elif move=='B2':
            for i in range(2):
                B(cube,True)

# testing
cube = cube()
s = gen_scramble(int(argv[1]))
scrambler(cube,s)
print()
print("Scramble:",*s)
print()
print(cube)