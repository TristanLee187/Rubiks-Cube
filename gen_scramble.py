from random import choice, random

def scramble(n):
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

s=scramble(20)
print(*s)
