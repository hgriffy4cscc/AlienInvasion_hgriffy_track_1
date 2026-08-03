"""defines a class to control player collection of ammo"""

import pygame
from bullet import Bullet
from cannon import BulletWithGravity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Arsenal:

    def __init__(self, game: 'AlienInvasion') -> None:
        self.game = game
        self.settings = game.settings
        #self.screen = game.screen
        #self.boundaries = game.screen.get_rect()
        self.arsenal = pygame.sprite.Group()
    
    def update_arsenal(self):
        """change game display to account for game actions"""
        self.arsenal.update()
        self._remove_bullets_offscreen()

    def _remove_bullets_offscreen(self):
        """if any bullets have left the screen remove them from play"""
        for bullet in self.arsenal.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.top >= self.settings.screen_h:
                self.arsenal.remove(bullet)

    def draw(self):
        """represent bullet objects on the screen"""
        for bullet in self.arsenal:
            bullet.draw()

    def fire_bullet(self, bullet_type):
        """per player action, launch new bullet"""
        if len(self.arsenal) < ( self.settings.bullet_count + self.settings.cannon_count ):
            if bullet_type == 'laser':
                new_bullet = Bullet(self.game)
                self.arsenal.add(new_bullet)
                return True
            elif bullet_type == 'gravitational':
                new_bullet = BulletWithGravity(self.game)
                self.arsenal.add(new_bullet)
                return True
        return False