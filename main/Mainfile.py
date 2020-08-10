import sys
import pygame

from settings import Settings
from ship import Ship
from bullets import Bullets
from enemy import Enemy
from time import sleep
from gamestats import GameStats
#from enemy import check_edges
#from bullets import Bullets_Up

class Invasion:
    def __init__(self):
        pygame.init()   #initialize the game
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Invasion")

        #Instance of GameStats
        self.stats = GameStats(self)
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        #self.bullets_up = pygame.sprite.Group()
        self.bg_color = (230, 230, 230)
        self.enemy = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_enemy()
            self._update_screen()

        
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        #if len(self.bullets) < self.settings.bullets_allowed:
        new_bullet = Bullets(self)
        self.bullets.add(new_bullet)
    
    """def _fire_bullets_up(self):
        new_bullet_up = Bullets_Up(self)
        self.bullets_up.add(new_bullet_up)"""

    def _update_bullets(self):
        self.bullets.update()
        
        #Removing bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            print(len(self.bullets))
            self._check_bullets_enemy_collsions()

    def _check_bullets_enemy_collsions(self):
        #Check for bullets that have enemies
        #If so get rid of them
        collisions = pygame.sprite.groupcollide(self.bullets, self.enemy, True, True)

        if not self.enemy:
            self.bullets.empty()
            self._create_fleet()
    
    def _create_fleet(self):
        enemy = Enemy(self)
        
        enemy_width, enemy_height = enemy.rect.size
        available_space_x = self.settings.screen_width -  (2 * enemy_width)
        num_enemy_x =  available_space_x // (2 * enemy_width)

        #Determine the number of rows of aliens fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * enemy_height) - (ship_height))
        num_rows = available_space_y // (2 * enemy_height)

        #Create full fleet of aliens
        for row_num in range(num_rows): 
            for enemy_num in range(num_enemy_x):
                self._create_enemy(enemy_num, row_num)

    def _create_enemy(self, enemy_num, row_num):    
        #Create an enemy in the row
        enemy = Enemy(self)
        enemy_width, enemy_height = enemy.rect.size
        enemy.x = enemy_width + (2 * enemy_width * enemy_num)
        enemy.rect.x = enemy.x
        enemy.rect.y = enemy.rect.height + (2 * enemy.rect.height * row_num)
        self.enemy.add(enemy)
    
    def _update_enemy(self):
        #Updating the positions of all the enemy
        self._fleet_check_edges()
        self.enemy.update()

        self._check_enemy_bottom()

        #detecting alien, enemy collsion
        if pygame.sprite.spritecollideany(self.ship, self.enemy):
            self._ship_hit()

    def _fleet_check_edges(self):
        for enemy in self.enemy.sprites():
            if enemy.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        for enemy in self.enemy.sprites():
            enemy.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            #Decrement ships left
            self.stats.ships_left -= 1

            #Get rid of aliens and bulllets
            self.enemy.empty()
            self.bullets.empty()

            #Create new ship
            self._create_fleet()
            self.ship.bottom_ship()

            #Pause
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _check_enemy_bottom(self):
        screen_rect = self.screen.get_rect()
        for enemy in self.enemy.sprites():
            if enemy.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_screen(self):   
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullets()
        self.enemy.draw(self.screen)
        pygame.display.flip()
        

if __name__ == '__main__':
    ai = Invasion()
    ai.run_game()
