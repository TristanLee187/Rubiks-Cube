import pygame
from Logic import logic
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import sin, cos, ceil, radians
from subprocess import run
import matrix

pygame.init()

WIDTH = 800
HEIGHT = 600
DISPLAY = (WIDTH, HEIGHT)
WIN = pygame.display.set_mode(DISPLAY, DOUBLEBUF | OPENGL)
FPS = 60
GREY = (200 / 255, 200 / 255, 200 / 255)
WHITE = (1, 1, 1)
YELLOW = (1, 1, 0)
RED = (1, 0, 0)
ORANGE = (1, 135 / 255, 0)
BLUE = (0, 0, 1)
GREEN = (0, 200 / 255, 0)
BLACK = (0, 0, 0)
ANGLES = 15
CUBE = logic.Cube()
SCRAMBLE_LENGTH = 20

X_AXIS = [[1, 0, 0, 0]]
Y_AXIS = [[0, 1, 0, 0]]

edges = (
    (0, 1), (0, 3), (0, 4),
    (2, 1), (2, 3), (2, 7),
    (6, 3), (6, 4), (6, 7),
    (5, 1), (5, 4), (5, 7)
)
surfaces = (
    (3, 2, 1, 0),  # back
    (6, 7, 2, 3),  # left
    (0, 1, 5, 4),  # right
    (2, 7, 5, 1),  # top
    (6, 3, 0, 4),  # bottom
    (4, 5, 7, 6)  # front
)


def str_color_to_tuple(color):
    if color == 'BL':
        return BLACK
    if color == 'R':
        return RED
    if color == 'B':
        return BLUE
    if color == 'O':
        return ORANGE
    if color == 'W':
        return WHITE
    if color == 'G':
        return GREEN
    if color == 'Y':
        return YELLOW


def round_square3(points, face, color, length, radius, res, shift):
    cx, cy, cz = [sum([points[i][j] for i in range(4)]) / 4 for j in range(3)]
    if face == 0:
        cz -= shift
    if face == 1:
        cx -= shift
    if face == 2:
        cx += shift
    if face == 3:
        cy += shift
    if face == 4:
        cy -= shift
    if face == 5:
        cz += shift
    cd = length / 2 - radius
    tl = (-cd, cd)
    tr = (cd, cd)
    bl = (-cd, -cd)
    br = (cd, -cd)
    glColor3fv(color)
    corners = []
    corners2 = []
    if face == 0 or face == 5:
        add = [tr, br, bl, tl]
        angle = 90
        for quarter in range(4):
            glBegin(GL_TRIANGLE_FAN)
            nx, ny = cx + add[quarter][0], cy + add[quarter][1]
            glVertex3fv((nx, ny, cz))
            for i in range(ceil(res / 4) + 1):
                glVertex3fv(
                    ((nx + (radius * cos(radians(angle)))), (ny + (radius * sin(radians(angle)))), cz)
                )
                angle -= 360 / res
            angle += 360 / res
            glEnd()
        corners = [
            (cx - cd, cy + length / 2, cz),
            (cx + cd, cy + length / 2, cz),
            (cx + cd, cy - length / 2, cz),
            (cx - cd, cy - length / 2, cz),
        ]
        corners2 = [
            (cx - length / 2, cy + cd, cz),
            (cx + length / 2, cy + cd, cz),
            (cx + length / 2, cy - cd, cz),
            (cx - length / 2, cy - cd, cz)
        ]
    elif face == 1 or face == 2:
        add = [tr, br, bl, tl]
        angle = 0
        for quarter in range(4):
            glBegin(GL_TRIANGLE_FAN)
            ny, nz = cy + add[quarter][0], cz + add[quarter][1]
            glVertex3fv((cx, ny, nz))
            for i in range(ceil(res / 4) + 1):
                glVertex3fv(
                    (cx, (ny + (radius * sin(radians(angle)))), (nz + (radius * cos(radians(angle)))))
                )
                angle += 360 / res
            angle -= 360 / res
            glEnd()
        corners = [
            (cx, cy + cd, cz + length / 2),
            (cx, cy + cd, cz - length / 2),
            (cx, cy - cd, cz - length / 2),
            (cx, cy - cd, cz + length / 2)
        ]
        corners2 = [
            (cx, cy + length / 2, cz + cd),
            (cx, cy + length / 2, cz - cd),
            (cx, cy - length / 2, cz - cd),
            (cx, cy - length / 2, cz + cd)
        ]
    elif face == 3 or face == 4:
        add = [tr, br, bl, tl]
        angle = 0
        for quarter in range(4):
            glBegin(GL_TRIANGLE_FAN)
            nx, nz = cx + add[quarter][0], cz + add[quarter][1]
            glVertex3fv((nx, cy, nz))
            for i in range(ceil(res / 4) + 1):
                glVertex3fv(
                    ((nx + (radius * sin(radians(angle)))), cy, (nz + (radius * cos(radians(angle)))))
                )
                angle += 360 / res
            angle -= 360 / res
            glEnd()
        corners = [
            (cx + cd, cy, cz + length / 2),
            (cx + cd, cy, cz - length / 2),
            (cx - cd, cy, cz - length / 2),
            (cx - cd, cy, cz + length / 2)
        ]
        corners2 = [
            (cx + length / 2, cy, cz - cd),
            (cx - length / 2, cy, cz - cd),
            (cx - length / 2, cy, cz + cd),
            (cx + length / 2, cy, cz + cd)
        ]
    glBegin(GL_QUADS)
    for corner in corners:
        glVertex3fv(corner)
    glEnd()
    glBegin(GL_QUADS)
    for corner in corners2:
        glVertex3fv(corner)
    glEnd()


def cuboid(x, y, z):
    vertices = [
        [1, -1, -1], [1, 1, -1],
        [-1, 1, -1], [-1, -1, -1],
        [1, -1, 1], [1, 1, 1],
        [-1, -1, 1], [-1, 1, 1]
    ]
    for i in range(len(vertices)):
        vertices[i] = [vertices[i][j] + [x, y, z][j] for j in range(3)]

    # wireframe, for debugging
    def wireframe():
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()

    # faces
    def faces():
        xc, yc, zc = -y // 2 + 1, z // 2 + 1, x // 2 + 1
        cubie = CUBE.pieces[xc][yc][zc]
        colors = [cubie.back, cubie.left, cubie.right, cubie.top, cubie.bottom, cubie.front]
        for j in range(6):
            surface = surfaces[j]
            if colors[j] != 'BL':
                glColor3fv(str_color_to_tuple('BL'))
                glBegin(GL_QUADS)
                for vertex in surface:
                    glVertex3fv(vertices[vertex])
                glEnd()
                points = [vertices[vertex] for vertex in surface]
                round_square3(points, j, str_color_to_tuple(colors[j]), 1.8, 0.4, 12, 0.03)

    faces()


def cube():
    for i in range(-2, 4, 2):
        for j in range(-2, 4, 2):
            for k in range(-2, 4, 2):
                cuboid(i, j, k)


# Animation of cube moves


def R(clock):
    for angle in range(ANGLES + 1):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for i in range(-2, 2, 2):
            for j in range(-2, 4, 2):
                for k in range(-2, 4, 2):
                    cuboid(i, j, k)
        glRotatef(clock * angle * 90 / ANGLES, 1, 0, 0)
        for j in range(-2, 4, 2):
            for k in range(-2, 4, 2):
                cuboid(2, j, k)
        glRotatef(-clock * angle * 90 / ANGLES, 1, 0, 0)
        pygame.display.flip()
    logic.R(CUBE, clock == -1)


def L(clock):
    for angle in range(ANGLES + 1):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for i in range(0, 4, 2):
            for j in range(-2, 4, 2):
                for k in range(-2, 4, 2):
                    cuboid(i, j, k)
        glRotatef(-clock * angle * 90 / ANGLES, 1, 0, 0)
        for j in range(-2, 4, 2):
            for k in range(-2, 4, 2):
                cuboid(-2, j, k)
        glRotatef(clock * angle * 90 / ANGLES, 1, 0, 0)
        pygame.display.flip()
    logic.L(CUBE, clock == -1)


def U(clock):
    for angle in range(ANGLES + 1):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for i in range(-2, 4, 2):
            for j in range(-2, 2, 2):
                for k in range(-2, 4, 2):
                    cuboid(i, j, k)
        glRotatef(clock * angle * 90 / ANGLES, 0, 1, 0)
        for i in range(-2, 4, 2):
            for k in range(-2, 4, 2):
                cuboid(i, 2, k)
        glRotatef(-clock * angle * 90 / ANGLES, 0, 1, 0)
        pygame.display.flip()
    logic.U(CUBE, clock == -1)


def D(clock):
    for angle in range(ANGLES + 1):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for i in range(-2, 4, 2):
            for j in range(0, 4, 2):
                for k in range(-2, 4, 2):
                    cuboid(i, j, k)
        glRotatef(-clock * angle * 90 / ANGLES, 0, 1, 0)
        for i in range(-2, 4, 2):
            for k in range(-2, 4, 2):
                cuboid(i, -2, k)
        glRotatef(clock * angle * 90 / ANGLES, 0, 1, 0)
        pygame.display.flip()
    logic.D(CUBE, clock == -1)


def F(clock):
    for angle in range(ANGLES + 1):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for i in range(-2, 4, 2):
            for j in range(-2, 4, 2):
                for k in range(-2, 2, 2):
                    cuboid(i, j, k)
        glRotatef(clock * angle * 90 / ANGLES, 0, 0, 1)
        for i in range(-2, 4, 2):
            for j in range(-2, 4, 2):
                cuboid(i, j, 2)
        glRotatef(-clock * angle * 90 / ANGLES, 0, 0, 1)
        pygame.display.flip()
    logic.F(CUBE, clock == -1)


def B(clock):
    for angle in range(ANGLES + 1):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for i in range(-2, 4, 2):
            for j in range(-2, 4, 2):
                for k in range(0, 4, 2):
                    cuboid(i, j, k)
        glRotatef(-clock * angle * 90 / ANGLES, 0, 0, 1)
        for i in range(-2, 4, 2):
            for j in range(-2, 4, 2):
                cuboid(i, j, -2)
        glRotatef(clock * angle * 90 / ANGLES, 0, 0, 1)
        pygame.display.flip()
    logic.B(CUBE, clock == -1)


# end of animation of cube moves


def scrambler_3d(s):
    # rotate_head()
    moves = 'RLUDFB'
    for move in s:
        if move[0] in moves:
            if len(move) == 1:
                eval(move + '(-1)')
            elif len(move) == 2 and move[-1] == '\'':
                eval(move[0] + '(1)')
            elif move[-1] == '2':
                eval(move[0] + '(-1)')
                eval(move[0] + '(-1)')
            else:
                print('Invalid move found:', move)
                return
        else:
            print('Invalid move found:', move)
            return
    # rotate_tail()


def handle_keys():
    keys = pygame.key.get_pressed()
    clock = '\'' if (pygame.key.get_mods() & pygame.KMOD_SHIFT) else ''
    scramble = []
    if keys[pygame.K_r]:
        scramble.append('R' + clock)
    elif keys[pygame.K_l]:
        scramble.append('L' + clock)
    elif keys[pygame.K_u]:
        scramble.append('U' + clock)
    elif keys[pygame.K_d]:
        scramble.append('D' + clock)
    elif keys[pygame.K_f]:
        scramble.append('F' + clock)
    elif keys[pygame.K_b]:
        scramble.append('B' + clock)
    elif keys[pygame.K_s]:
        scramble += logic.gen_scramble(SCRAMBLE_LENGTH)
        print("Scramble:", *scramble)
    elif keys[pygame.K_SPACE]:
        print('Solving...')
        sol = run(['pypy3', 'Solver/solver.py', CUBE.__str__()], capture_output=True)
        sol = sol.stdout.decode('utf-8').strip()
        print('Solution: ' + sol)
        scramble += sol.split()
    scrambler_3d(scramble)


def rotate(axis, mul):
    if axis:
        glRotatef(mul, *X_AXIS[0][:-1])
        matrix.matrix_mult(matrix.rotation_matrix(radians(mul), X_AXIS[0][:-1]), Y_AXIS)
    else:
        glRotatef(mul, *Y_AXIS[0][:-1])
        matrix.matrix_mult(matrix.rotation_matrix(radians(mul), Y_AXIS[0][:-1]), X_AXIS)


def rotate_keys():
    keys = pygame.key.get_pressed()
    clock = 1 if (pygame.key.get_mods() & pygame.KMOD_SHIFT) else -1
    if keys[pygame.K_x]:
        rotate(True, 2*clock)
    if keys[pygame.K_y]:
        rotate(False, 2*clock)


def mouse_movement(x, y, drag):
    if drag:
        rotate(True, x/3.5)
        rotate(False, y/3.5)


def main():
    glClearColor(*GREY, 0)
    gluPerspective(45, (WIDTH / HEIGHT), 0.1, 50.0)
    glTranslatef(0, 0, -15)
    glEnable(GL_DEPTH_TEST)
    drag = False

    clock = pygame.time.Clock()
    while True:
        y, x = pygame.mouse.get_rel()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                drag=True
            elif event.type == pygame.MOUSEBUTTONUP:
                drag = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_movement(x, y, drag)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        rotate_keys()
        cube()
        handle_keys()
        pygame.display.flip()
        clock.tick(FPS)


main()
