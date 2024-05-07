import pygame

class player():
    def __init__(self, position=(0, 0), scale=(10, 10)):
        self.position = position
        self.scale = scale

        body = pygame.Rect(self.position, self.scale)
        sprite = capsule
        player = {body: body, sprite: sprite}





def look_at(object, coords):
    pass


def capsule(surface, x=0, y=0, radius=30, heigh=70):
    heigh = max(heigh, 2 * radius)
    pygame.draw.circle(surface, 'darkgrey', (x + radius, y + heigh - radius), radius)
    pygame.draw.rect(surface, 'white', (x, y + radius, 2 * radius, heigh - 2 * radius))
    pygame.draw.circle(surface, 'purple', (x + radius, y + radius), radius)

pygame.init()

screen_size = 800, 600
screen_size_x = screen_size[0]
screen_size_y = screen_size[1]

screen = pygame.display.set_mode((screen_size_x, screen_size_y))
#player = pygame.surface
done = False

a = pygame.Rect(10, 10, 20, 20)
capsule(screen, 60, 60, 40, 200)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEMOTION:
            pass

    pygame.display.flip()