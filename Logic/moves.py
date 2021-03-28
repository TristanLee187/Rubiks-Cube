# file containing each of the moves
# Supported moves include:
# 1) the 6 basic outer face turns,
# 2) each of their corresponding wide moves,
# 3) the 3 slice moves, and
# 4) the 3 cube rotations.
#
# Each outer face or slice function follows the following format:
# 1) create a temporary face to be changed, then reassigned to the cube object.
#    temporary faces are created as if they we being viewed head on.
# 2) rotate each cubie in the temp face along one of their own central axes
# 3) rotate each face as a whole
# 4) reassign the values in the temp face to the corresponding places in the main cube
# See the R method for in line details
#
# Wide moves and cube rotations use a combination of outer face turns and slices.


# returns a clockwise rotation of a face if "clock" is True, a counterclockwise rotation otherwise.
def rotate(face,clock):
    if clock:
        return [[face[i][j] for i in range(2, -1, -1)] for j in range(3)]
    return [[face[i][j] for i in range(3)] for j in range(2,-1,-1)]

# regular outer face turns

def R(cube,clock):
    # create the temp face
    tempface = [[cube.pieces[i][j][2] for j in range(2,-1,-1)] for i in range(3)]

    # rotate each cubie
    for i in range(3):
        for j in range(3):
            tempface[i][j].rotate('x',clock)

    # rotate the whole face
    newface=rotate(tempface,clock)

    # reassign
    for i in range(3):
        for j in range(3):
            cube.pieces[i][2-j][2] = newface[i][j]

def L(cube,clock):
    tempface = [[cube.pieces[i][j][0] for j in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            tempface[i][j].rotate('x', not clock)
    newface=rotate(tempface,clock)
    for i in range(3):
        for j in range(3):
            cube.pieces[i][j][0] = newface[i][j]

def U(cube,clock):
    tempface = [[cube.pieces[0][i][j] for j in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            tempface[i][j].rotate('y', clock)
    newface = rotate(tempface, clock)
    for i in range(3):
        for j in range(3):
            cube.pieces[0][i][j] = newface[i][j]

def D(cube,clock):
    tempface = [[cube.pieces[2][i][j] for j in range(3)] for i in range(2,-1,-1)]
    for i in range(3):
        for j in range(3):
            tempface[i][j].rotate('y', not clock)
    newface = rotate(tempface, clock)
    for i in range(3):
        for j in range(3):
            cube.pieces[2][2-i][j] = newface[i][j]

def F(cube,clock):
    tempface = [[cube.pieces[i][2][j] for j in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            tempface[i][j].rotate('z', clock)
    newface = rotate(tempface, clock)
    for i in range(3):
        for j in range(3):
            cube.pieces[i][2][j] = newface[i][j]

def B(cube,clock):
    tempface = [[cube.pieces[i][0][j] for j in range(2,-1,-1)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            tempface[i][j].rotate('z', not clock)
    newface = rotate(tempface, clock)
    for i in range(3):
        for j in range(3):
            cube.pieces[i][0][2-j] = newface[i][j]

# slices

def M(cube, clock):
    tempface = [[cube.pieces[i][j][1] for j in range(2,-1,-1)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            tempface[i][j].rotate('x', not clock)
    newface = rotate(tempface, not clock)
    for i in range(3):
        for j in range(3):
            cube.pieces[i][2-j][1] = newface[i][j]

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

# wide moves

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

# rotations

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
