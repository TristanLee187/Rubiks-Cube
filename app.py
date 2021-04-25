# PyGame Rubik's Cube application

from Logic import logic
import pygame
from math import sin, cos, radians

pygame.init()
pygame.display.set_caption('Rubik\'s Cube')

WIDTH = 900
HEIGHT = 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
GREY = (200, 200, 200)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 135, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
sw = 35
sw3D = 70
ew = 3
ew3D = 4
FPS = 60
FLAT_CUBE_X, FLAT_CUBE_Y = 400, (HEIGHT - (10 * ew + 9 * sw)) / 2
CUBE_3D_X, CUBE_3D_Y = 400, 150
CUBE_SWITCH = True


class button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        primeless_buttons = ['Reset', 'Scramble', '?', 'Switch']

        if self.text != '':
            font = pygame.font.SysFont('Arial Black', 30)
            text = font.render(self.text + int(pygame.key.get_mods() & pygame.KMOD_SHIFT and
                                               self.text not in primeless_buttons) * '\'', True, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x + self.width > pos[0] > self.x:
            if self.y + self.height > pos[1] > self.y:
                return True

        return False


# draw the given cube to WIN in a 3D format, showing the front, top, and right faces
def draw_3d_cube(cube, xx, yy):
    x = xx
    y = yy
    angle = 60
    si = sin(radians(angle))
    co = cos(radians(angle))
    colors = {'W': WHITE, 'Y': YELLOW, 'O': ORANGE, 'G': GREEN, 'R': RED, 'B': BLUE}
    # front face
    for i in range(3):
        for j in range(3):
            x_add = j * sw3D * si
            y_add = i * sw3D + j * sw3D * co
            color = colors[cube.pieces[i][2][j].front]
            pygame.draw.polygon(WIN, color,
                                [(x + x_add, y + y_add), (x + x_add, y + y_add + sw3D),
                                 (x + sw3D * si+x_add, y + y_add + sw3D * co + sw3D),
                                 (x + sw3D * si+x_add, y + y_add + sw3D * co)])
            pygame.draw.polygon(WIN, BLACK,
                                [(x+x_add, y + y_add), (x+x_add, y + y_add + sw3D),
                                 (x + sw3D * si+x_add, y + y_add + sw3D * co + sw3D),
                                 (x + sw3D * si+x_add, y + y_add + sw3D * co)], ew3D)
    # top face
    for i in range(3):
        for j in range(3):
            x_add = (j+i) * sw3D * si
            y_sub = (j-i) * sw3D * co
            color = colors[cube.pieces[0][2-j][i].top]
            pygame.draw.polygon(WIN, color,
                                [(x + x_add, y - y_sub), (x + x_add + sw3D*si, y-y_sub-sw3D*co),
                                 (x+x_add+2*sw3D*si, y-y_sub),
                                 (x + x_add + sw3D*si, y-y_sub+sw3D*co)])
            pygame.draw.polygon(WIN, BLACK,
                                [(x + x_add, y - y_sub),
                                 (x + x_add + sw3D * si, y - y_sub - sw3D * co),
                                 (x + x_add + 2 * sw3D * si, y - y_sub),
                                 (x + x_add + sw3D * si, y - y_sub + sw3D * co)], ew3D)

    # right face
    x += 6*sw3D*si
    for i in range(3):
        for j in range(3):
            x_sub = i * sw3D * si
            y_add = j * sw3D + i * sw3D * co
            color = colors[cube.pieces[j][i][2].right]
            pygame.draw.polygon(WIN, color,
                                [(x - x_sub, y + y_add), (x - x_sub, y + y_add + sw3D),
                                 (x - sw3D * si-x_sub, y + y_add + sw3D * co + sw3D),
                                 (x - sw3D * si-x_sub, y + y_add + sw3D * co)])
            pygame.draw.polygon(WIN, BLACK,
                                [(x-x_sub, y + y_add), (x-x_sub, y + y_add + sw3D),
                                 (x - sw3D * si-x_sub, y + y_add + sw3D * co + sw3D),
                                 (x - sw3D * si-x_sub, y + y_add + sw3D * co)], ew3D)
    pygame.display.update()


# draws the given cube to WIN in a flat layout
def draw_2d_cube(cube, x, y):
    colors = {'W': WHITE, 'Y': YELLOW, 'O': ORANGE, 'G': GREEN, 'R': RED, 'B': BLUE}
    grid = [row.split() for row in str(cube).split('\n') if row != '']
    # stickers
    for i in range(9):
        indexes = range(3, 6) if (i < 3 or i > 5) else range(12)
        for j in indexes:
            square = pygame.Rect(j * sw + ew * j + x, i * sw + ew * i + y, sw, sw)
            color = colors[grid[i][j - 3 * int(i < 3 or i > 5)]]
            pygame.draw.rect(WIN, color, square)

    # edges
    for i in range(10):
        if i < 3 or i > 6:
            edge = [3 * sw + 3 * ew + x - ew, i * sw + ew * i + y - ew, 3 * (sw + ew) + ew, ew]
        else:
            edge = [x - ew, i * sw + ew * i + y - ew, 12 * (sw + ew), ew]
        pygame.draw.rect(WIN, BLACK, edge)

    for i in range(13):
        if i < 3 or i > 6:
            edge = [i * sw + ew * i + x - ew, 3 * sw + 3 * ew + y - ew, ew, 3 * (sw + ew) + ew]
        else:
            edge = [i * sw + ew * i + x - ew, y - ew, ew, 9 * (sw + ew) + ew]
        pygame.draw.rect(WIN, BLACK, edge)
    pygame.display.update()


# general draw cube function, that calls the 2D of 3D function if CUBE_SWITCH is True or False, respectively
def draw_cube(cube):
    if CUBE_SWITCH:
        draw_2d_cube(cube, FLAT_CUBE_X, FLAT_CUBE_Y)
    else:
        draw_3d_cube(cube, CUBE_3D_X, CUBE_3D_Y)


# buttons
OFFSET_X = 30
OFFSET_Y = 30
BUTTON_COLOR = GREY
BUTTON_HOVER_COLOR = (0, 255, 255)
BUTTON_SIZE = 50
SPACE = 75

right = button(BUTTON_COLOR, OFFSET_X, OFFSET_Y, BUTTON_SIZE, BUTTON_SIZE, 'R')
left = button(BUTTON_COLOR, OFFSET_X + SPACE, OFFSET_Y, BUTTON_SIZE, BUTTON_SIZE, 'L')
mid = button(BUTTON_COLOR, OFFSET_X + 2 * SPACE, OFFSET_Y, BUTTON_SIZE, BUTTON_SIZE, 'M')
up = button(BUTTON_COLOR, OFFSET_X, OFFSET_Y + SPACE, BUTTON_SIZE, BUTTON_SIZE, 'U')
down = button(BUTTON_COLOR, OFFSET_X + SPACE, OFFSET_Y + SPACE, BUTTON_SIZE, BUTTON_SIZE, 'D')
equ = button(BUTTON_COLOR, OFFSET_X + 2 * SPACE, OFFSET_Y + SPACE, BUTTON_SIZE, BUTTON_SIZE, 'E')
front = button(BUTTON_COLOR, OFFSET_X, OFFSET_Y + 2 * SPACE, BUTTON_SIZE, BUTTON_SIZE, 'F')
back = button(BUTTON_COLOR, OFFSET_X + SPACE, OFFSET_Y + 2 * SPACE, BUTTON_SIZE, BUTTON_SIZE, 'B')
s = button(BUTTON_COLOR, OFFSET_X + 2 * SPACE, OFFSET_Y + 2 * SPACE, BUTTON_SIZE, BUTTON_SIZE, 'S')
X = button(BUTTON_COLOR, OFFSET_X, OFFSET_Y + 3 * SPACE, BUTTON_SIZE, BUTTON_SIZE, 'x')
Y = button(BUTTON_COLOR, OFFSET_X + SPACE, OFFSET_Y + 3 * SPACE, BUTTON_SIZE, BUTTON_SIZE, 'y')
Z = button(BUTTON_COLOR, OFFSET_X + 2 * SPACE, OFFSET_Y + 3 * SPACE, BUTTON_SIZE, BUTTON_SIZE, 'z')
reset = button(BUTTON_COLOR, OFFSET_X, OFFSET_Y + 4 * SPACE, 2.5 * BUTTON_SIZE, BUTTON_SIZE, 'Reset')
scramble = button(BUTTON_COLOR, OFFSET_X, OFFSET_Y + 5 * SPACE, 3.75 * BUTTON_SIZE, BUTTON_SIZE, 'Scramble')
Help = button(BUTTON_COLOR, WIDTH - BUTTON_SIZE - OFFSET_X, OFFSET_Y + 5 * SPACE, BUTTON_SIZE, BUTTON_SIZE, '?')
switch = button(BUTTON_COLOR, WIDTH - 3 * BUTTON_SIZE - OFFSET_X, OFFSET_Y, 2.5 * BUTTON_SIZE, BUTTON_SIZE, 'Switch')
buttons = [right, left, mid, up, down, equ, front, back, s, X, Y, Z, reset, scramble, Help, switch]


def help_function():
    help_text = ['Hello There! Here`s how to use this virtual Rubik`s Cube:',
                 'Clicking one of the buttons with cube notation moves performs the corresponding move.',
                 '  -Holding Shift while pressing one of these buttons performs the counterclockwise counterpart.',
                 '  -Using right click has the same effect.',
                 '  -Doing both of these simultaneously does the clockwise move (same as a regular button press).',
                 'Pressing `Reset` returns the cube to the solved state and standard orientation.',
                 'Pressing `Scramble` applies a random, 20 move scramble to the cube, and prints the scramble to',
                 '   standard output.',
                 'Pressing `Switch` switches the viewing layout of the cube; if you`re viewing it in a flat layout,',
                 '   the view changes to 3D, and vice versa.',
                 '  -For the flat layout, the top and bottom faces of the cube are in their respective places; the',
                 '      faces in the middle, from left to right, are the cube`s left, front, right, and back faces.',
                 '  -For the 3D layout, the left, top, and right faces are the cube`s front, top, and right faces']
    win2 = pygame.display.set_mode((WIDTH, HEIGHT))
    win2.fill(GREY)
    font = pygame.font.SysFont('Arial', 20)
    spacing = 30
    for i in range(len(help_text)):
        line = font.render(help_text[i], True, BLACK)
        win2.blit(line, (20, spacing * (i+1)))
    pygame.display.update()
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    win2.fill(GREY)


def setup_buttons():
    for b in buttons:
        b.draw(WIN, BLACK)
    pygame.display.update()


def handle_buttons(cube, mode, pos):
    if mode == 'press':
        for b in buttons:
            if b.isOver(pos):
                if b.text == 'Reset':
                    cube.__init__()
                elif b.text == 'Scramble':
                    scr = logic.gen_scramble(20)
                    logic.scrambler(cube, scr)
                    print("Scramble:", *scr)
                elif b.text == '?':
                    help_function()
                    setup_win(cube)
                elif b.text == 'Switch':
                    global CUBE_SWITCH
                    CUBE_SWITCH = not CUBE_SWITCH
                    setup_win(cube)
                else:
                    eval('logic.' + b.text + '(cube,' + str(not (pygame.key.get_mods() & pygame.KMOD_SHIFT ^
                                                                 pygame.mouse.get_pressed(3)[2])) + ')')
    else:
        for b in buttons:
            if b.isOver(pos):
                b.color = BUTTON_HOVER_COLOR
            else:
                b.color = BUTTON_COLOR


def setup_win(cube):
    WIN.fill(GREY)
    setup_buttons()
    draw_cube(cube)


def main():
    cube = logic.Cube()
    clock = pygame.time.Clock()
    setup_win(cube)

    run = True
    while run:
        setup_buttons()
        clock.tick(FPS)
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEMOTION:
                handle_buttons(cube, 'move', pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_buttons(cube, 'press', pos)
                draw_cube(cube)


if __name__ == '__main__':
    main()
