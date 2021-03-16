from moves import *
from cube import *
from random import choice, random
from sys import argv

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


cube = cube()
s = gen_scramble(int(argv[1]))
scrambler(cube,s)
print(cube)
print(*s)