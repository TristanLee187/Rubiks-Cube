# PyGame Rubik's Cube application

from Logic import logic
from button import *

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
ew = 3
FPS = 60


# draws the given cube to WIN in a flat layout
def draw_cube(cube, x, y):
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


# buttons
OFFSET_X = 50
OFFSET_Y = 50
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
reset = button(BUTTON_COLOR, OFFSET_X, OFFSET_Y + 4 * SPACE, 2 * BUTTON_SIZE, BUTTON_SIZE, 'Reset')
buttons = [right, left, mid, up, down, equ, front, back, s, X, Y, Z, reset]


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
                else:
                    eval('logic.' + b.text + '(cube,' + str(not (pygame.key.get_mods() & pygame.KMOD_SHIFT)) + ')')
    else:
        for b in buttons:
            if b.isOver(pos):
                b.color = BUTTON_HOVER_COLOR
            else:
                b.color = BUTTON_COLOR


def main():
    WIN.fill(GREY)
    cube = logic.Cube()
    clock = pygame.time.Clock()
    draw_cube(cube, 400, (HEIGHT - (10 * ew + 9 * sw)) / 2)

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
        draw_cube(cube, 400, (HEIGHT - (10 * ew + 9 * sw)) / 2)


if __name__ == '__main__':
    main()
