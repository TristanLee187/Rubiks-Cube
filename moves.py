# file containing each of the moves
# Each face specific function follows the following format:
# 1) create a temporary face to be changed, then reassigned to the cube object.
#    temporary faces are created as if they we being viewed head on.
# 2) rotate each cubie in the temp face along one of their own central axes
# 3) rotate each face as a whole
# 4) reassign the values in the temp face to the corresponding places in the main cube
# See the R method for in line details


# returns a clockwise rotation of a face if "clock" is True, a counterclockwise rotation otherwise.
def rotate(face,clock):
    if clock:
        return [[face[i][j] for i in range(2, -1, -1)] for j in range(3)]
    return [[face[i][j] for i in range(3)] for j in range(2,-1,-1)]

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