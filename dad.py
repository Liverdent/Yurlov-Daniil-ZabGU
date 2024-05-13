import pygame
import random


class button:
    def __init__(self, surface,  position=(0, 0), size=(50, 20), text='Введите текст', color='white'):
        self.parent = surface
        self.surface = pygame.Surface(size)
        self.font = pygame.font.Font(None, 24)
        self.text = self.font.render(text, True, (0, 0, 0))
        self.text_rect = self.text.get_rect(center=(size[0] / 2, size[1] / 2))
        self.button_rect = pygame.Rect(125, 125, 150, 50)
        self.color = color
        self.position = position
        self.size = size

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.position + self.size)
        self.surface.blit(self.text, self.text_rect)


class desk:
    def __init__(self, surface, size, indent, *players):
        # screen settings
        self.surface = surface
        self.indent = indent
        self.screen_size = size
        # player settings
        # order
        if len(players) == 1:
            self.coop = False
            self.players = (player[0], "AI") if random.randint(0, 2) == 0 else ('AI', player[0])
        else:
            self.coop = True
            self.players = players if random.randint(0, 2) == 0 else players[::-1]
        self.cur_player = 'cross'
        # line positions (big)
        self.line1 = (screen_size - 2 * self.indent) / 3 + self.indent
        self.line2 = screen_size - self.line1
        # line positions (small)
        self.line11 = (self.line1 - self.indent) / 3 + self.indent
        self.line12 = (self.line1 - self.indent) / 3 * 2 + self.indent
        self.line21 = self.line1 + self.line11 - self.indent
        self.line22 = self.screen_size - self.line21
        self.line31 = self.screen_size - self.line12
        self.line32 = self.screen_size - self.line11

        self.lines = [self.indent, self.line11, self.line12, self.line1, self.line21,
                      self.line22, self.line2, self.line31, self.line32, self.screen_size - self.indent]
        self.big_lines = [self.indent, self.line1, self.line2, self.screen_size - self.indent]
        # fields

        self.cur_field = None
        self.fields = [[None] * 9 for _ in range(9)]
        self.field = [None] * 9
        # translation position to indexes
        self.translate = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2],
                          [0, 3], [0, 4], [0, 5], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5],
                          [0, 6], [0, 7], [0, 8], [1, 6], [1, 7], [1, 8], [2, 6], [2, 7], [2, 8],
                          [3, 0], [3, 1], [3, 2], [4, 0], [4, 1], [4, 2], [5, 0], [5, 1], [5, 2],
                          [3, 3], [3, 4], [3, 5], [4, 3], [4, 4], [4, 5], [5, 3], [5, 4], [5, 5],
                          [3, 6], [3, 7], [3, 8], [4, 6], [4, 7], [4, 8], [5, 6], [5, 7], [5, 8],
                          [6, 0], [6, 1], [6, 2], [7, 0], [7, 1], [7, 2], [8, 0], [8, 1], [8, 2],
                          [6, 3], [6, 4], [6, 5], [7, 3], [7, 4], [7, 5], [8, 3], [8, 4], [8, 5],
                          [6, 6], [6, 7], [6, 8], [7, 6], [7, 7], [7, 8], [8, 6], [8, 7], [8, 8]]
        self.translate_big = [[1, 1], [2, 1], [3, 1], [1, 2], [2, 2], [3, 2], [1, 3], [2, 3], [3, 3]]
        # checker for win
        self.check = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

    def get_current(self):
        return self.cur_player

    def change_player(self):
        self.cur_player = 'cross' if self.cur_player == 'zero' else 'zero'

    def set_fig(self, position):
        pos = [min(max(i, self.indent), self.screen_size - self.indent)for i in position]
        pos = [(int(i // ((self.screen_size - 2 * self.indent) / 9))) for i in pos]
        pos = [max(p, 1) for p in pos]

        pos_ = int(9 * (pos[1] - 1) + pos[0] - 1)
        new_pos = self.translate[pos_]

        if self.fields[new_pos[0]][new_pos[1]] != None:
            return

        self.draw_fig(True, pos)
        self.fields[new_pos[0]][new_pos[1]] = self.cur_player
        self.cur_field = new_pos
        self.check_desk()
        self.change_player()

    def set_fig_big(self, field):
        pos = self.translate_big[field]
        new_pos = int(3 * (pos[1] - 1) + pos[0] - 1)
        self.draw_fig(False, pos)
        self.field[new_pos] = self.cur_player
        if self.check_grid(self.field):
            print('win')

    def draw_fig(self, little=True, position=(0, 0), width=2):
        if little:
            xy1 = [self.lines[pos] - self.indent / 3 if self.lines[pos] in self.big_lines
                   else self.lines[pos] - self.indent * 2 / 9 for pos in position]
            position = [pos - 1 for pos in position]
            xy2 = [self.lines[pos] + self.indent / 3 if self.lines[pos] in self.big_lines
                   else self.lines[pos] + self.indent * 2 / 9 for pos in position]
            xy3 = [xy2[0], xy1[1]]
            xy4 = [xy1[0], xy2[1]]
        else:
            width *= 3
            xy1 = [self.big_lines[pos] - self.indent / 3 for pos in position]
            position = [pos - 1 for pos in position]
            xy2 = [self.big_lines[pos] + self.indent / 3 for pos in position]
            xy3 = [xy2[0], xy1[1]]
            xy4 = [xy1[0], xy2[1]]

        centre = [(xy1[i] + xy2[i]) / 2 for i in range(2)]
        radius = abs(xy2[0] - xy1[0]) / 2

        if self.get_current() == 'cross':
            pygame.draw.line(self.surface, 'red', xy1, xy2, width)
            pygame.draw.line(self.surface, 'red', xy3, xy4, width)
        elif self.get_current() == 'zero':
            pygame.draw.circle(self.surface, 'green', centre, radius, width)

    def check_grid(self, field: list):
        # получаем ряды для проверки
        for line in self.check:
            tri = True
            # получааем индексы из рядов
            for i in line:
                if field[i] != self.get_current():
                    tri = False
            if tri:
                return True
        return False

    def check_desk(self):
        for field in range(9):
            if self.check_grid(self.fields[field]):
                self.set_fig_big(field)

    def draw_(self, color='purple'):
        pygame.draw.line(self.surface, color, (self.indent, self.line1),
                         (self.screen_size - self.indent, self.line1), 5)
        pygame.draw.line(self.surface, color, (self.indent, self.line2),
                         (self.screen_size - self.indent, self.line2), 5)

        pygame.draw.line(self.surface, color, (self.line2, self.indent),
                         (self.line2, self.screen_size - self.indent), 5)
        pygame.draw.line(self.surface, color, (self.line1, self.indent),
                         (self.line1, self.screen_size - self.indent), 5)

        pygame.draw.line(self.surface, color, (self.indent * 1.3, self.line11),
                         (self.line1 - self.indent * 0.3, self.line11), 3)
        pygame.draw.line(self.surface, color, (self.line1 + self.indent * 0.3, self.line11),
                         (self.line2 - self.indent * 0.3, self.line11), 3)
        pygame.draw.line(self.surface, color, (self.line2 + self.indent * 0.3, self.line11),
                         (self.screen_size - self.indent * 1.3, self.line11), 3)

        pygame.draw.line(self.surface, color, (self.indent * 1.3, self.line12),
                         (self.line1 - self.indent * 0.3, self.line12), 3)
        pygame.draw.line(self.surface, color, (self.line1 + self.indent * 0.3, self.line12),
                         (self.line2 - self.indent * 0.3, self.line12), 3)
        pygame.draw.line(self.surface, color, (self.line2 + self.indent * 0.3, self.line12),
                         (self.screen_size - self.indent * 1.3, self.line12), 3)

        pygame.draw.line(self.surface, color, (self.indent * 1.3, self.line21),
                         (self.line1 - self.indent * 0.3, self.line21), 3)
        pygame.draw.line(self.surface, color, (self.line1 + self.indent * 0.3, self.line21),
                         (self.line2 - self.indent * 0.3, self.line21), 3)
        pygame.draw.line(self.surface, color, (self.line2 + self.indent * 0.3, self.line21),
                         (self.screen_size - self.indent * 1.3, self.line21), 3)

        pygame.draw.line(self.surface, color, (self.indent * 1.3, self.line22),
                         (self.line1 - self.indent * 0.3, self.line22), 3)
        pygame.draw.line(self.surface, color, (self.line1 + self.indent * 0.3, self.line22),
                         (self.line2 - self.indent * 0.3, self.line22), 3)
        pygame.draw.line(self.surface, color, (self.line2 + self.indent * 0.3, self.line22),
                         (self.screen_size - self.indent * 1.3, self.line22), 3)

        pygame.draw.line(self.surface, color, (self.indent * 1.3, self.line31),
                         (self.line1 - self.indent * 0.3, self.line31), 3)
        pygame.draw.line(self.surface, color, (self.line1 + self.indent * 0.3, self.line31),
                         (self.line2 - self.indent * 0.3, self.line31), 3)
        pygame.draw.line(self.surface, color, (self.line2 + self.indent * 0.3, self.line31),
                         (self.screen_size - self.indent * 1.3, self.line31), 3)

        pygame.draw.line(self.surface, color, (self.indent * 1.3, self.line32),
                         (self.line1 - self.indent * 0.3, self.line32), 3)
        pygame.draw.line(self.surface, color, (self.line1 + self.indent * 0.3, self.line32),
                         (self.line2 - self.indent * 0.3, self.line32), 3)
        pygame.draw.line(self.surface, color, (self.line2 + self.indent * 0.3, self.line32),
                         (self.screen_size - self.indent * 1.3, self.line32), 3)

        pygame.draw.line(self.surface, color, (self.line11, self.indent * 1.3),
                         (self.line11, self.line1 - self.indent * 0.3), 3)
        pygame.draw.line(self.surface, color, (self.line11, self.line1 + self.indent * 0.3),
                         (self.line11, self.line2 - self.indent * 0.3), 3)
        pygame.draw.line(self.surface, color, (self.line11, self.line2 + self.indent * 0.3),
                         (self.line11, self.screen_size - self.indent * 1.3), 3)

        pygame.draw.line(self.surface, color, (self.line12, self.indent * 1.3),
                         (self.line12, self.line1 - self.indent * 0.3), 3)
        pygame.draw.line(self.surface, color, (self.line12, self.line1 + self.indent * 0.3),
                         (self.line12, self.line2 - self.indent * 0.3), 3)
        pygame.draw.line(self.surface, color, (self.line12, self.line2 + self.indent * 0.3),
                         (self.line12, self.screen_size - self.indent * 1.3), 3)

        pygame.draw.line(self.surface, color, (self.line21, self.indent * 1.3),
                         (self.line21, self.line1 - self.indent * 0.3), 3)
        pygame.draw.line(self.surface, color, (self.line21, self.line1 + self.indent * 0.3),
                         (self.line21, self.line2 - self.indent * 0.3), 3)
        pygame.draw.line(self.surface, color, (self.line21, self.line2 + self.indent * 0.3),
                         (self.line21, self.screen_size - self.indent * 1.3), 3)

        pygame.draw.line(self.surface, color, (self.line22, self.indent * 1.3),
                         (self.line22, self.line1 - self.indent * 0.3), 3)
        pygame.draw.line(self.surface, color, (self.line22, self.line1 + self.indent * 0.3),
                         (self.line22, self.line2 - self.indent * 0.3), 3)
        pygame.draw.line(self.surface, color, (self.line22, self.line2 + self.indent * 0.3),
                         (self.line22, self.screen_size - self.indent * 1.3), 3)

        pygame.draw.line(self.surface, color, (self.line31, self.indent * 1.3),
                         (self.line31, self.line1 - self.indent * 0.3), 3)
        pygame.draw.line(self.surface, color, (self.line31, self.line1 + self.indent * 0.3),
                         (self.line31, self.line2 - self.indent * 0.3), 3)
        pygame.draw.line(self.surface, color, (self.line31, self.line2 + self.indent * 0.3),
                         (self.line31, self.screen_size - self.indent * 1.3), 3)

        pygame.draw.line(self.surface, color, (self.line32, self.indent * 1.3),
                         (self.line32, self.line1 - self.indent * 0.3), 3)
        pygame.draw.line(self.surface, color, (self.line32, self.line1 + self.indent * 0.3),
                         (self.line32, self.line2 - self.indent * 0.3), 3)
        pygame.draw.line(self.surface, color, (self.line32, self.line2 + self.indent * 0.3),
                         (self.line32, self.screen_size - self.indent * 1.3), 3)


pygame.init()

screen_size = 600
screen = pygame.display.set_mode((screen_size, screen_size))

layer = pygame.Surface((screen_size, screen_size), pygame.SRCALPHA)

player = "Потом"

Desk = desk(layer, screen_size, 50,  player)

done = False

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            Desk.set_fig(pygame.mouse.get_pos())

    Desk.draw_('grey')
    screen.blit(layer, (0, 0))
    pygame.display.flip()
