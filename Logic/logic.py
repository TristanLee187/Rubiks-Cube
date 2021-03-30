# single logic file containing the contents of all the other files
# in the Logic package

############################################################################
# Cube class

class Cube:
    def __init__(self):
        # initiate the top, middle, and bottom layers
        self.pieces = []
        for i in range(3):
            self.pieces.append([])
            for j in range(3):
                self.pieces[-1].append(3 * [0])

        # populate the layers with cubies
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    colors = 6 * ['BL']
                    # right side
                    if k == 2:
                        colors[0] = 'R'
                    # left side
                    if k == 0:
                        colors[1] = 'O'
                    # top side
                    if i == 0:
                        colors[2] = 'W'
                    # bottom side
                    if i == 2:
                        colors[3] = 'Y'
                    # front side
                    if j == 2:
                        colors[4] = 'G'
                    # back side
                    if j == 0:
                        colors[5] = 'B'
                    self.pieces[i][j][k] = cubie(colors)

    # prints the cube in a flat format. See the cubie class for color specifications.
    def __str__(self):
        ans = ''

        # top face
        top = [[self.pieces[0][i][j].top for j in range(3)] for i in range(3)]
        for i in range(3):
            ans += 8 * ' ' + ' '.join(top[i]) + '\n'
        ans += '\n'

        # left face
        left = [[self.pieces[i][j][0].left for j in range(3)] for i in range(3)]

        # front face
        front = [[self.pieces[i][2][j].front for j in range(3)] for i in range(3)]

        # right face
        right = [[self.pieces[i][j][2].right for j in range(2, -1, -1)] for i in range(3)]

        # back face
        back = [[self.pieces[i][0][j].back for j in range(2, -1, -1)] for i in range(3)]

        for i in range(3):
            ans += ' '.join(left[i]) + '   ' + ' '.join(front[i]) + '   ' + ' '.join(right[i]) + '   ' + ' '.join(
                back[i]) + '\n'
        ans += '\n'

        # bottom face
        bottom = [[self.pieces[2][i][j].bottom for j in range(3)] for i in range(2, -1, -1)]
        for i in range(3):
            ans += 8 * ' ' + ' '.join(bottom[i]) + '\n'
        return ans


############################################################################
# cubie class

class cubie:
    # treat each cubie as a small cube with 6 faces; faces of the cubie that one wouldn't normally see
    # are given the color Black or 'BL'. The other colors are:
    # 'W': White
    # 'Y': Yellow
    # 'R': Red
    # 'O': Orange
    # 'B': Blue
    # 'G': Green

    def __init__(self, colors):
        self.right = colors[0]
        self.left = colors[1]
        self.top = colors[2]
        self.bottom = colors[3]
        self.front = colors[4]
        self.back = colors[5]

    # general rotate method, which calls on axis specific methods and passing along a boolean "clock";
    # this represents a clockwise turn if True and counterclockwise if False
    def rotate(self, axis, clock):
        if axis == 'x':
            self.rotate_x(clock)
        elif axis == 'y':
            self.rotate_y(clock)
        else:
            self.rotate_z(clock)

    def rotate_x(self, clock):
        if clock:
            self.top, self.front, self.bottom, self.back = self.front, self.bottom, self.back, self.top
        else:
            self.top, self.front, self.bottom, self.back = self.back, self.top, self.front, self.bottom

    def rotate_y(self, clock):
        if clock:
            self.right, self.front, self.left, self.back = self.back, self.right, self.front, self.left
        else:
            self.right, self.front, self.left, self.back = self.front, self.left, self.back, self.right

    def rotate_z(self, clock):
        if clock:
            self.top, self.right, self.bottom, self.left = self.left, self.top, self.right, self.bottom
        else:
            self.top, self.right, self.bottom, self.left = self.right, self.bottom, self.left, self.top

    def __str__(self):
        ans = ''
        ans += 'right: ' + self.right + '\n'
        ans += 'left: ' + self.left + '\n'
        ans += 'top: ' + self.top + '\n'
        ans += 'bottom: ' + self.bottom + '\n'
        ans += 'front: ' + self.front + '\n'
        ans += 'back: ' + self.back + '\n'
        return ans


############################################################################
# moves

def rotate(face, clock):
    if clock:
        return [[face[i][j] for i in range(2, -1, -1)] for j in range(3)]
    return [[face[i][j] for i in range(3)] for j in range(2, -1, -1)]


def R(cube, clock):
    # create the temp face
    tempface = [[cube.pieces[i][j][2] for j in range(2, -1, -1)] for i in range(3)]

    # rotate each cubie
    for i in range(3):
        for j in range(3):
            tempface[i][j].rotate('x', clock)

    # rotate the whole face
    newface = rotate(tempface, clock)

    # reassign
    for i in range(3):
        for j in range(3):
            cube.pieces[i][2 - j][2] = newface[i][j]


def L(cube, clock):
    tempface = [[cube.pieces[i][j][0] for j in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            tempface[i][j].rotate('x', not clock)
    newface = rotate(tempface, clock)
    for i in range(3):
        for j in range(3):
            cube.pieces[i][j][0] = newface[i][j]


def U(cube, clock):
    tempface = [[cube.pieces[0][i][j] for j in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            tempface[i][j].rotate('y', clock)
    newface = rotate(tempface, clock)
    for i in range(3):
        for j in range(3):
            cube.pieces[0][i][j] = newface[i][j]


def D(cube, clock):
    tempface = [[cube.pieces[2][i][j] for j in range(3)] for i in range(2, -1, -1)]
    for i in range(3):
        for j in range(3):
            tempface[i][j].rotate('y', not clock)
    newface = rotate(tempface, clock)
    for i in range(3):
        for j in range(3):
            cube.pieces[2][2 - i][j] = newface[i][j]


def F(cube, clock):
    tempface = [[cube.pieces[i][2][j] for j in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            tempface[i][j].rotate('z', clock)
    newface = rotate(tempface, clock)
    for i in range(3):
        for j in range(3):
            cube.pieces[i][2][j] = newface[i][j]


def B(cube, clock):
    tempface = [[cube.pieces[i][0][j] for j in range(2, -1, -1)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            tempface[i][j].rotate('z', not clock)
    newface = rotate(tempface, clock)
    for i in range(3):
        for j in range(3):
            cube.pieces[i][0][2 - j] = newface[i][j]


def M(cube, clock):
    tempface = [[cube.pieces[i][j][1] for j in range(2, -1, -1)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            tempface[i][j].rotate('x', not clock)
    newface = rotate(tempface, not clock)
    for i in range(3):
        for j in range(3):
            cube.pieces[i][2 - j][1] = newface[i][j]


def E(cube, clock):
    tempface = [[cube.pieces[1][i][j] for j in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            tempface[i][j].rotate('y', not clock)
    newface = rotate(tempface, not clock)
    for i in range(3):
        for j in range(3):
            cube.pieces[1][i][j] = newface[i][j]


def S(cube, clock):
    tempface = [[cube.pieces[i][1][j] for j in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            tempface[i][j].rotate('z', clock)
    newface = rotate(tempface, clock)
    for i in range(3):
        for j in range(3):
            cube.pieces[i][1][j] = newface[i][j]


def r(cube, clock):
    R(cube, clock)
    M(cube, not clock)


def l(cube, clock):
    L(cube, clock)
    M(cube, clock)


def u(cube, clock):
    U(cube, clock)
    E(cube, not clock)


def d(cube, clock):
    D(cube, clock)
    E(cube, clock)


def f(cube, clock):
    F(cube, clock)
    S(cube, clock)


def b(cube, clock):
    B(cube, clock)
    S(cube, not clock)


def x(cube, clock):
    R(cube, clock)
    L(cube, not clock)
    M(cube, not clock)


def y(cube, clock):
    U(cube, clock)
    D(cube, not clock)
    E(cube, not clock)


def z(cube, clock):
    F(cube, clock)
    B(cube, not clock)
    S(cube, clock)


############################################################################
# scrambling

from random import choice, random


def gen_scramble(n):
    moves = ['R', 'L', 'U', 'D', 'F', 'B']
    scramble = []
    for i in range(n):
        poss = list(range(6))
        if len(scramble) > 0:
            poss.remove(scramble[-1])
        if len(scramble) > 1 and scramble[-1] // 2 == scramble[-2] // 2:
            poss.remove(scramble[-2])
        scramble.append(choice(poss))
    scramble = list(map(lambda x: moves[x], scramble))
    for i in range(n):
        r = random()
        if r < 1 / 3:
            scramble[i] = scramble[i] + '\''
        elif r < 2 / 3:
            scramble[i] = scramble[i] + '2'
    return scramble


def read_scramble(filename):
    try:
        file = open(filename, 'r')
    except:
        print('File not found')
        return []
    scramble = file.readline().split()
    return scramble


def see_scramble(cube, filename):
    try:
        file = open(filename, 'r')
    except:
        print('File not found')
        return
    # top face
    for i in range(3):
        row = file.readline().split()
        for j in range(3):
            cube.pieces[0][i][j].top = row[j]
    file.readline()

    # left, front, right, and back faces
    for i in range(3):
        row = file.readline().split()

        for j in range(3):
            # left face
            cube.pieces[i][j][0].left = row[j]
            # front face
            cube.pieces[i][2][j].front = row[j + 3]
            # right face
            cube.pieces[i][2 - j][2].right = row[j + 6]
            # back face
            cube.pieces[i][0][2 - j].back = row[j + 9]
    file.readline()

    # bottom face
    for i in range(3):
        row = file.readline().split()
        for j in range(3):
            cube.pieces[2][2 - i][j].bottom = row[j]


def scrambler(cube, s):
    moves = 'RLUDFBrludfbMESxyz'

    for move in s:
        if move[0] in moves:
            if len(move) == 1:
                eval(move + '(cube, True)')
            elif len(move) == 2 and move[-1] == '\'':
                eval(move[0] + '(cube, False)')
            elif move[-1] == '2':
                eval(move[0] + '(cube, True)')
                eval(move[0] + '(cube, True)')
            else:
                print('Invalid move found:', move)
                return
        else:
            print('Invalid move found:', move)
            return
