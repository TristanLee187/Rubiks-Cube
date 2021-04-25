import pygame
from Logic import logic
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import sin, cos, ceil, radians

pygame.init()

DISPLAY = (800, 600)
WIN = pygame.display.set_mode(DISPLAY, DOUBLEBUF | OPENGL)

GREY = (200 / 255, 200 / 255, 200 / 255)
WHITE = (1, 1, 1)
YELLOW = (1, 1, 0)
RED = (1, 0, 0)
ORANGE = (1, 135 / 255, 0)
BLUE = (0, 0, 1)
GREEN = (0, 200 / 255, 0)
BLACK = (0, 0, 0)
X_ROTATE = 0
Y_ROTATE = 0
Z_ROTATE = 0

CUBE = logic.Cube()

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
    (4, 5, 7, 6)   # front
)


def strColorToTuple(color):
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


def round_square3(points, face, color, l, radius, res, shift):
    cx, cy, cz = [sum([points[i][j] for i in range(4)])/4 for j in range(3)]
    if face==0:
        cz-=shift
    if face==1:
        cx-=shift
    if face==2:
        cx+=shift
    if face==3:
        cy+=shift
    if face==4:
        cy-=shift
    if face==5:
        cz+=shift
    cd = l/2-radius
    tl = (-cd, cd)
    tr = (cd, cd)
    bl = (-cd, -cd)
    br = (cd, -cd)
    glColor3fv(color)
    corners=[]
    corners2=[]
    if face==0 or face==5:
        add=[tr, br, bl, tl]
        angle = 90
        for quarter in range(4):
            glBegin(GL_TRIANGLE_FAN)
            nx, ny = cx+add[quarter][0], cy+add[quarter][1]
            glVertex3fv((nx, ny, cz))
            for i in range(ceil(res/4)+1):
                glVertex3fv(
                    ((nx + (radius * cos(radians(angle)))), (ny + (radius * sin(radians(angle)))), cz)
                )
                angle-=360/res
            angle+=360/res
            glEnd()
        corners = [
            (cx-cd, cy+l/2, cz),
            (cx+cd, cy+l/2, cz),
            (cx+cd, cy-l / 2, cz),
            (cx-cd, cy-l/2, cz),
        ]
        corners2 = [
            (cx-l/2, cy+cd, cz),
            (cx+l / 2, cy+cd, cz),
            (cx+l/2, cy-cd, cz),
            (cx-l/2, cy-cd, cz)
        ]
    elif face==1 or face==2:
        add=[tr, br, bl, tl]
        angle = 0
        for quarter in range(4):
            glBegin(GL_TRIANGLE_FAN)
            ny, nz = cy+add[quarter][0], cz+add[quarter][1]
            glVertex3fv((cx, ny, nz))
            for i in range(ceil(res/4)+1):
                glVertex3fv(
                    (cx, (ny + (radius * sin(radians(angle)))), (nz + (radius * cos(radians(angle)))))
                )
                angle+=360/res
            angle-=360/res
            glEnd()
        corners = [
            (cx, cy+cd, cz+l/2),
            (cx, cy+cd, cz-l/2),
            (cx, cy-cd, cz-l/2),
            (cx, cy-cd, cz+l/2)
        ]
        corners2 = [
            (cx, cy+l / 2, cz+cd),
            (cx, cy+l / 2, cz-cd),
            (cx, cy-l / 2, cz-cd),
            (cx, cy-l / 2, cz+cd)
        ]
    elif face==3 or face==4:
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
            (cx+cd, cy, cz+l / 2),
            (cx+cd, cy, cz-l / 2),
            (cx-cd, cy, cz-l / 2),
            (cx-cd, cy, cz+l / 2)
        ]
        corners2 = [
            (cx+l/2, cy, cz-cd),
            (cx-l/2, cy, cz-cd),
            (cx-l/2, cy, cz+cd),
            (cx+l/2, cy, cz+cd)
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
                glColor3fv(strColorToTuple('BL'))
                glBegin(GL_QUADS)
                for vertex in surface:
                    glVertex3fv(vertices[vertex])
                glEnd()
                points = [vertices[vertex] for vertex in surface]
                round_square3(points, j, strColorToTuple(colors[j]), 1.8, 0.3, 12, 0.03)

    faces()


def cube():
    for i in range(-2, 4, 2):
        for j in range(-2, 4, 2):
            for k in range(-2, 4, 2):
                cuboid(i, j, k)

# Animation of cube moves


def right(angles):
    clock = 1 if (pygame.key.get_mods() & pygame.KMOD_SHIFT) else -1
    for angle in range(angles):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for i in range(-2, 2, 2):
            for j in range(-2, 4, 2):
                for k in range(-2, 4, 2):
                    cuboid(i, j, k)
        glRotatef(clock * angle * 90 / angles, 1, 0, 0)
        for j in range(-2, 4, 2):
            for k in range(-2, 4, 2):
                cuboid(2, j, k)
        glRotatef(-clock * angle * 90 / angles, 1, 0, 0)
        pygame.display.flip()
    logic.R(CUBE, clock == -1)


def left(angles):
    clock = -1 if (pygame.key.get_mods() & pygame.KMOD_SHIFT) else 1
    for angle in range(angles):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for i in range(0, 4, 2):
            for j in range(-2, 4, 2):
                for k in range(-2, 4, 2):
                    cuboid(i, j, k)
        glRotatef(clock * angle * 90 / angles, 1, 0, 0)
        for j in range(-2, 4, 2):
            for k in range(-2, 4, 2):
                cuboid(-2, j, k)
        glRotatef(-clock * angle * 90 / angles, 1, 0, 0)
        pygame.display.flip()
    logic.L(CUBE, clock == 1)


def up(angles):
    clock = 1 if (pygame.key.get_mods() & pygame.KMOD_SHIFT) else -1
    for angle in range(angles):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for i in range(-2, 4, 2):
            for j in range(-2, 2, 2):
                for k in range(-2, 4, 2):
                    cuboid(i, j, k)
        glRotatef(clock * angle * 90 / angles, 0, 1, 0)
        for i in range(-2, 4, 2):
            for k in range(-2, 4, 2):
                cuboid(i, 2, k)
        glRotatef(-clock * angle * 90 / angles, 0, 1, 0)
        pygame.display.flip()
    logic.U(CUBE, clock == -1)


def down(angles):
    clock = -1 if (pygame.key.get_mods() & pygame.KMOD_SHIFT) else 1
    for angle in range(angles):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for i in range(-2, 4, 2):
            for j in range(0, 4, 2):
                for k in range(-2, 4, 2):
                    cuboid(i, j, k)
        glRotatef(clock * angle * 90 / angles, 0, 1, 0)
        for i in range(-2, 4, 2):
            for k in range(-2, 4, 2):
                cuboid(i, -2, k)
        glRotatef(-clock * angle * 90 / angles, 0, 1, 0)
        pygame.display.flip()
    logic.D(CUBE, clock == 1)


def front(angles):
    clock = 1 if (pygame.key.get_mods() & pygame.KMOD_SHIFT) else -1
    for angle in range(angles):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for i in range(-2, 4, 2):
            for j in range(-2, 4, 2):
                for k in range(-2, 2, 2):
                    cuboid(i, j, k)
        glRotatef(clock * angle * 90 / angles, 0, 0, 1)
        for i in range(-2, 4, 2):
            for j in range(-2, 4, 2):
                cuboid(i, j, 2)
        glRotatef(-clock * angle * 90 / angles, 0, 0, 1)
        pygame.display.flip()
    logic.F(CUBE, clock == -1)


def back(angles):
    clock = -1 if (pygame.key.get_mods() & pygame.KMOD_SHIFT) else 1
    for angle in range(angles):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for i in range(-2, 4, 2):
            for j in range(-2, 4, 2):
                for k in range(0, 4, 2):
                    cuboid(i, j, k)
        glRotatef(clock * angle * 90 / angles, 0, 0, 1)
        for i in range(-2, 4, 2):
            for j in range(-2, 4, 2):
                cuboid(i, j, -2)
        glRotatef(-clock * angle * 90 / angles, 0, 0, 1)
        pygame.display.flip()
    logic.B(CUBE, clock == 1)


def moves(angles):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        right(angles)
    elif keys[pygame.K_l]:
        left(angles)
    elif keys[pygame.K_u]:
        up(angles)
    elif keys[pygame.K_d]:
        down(angles)
    elif keys[pygame.K_f]:
        front(angles)
    elif keys[pygame.K_b]:
        back(angles)
    pass


# end of animation of cube moves


def rotate():
    global X_ROTATE, Y_ROTATE
    keys = pygame.key.get_pressed()
    if keys[pygame.K_x]:
        glRotatef(2, 1, 0, 0)
    elif keys[pygame.K_y]:
        glRotatef(2, 0, 1, 0)
    elif keys[pygame.K_z]:
        glRotatef(2, 0, 0, 1)


def main():
    glClearColor(200 / 255, 200 / 255, 200 / 255, 0)
    gluPerspective(45, (DISPLAY[0] / DISPLAY[1]), 0.1, 50.0)
    glTranslatef(0, 0, -15)
    glEnable(GL_DEPTH_TEST)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        rotate()
        cube()
        moves(20)
        pygame.display.flip()


main()
