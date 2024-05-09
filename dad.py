import pygame


class desk:
    def __init__(self, surface, size, indent):
        self.surface = surface
        self.indent = indent
        self.screen_size = size
        self.line = (screen_size - 2 * self.indent) / 3 + self.indent
        self.line2 = (screen_size - 2 * self.indent) / 3 * 2 + self.indent

    def draw_(self, color='purple'):
        pygame.draw.line(self.surface,
                         color,
                         (self.indent, self.line),
                         (self.screen_size - self.indent, self.line),
                         5)
        pygame.draw.line(self.surface,
                         color,
                         (self.indent, self.line2),
                         (self.screen_size - self.indent, self.line2),
                         5)
        pygame.draw.line(self.surface,
                         color,
                         (self.line2, self.indent),
                         (self.line2, self.screen_size - self.indent),
                         5)
        pygame.draw.line(self.surface,
                         color,
                         (self.line, self.indent),
                         (self.line, self.screen_size - self.indent),
                         5)


        self.draw_l(color)

    def draw_l(self, color='purple', position=(0, 0)):
        pass

pygame.init()

screen_size = 600


screen = pygame.display.set_mode((screen_size, screen_size))


layer = pygame.Surface((screen_size, screen_size), pygame.SRCALPHA)

Desk = desk(layer, screen_size, 50)

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    Desk.draw_('yellow')

    screen.blit(layer, (0, 0))
    pygame.display.flip()
