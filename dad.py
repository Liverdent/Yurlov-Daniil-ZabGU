import pygame


def look_at(object, coords):
    pass


def capsule(surface, x = 0, y=0, radius=30, heigh=70):
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

capsule(screen, 60, 60, 40, 90)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pygame.display.flip()