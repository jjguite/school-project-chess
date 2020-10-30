import pygame
from pieces import template
import colors


class Bishop(template.Template):

    def __init__(self, location, color):
        template.Template.__init__(self, location, color)

        self.ID = 'B'
        self.image_a = pygame.image.load('pieces/img/White B.png')
        self.image_b = pygame.image.load('pieces/img/Black B.png')

        if self.color == (255, 255, 255): self.image = self.image_a
        elif self.color == (0, 0, 0): self.image = self.image_b