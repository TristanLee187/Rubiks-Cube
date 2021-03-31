import pygame


class button():
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
        primeless_buttons = ['Reset', 'Scramble', '?']

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
