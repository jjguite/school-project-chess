import pygame

import colors
from pieces import template


class Rook(template.Template):

    def __init__(self, location, color):
        template.Template.__init__(self, location, color)

        self.ID = 'R'
        self.image_a = pygame.image.load('pieces/img/White R.png')
        self.image_b = pygame.image.load('pieces/img/Black R.png')

        if self.color == (255, 255, 255): self.image = self.image_a
        elif self.color == (0, 0, 0): self.image = self.image_b