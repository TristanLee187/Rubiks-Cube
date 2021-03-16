def rotate(face,clock):
    if clock:
        return [[face[i][j] for i in range(2, -1, -1)] for j in range(3)]
    return [[face[i][j] for i in range(3)] for j in range(2,-1,-1)]

def R(cube,clock):
    tempface = [[cube.pieces[i][j][2] for j in range(2,-1,-1)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            tempface[i][j].rotate('x',clock)
    newface=rotate(tempface,clock)
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