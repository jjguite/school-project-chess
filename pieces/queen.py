import pygame

import colors
from pieces import template


class Queen(template.Template):

    def __init__(self, location, color):
        template.Template.__init__(self, location, color)

        self.ID = 'Q'
        self.image_a = pygame.image.load('pieces/img/White Q.png')
        self.image_b = pygame.image.load('pieces/img/Black Q.png')

        if self.color == (255, 255, 255): self.image = self.image_a
        elif self.color == (0, 0, 0): self.image = self.image_b





