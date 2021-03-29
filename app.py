from Logic import logic
from button import *

pygame.init()

pygame.display.set_caption('Rubik\'s Cube')

WIDTH = 900
HEIGHT = 500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
GREY = (200,200,200)
WHITE = (255,255,255)
YELLOW = (255,255,0)
RED = (255,0,0)
ORANGE = (255,165,0)
BLUE = (0,0,255)
GREEN = (0,200,0)
BLACK=(0,0,0)
sw=35
ew=3
BUTTON_COLOR = GREY
FPS=60


# draws the given cube to WIN in a flat layout
def draw_cube(cube, x, y):
    colors = {'W':WHITE, 'Y':YELLOW, 'O':ORANGE, 'G':GREEN, 'R':RED, 'B':BLUE}
    grid = [row.split() for row in str(cube).split('\n') if row!='']
    # stickers
    for i in range(9):
        indexes=range(3,6) if (i<3 or i>5) else range(12)
        for j in indexes:
            square = pygame.Rect(j * sw + ew*j + x, i * sw + ew*i + y, sw, sw)
            color = colors[grid[i][j - 3 * int(i<3 or i>5)]]
            pygame.draw.rect(WIN, color, square)

    # edges
    for i in range(10):
        if i < 3 or i > 6:
            edge = [3 * sw + 3*ew + x-ew, (i) * sw + ew*i + y-ew, 3*(sw+ew)+ew, ew]
        else:
            edge = [x-ew,(i) * sw + ew*i + y-ew,12*(sw+ew),ew]
        pygame.draw.rect(WIN,BLACK,edge)

    for i in range(13):
        if i<3 or i>6:
            edge = [(i) * sw + ew*i + x-ew, 3 * sw + 3*ew+y-ew, ew, 3*(sw+ew)+ew]
        else:
            edge = [(i) * sw + ew*i + x-ew,y-ew,ew,9*(sw+ew)+ew]
        pygame.draw.rect(WIN, BLACK, edge)
    pygame.display.update()


right=button(BUTTON_COLOR,100,100,50,50,'R')
left=button(BUTTON_COLOR,175,100,50,50,'L')
up=button(BUTTON_COLOR,100,175,50,50,'U')
down=button(BUTTON_COLOR,175,175,50,50,'D')
front=button(BUTTON_COLOR,100,250,50,50,'F')
back=button(BUTTON_COLOR,175,250,50,50,'B')
buttons= [right,left,up,down,front,back]

def setup_buttons():
    for b in buttons:
        b.draw(WIN,BLACK)
    pygame.display.update()

def handle_buttons(cube,mode,pos):
    if mode=='press':
        for b in buttons:
            if b.isOver(pos):
                eval('logic.'+b.text+'(cube,True)')
    else:
        for b in buttons:
            if b.isOver(pos):
                b.color = (0, 255, 255)
            else:
                b.color = BUTTON_COLOR

def main():
    WIN.fill(GREY)
    cube = logic.Cube()
    clock = pygame.time.Clock()

    # testing
    # scramble = logic.gen_scramble(20)
    # print("Scramble:",*scramble)
    # logic.scrambler(cube, scramble)

    draw_cube(cube, 400, (HEIGHT-(10*ew+9*sw))/2)
    run = True
    while run:
        setup_buttons()
        clock.tick(FPS)
        pos=pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEMOTION:
                handle_buttons(cube,'move',pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_buttons(cube,'press',pos)
            draw_cube(cube, 400, (HEIGHT - (10 * ew + 9 * sw)) / 2)


if __name__ == '__main__':
    main()
