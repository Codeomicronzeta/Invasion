import pygame
from pygame.sprite import Sprite

class Enemy(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #Loading enemy image
        self.image = pygame.image.load('images/enemy.png')
        self.rect = self.image.get_rect()

        #Initializing position of enemy
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        #Move to the right or 
        self.x += (self.settings.enemy_speed * self.settings.fleet_direction)
        self.rect.x = self.x



    


