# layer by layer cube object

from cubie import *
from moves import *

class cube:
    def __init__(self):
        # initiate the top, middle, and bottom layers
        self.pieces=[]
        for i in range(3):
            self.pieces.append([])
            for j in range(3):
                self.pieces[-1].append(3*[0])

        # populate the layers with cubies
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

    # prints the cube in a flat format. See the cubie class for color specifications.
    def __str__(self):
        ans=''

        # top face
        top = [[self.pieces[0][i][j].top for j in range(3)] for i in range(3)]
        for i in range(3):
            ans += 8*' ' + ' '.join(top[i]) + '\n'
        ans+='\n'

        # left face
        left = [[self.pieces[i][j][0].left for j in range(3)] for i in range(3)]

        # front face
        front = [[self.pieces[i][2][j].front for j in range(3)] for i in range(3)]

        # right face
        right = [[self.pieces[i][j][2].right for j in range(2,-1,-1)] for i in range(3)]

        # back face
        back = [[self.pieces[i][0][j].back for j in range(2,-1,-1)] for i in range(3)]

        for i in range(3):
            ans += ' '.join(left[i]) + '   ' + ' '.join(front[i]) + '   ' + ' '.join(right[i]) + '   ' + ' '.join(back[i]) + '\n'
        ans+='\n'

        # bottom face
        bottom = [[self.pieces[2][i][j].bottom for j in range(3)] for i in range(2,-1,-1)]
        for i in range(3):
            ans += 8*' ' + ' '.join(bottom[i]) + '\n'
        return ans