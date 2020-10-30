import pygame
import colors
from pieces import template


class Pawn(template.Template):

    def __init__(self, location, color):
        template.Template.__init__(self, location, color)

        self.ID = 'P'
        self.promote = False
        self.image_a = pygame.image.load('pieces/img/White P.png')
        self.image_b = pygame.image.load('pieces/img/Black P.png')

        if self.color == (255, 255, 255): self.image = self.image_a
        elif self.color == (0, 0, 0): self.image = self.image_b

    def _move(self):
        if self.color == colors.PLAYER_1:
            if self.location[1] == 7:
                self.promote = True
        if self.color == colors.PLAYER_2:
            if self.location[1] == 0:
                self.promote = True
