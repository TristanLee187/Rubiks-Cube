import pygame
from Logic import logic
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

GREY = (200 / 255, 200 / 255, 200 / 255)
WHITE = (1, 1, 1)
YELLOW = (1, 1, 0)
RED = (1, 0, 0)
ORANGE = (1, 135 / 255, 0)
BLUE = (0, 0, 1)
GREEN = (0, 200 / 255, 0)
BLACK = (0, 0, 0)
CUBE = logic.Cube()

edges = ((0, 1), (0, 3), (0, 4),
         (2, 1), (2, 3), (2, 7),
         (6, 3), (6, 4), (6, 7),
         (5, 1), (5, 4), (5, 7))
surfaces = (
            (0, 1, 2, 3),  # back
            (3, 2, 7, 6),  # left
            (4, 5, 1, 0),  # right
            (1, 5, 7, 2),  # top
            (4, 0, 3, 6),  # bottom
            (6, 7, 5, 4))  # front


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


def cuboid(x, y, z):
    vertices = [
        [1, -1, -1], [1, 1, -1],
        [-1, 1, -1], [-1, -1, -1],
        [1, -1, 1], [1, 1, 1],
        [-1, -1, 1], [-1, 1, 1]
    ]
    for i in range(len(vertices)):
        vertices[i] = [vertices[i][j] + [x, y, z][j] for j in range(3)]
    xc,yc,zc = -y//2+1,z//2+1,x//2+1
    cubie = CUBE.pieces[xc][yc][zc]
    colors = [cubie.back, cubie.left, cubie.right, cubie.top, cubie.bottom, cubie.front]
    glBegin(GL_QUADS)
    for i in range(6):
        surface = surfaces[i]
        if colors[i]!='BL':
            glColor3fv(strColorToTuple(colors[i]))
            for vertex in surface:
                glVertex3fv(vertices[vertex])
    glEnd()


def cube():
    for i in range(-2, 4, 2):
        for j in range(-2, 4, 2):
            for k in range(-2, 4, 2):
                cuboid(i, j, k)


# Animation of cube moves
def right():
    clock = 1 if (pygame.key.get_mods() & pygame.KMOD_SHIFT) else -1
    for angle in range(90):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for i in range(-2, 2, 2):
            for j in range(-2, 4, 2):
                for k in range(-2, 4, 2):
                    cuboid(i, j, k)
        glRotatef(clock * angle, 1, 0, 0)
        for j in range(-2, 4, 2):
            for k in range(-2, 4, 2):
                cuboid(2, j, k)
        glRotatef(-clock * angle, 1, 0, 0)
        pygame.display.flip()
    logic.R(CUBE, clock==-1)


def left():
    clock = -1 if (pygame.key.get_mods() & pygame.KMOD_SHIFT) else 1
    for angle in range(90):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for i in range(0, 4, 2):
            for j in range(-2, 4, 2):
                for k in range(-2, 4, 2):
                    cuboid(i, j, k)
        glRotatef(clock * angle, 1, 0, 0)
        for j in range(-2, 4, 2):
            for k in range(-2, 4, 2):
                cuboid(-2, j, k)
        glRotatef(-clock * angle, 1, 0, 0)
        pygame.display.flip()
    logic.L(CUBE, clock==1)


def up():
    clock = 1 if (pygame.key.get_mods() & pygame.KMOD_SHIFT) else -1
    for angle in range(90):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for i in range(-2, 4, 2):
            for j in range(-2, 2, 2):
                for k in range(-2, 4, 2):
                    cuboid(i, j, k)
        glRotatef(clock * angle, 0, 1, 0)
        for i in range(-2, 4, 2):
            for k in range(-2, 4, 2):
                cuboid(i, 2, k)
        glRotatef(-clock * angle, 0, 1, 0)
        pygame.display.flip()
    logic.U(CUBE, clock==-1)


def down():
    clock = -1 if (pygame.key.get_mods() & pygame.KMOD_SHIFT) else 1
    for angle in range(90):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for i in range(-2, 4, 2):
            for j in range(0, 4, 2):
                for k in range(-2, 4, 2):
                    cuboid(i, j, k)
        glRotatef(clock * angle, 0, 1, 0)
        for i in range(-2, 4, 2):
            for k in range(-2, 4, 2):
                cuboid(i, -2, k)
        glRotatef(-clock * angle, 0, 1, 0)
        pygame.display.flip()
    logic.D(CUBE, clock==1)


def front():
    clock = 1 if (pygame.key.get_mods() & pygame.KMOD_SHIFT) else -1
    for angle in range(90):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for i in range(-2, 4, 2):
            for j in range(-2, 4, 2):
                for k in range(-2, 2, 2):
                    cuboid(i, j, k)
        glRotatef(clock * angle, 0, 0, 1)
        for i in range(-2, 4, 2):
            for j in range(-2, 4, 2):
                cuboid(i, j, 2)
        glRotatef(-clock * angle, 0, 0, 1)
        pygame.display.flip()
    logic.F(CUBE, clock==-1)


def back():
    clock = -1 if (pygame.key.get_mods() & pygame.KMOD_SHIFT) else 1
    for angle in range(90):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for i in range(-2, 4, 2):
            for j in range(-2, 4, 2):
                for k in range(0, 4, 2):
                    cuboid(i, j, k)
        glRotatef(clock * angle, 0, 0, 1)
        for i in range(-2, 4, 2):
            for j in range(-2, 4, 2):
                cuboid(i, j, -2)
        glRotatef(-clock * angle, 0, 0, 1)
        pygame.display.flip()
    logic.B(CUBE, clock==1)


def moves():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        right()
    elif keys[pygame.K_l]:
        left()
    elif keys[pygame.K_u]:
        up()
    elif keys[pygame.K_d]:
        down()
    elif keys[pygame.K_f]:
        front()
    elif keys[pygame.K_b]:
        back()
    pass


# end of animation of cube moves


def main():
    pygame.init()
    display = (800, 600)
    WIN = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glTranslatef(0, 0, -20)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        cube()
        moves()
        pygame.display.flip()


main()
