import pygame
import sys

class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        

        #Bullet settings
        self.bullet_speed  = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 255, 255)
        self.bullets_allowed = 3
        #self.bullets_speed_up =  10.0

        #Enemy Settings
        self.enemy_speed = 1.0
        self.fleet_drop_speed = 10
            #fleet direction 1 is right and -1 is left
        self.fleet_direction = 1   

        #ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3 