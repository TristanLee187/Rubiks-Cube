# layer by layer cube object

from cubie import *

class cube:
    def __init__(self):
        self.pieces=[]
        for i in range(3):
            self.pieces.append([])
            for j in range(3):
                self.pieces[-1].append(3*[0])
        # population
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    colors=6*['BL']
                    # right side
                    if k==2:
                        colors[0]='R'
                    # left side
                    if k==0:
                        colors[1]='O'
                    # top side
                    if i==0:
                        colors[2]='W'
                    # bottom side
                    if i==2:
                        colors[3]='Y'
                    # front side
                    if j==2:
                        colors[4]='G'
                    # back side
                    if j==0:
                        colors[5]='B'
                    self.pieces[i][j][k]=cubie(colors)

    def __str__(self):
        ans=''

        # top face
        top = [[self.pieces[0][i][j].top for j in range(3)] for i in range(3)]
        for i in range(3):
            ans+= 7*' ' + ' '.join(top[i]) + '\n'
        ans+='\n'

        # left face
        left = [[self.pieces[i][j][0].left for j in range(3)] for i in range(3)]

cube=cube()
print(cube)