"""defines a class to control player collection of ammo"""

import pygame
from bullet import Bullet
from cannon import CannonBullet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Arsenal:

    def __init__(self, game: 'AlienInvasion') -> None:
        self.game = game
        self.settings = game.settings
        #self.screen = game.screen
        #self.boundaries = game.screen.get_rect()
        self.laser_arsenal = pygame.sprite.Group()
        self.cannon_arsenal = pygame.sprite.Group()
        # group arsenals for easier bulk processing
        self.all_arsenals = [self.laser_arsenal, self.cannon_arsenal]
    
    def update_arsenals(self):
        """change game display to account for game actions"""
        for arsenal in self.all_arsenals:
            arsenal.update()
            self._remove_bullets_offscreen()

    def _remove_bullets_offscreen(self):
        """if any bullets have left the screen remove them from play"""
        for arsenal in self.all_arsenals:
            for bullet in arsenal.copy():
                if bullet.rect.bottom <= 0 or bullet.rect.top >= self.settings.screen_h \
                    or bullet.rect.right <= 0 or bullet.rect.left >= self.settings.screen_w:
                    arsenal.remove(bullet)
  
    def draw(self):
        """represent bullet objects on the screen"""
        for arsenal in self.all_arsenals:
            for bullet in arsenal:
                bullet.draw()

    def fire_bullet(self, bullet_type):
        """per player action, launch new bullet"""
        if bullet_type == 'laser':
            if len(self.laser_arsenal) < (self.settings.laser_count):
                new_bullet = Bullet(self.game)
                self.laser_arsenal.add(new_bullet)
                return True
        elif bullet_type == 'cannon':
            if len(self.cannon_arsenal) < ( self.settings.cannon_arsenal_max ):
                new_bullet = CannonBullet(self.game)
                self.cannon_arsenal.add(new_bullet)
                return True
        return False