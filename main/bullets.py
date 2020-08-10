import pygame
from pygame.sprite import Sprite

class Bullets(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #Creating a bullet
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        #Move bullet up the screen:
        self.y -= self.settings.bullet_speed

        #Update value of self.rect.y
        self.rect.y = self.y

    def draw_bullets(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

"""class Bullets_Up(Bullets):
    def __init__(self, ai_game):
        super().__init__(ai_game)

    def update(self):
        self.y -= self.settings.bullets_speed_up
        self.rect.y = self.y"""