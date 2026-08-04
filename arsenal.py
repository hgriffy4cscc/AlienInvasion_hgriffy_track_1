"""defines a class to control player collection of ammo
Depends on:
* settings.py
* bullet_cannon.py
* bullet_laser.py

Is Depended on:
* arsenal.py
* ship.py

Properties contain:
* list of lasers fired
* list of cannon fired

Methods control:
* drawing on screen
* removing any that have left screen
* "firing" lasers
* "firing" cannon
"""

from typing import TYPE_CHECKING
import pygame
from bullet_laser import Laser
from bullet_cannon import Cannon

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Arsenal:
    """class that holds bullets (Laser and Cannon)"""

    def __init__(self, game: 'AlienInvasion') -> None:
        self.game = game
        self.settings = game.settings
        #self.screen = game.screen
        #self.boundaries = game.screen.get_rect()
        self.laser_arsenal = pygame.sprite.Group()
        self.cannon_arsenal = pygame.sprite.Group()
        # group arsenals for easier bulk processing
        self.all_arsenals: list = [self.laser_arsenal, self.cannon_arsenal]

    def update_arsenals(self) -> None:
        """change game display to account for game actions"""
        for arsenal in self.all_arsenals:
            arsenal.update()
            self._remove_bullets_offscreen()

    def _remove_bullets_offscreen(self) -> None:
        """if any bullets have left the screen remove them from play"""
        for arsenal in self.all_arsenals:
            for bullet in arsenal.copy():
                if bullet.rect.bottom <= 0 or bullet.rect.top >= self.settings.screen_h \
                    or bullet.rect.right <= 0 or bullet.rect.left >= self.settings.screen_w:
                    arsenal.remove(bullet)

    def draw(self) -> None:
        """represent bullet objects on the screen"""
        for arsenal in self.all_arsenals:
            for bullet in arsenal:
                bullet.draw()

    def fire_bullet(self, bullet_type) -> bool:
        """per player action, launch new bullet"""
        if bullet_type == 'laser':
            if len(self.laser_arsenal) < (self.settings.laser_arsenal_max):
                new_bullet = Laser(self.game)
                self.laser_arsenal.add(new_bullet)
                return True
        elif bullet_type == 'cannon':
            if len(self.cannon_arsenal) < ( self.settings.cannon_arsenal_max ):
                new_bullet = Cannon(self.game)
                self.cannon_arsenal.add(new_bullet)
                return True
        return False
