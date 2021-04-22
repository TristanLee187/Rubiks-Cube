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
        glBegin(GL_QUADS)
        for j in range(6):
            surface = surfaces[j]
            if colors[j] != 'BL':
                glColor3fv(strColorToTuple(colors[j]))
                for vertex in surface:
                    glVertex3fv(vertices[vertex])
        glEnd()

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
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        glRotatef(2, -1, 0, 0)
    elif keys[pygame.K_DOWN]:
        glRotatef(2, 1, 0, 0)
    elif keys[pygame.K_LEFT]:
        glRotatef(2, 0, 1, 0)
    elif keys[pygame.K_RIGHT]:
        glRotatef(2, 0, -1, 0)


def main():
    pygame.init()
    display = (800, 600)
    WIN = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0, 0, -15)
    glEnable(GL_CULL_FACE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        cube()
        rotate()
        moves(30)
        pygame.display.flip()
        pygame.time.wait(10)


main()
