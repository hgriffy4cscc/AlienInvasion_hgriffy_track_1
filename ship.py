"""Class to define protagonist ship + actions"""

import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Ship:
    
    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal') -> None:
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image,
            (self.settings.ship_w,self.settings.ship_h)
            )
        
        self.rect = self.image.get_rect()
        self._center_ship()
        
        self.moving_left = False
        self.moving_right = False

        self.arsenal = arsenal

    def _center_ship(self):
        """return ship to the middle of the screen"""
        self.rect.midbottom = self.boundaries.midbottom
        self.x = float(self.rect.x)

    def update(self):
        """update the position of the ship"""
        self._update_ship_movement()
        self.arsenal.update_arsenals()

    def _update_ship_movement(self):
        """calculate position of the ship (for self.update())"""
        temp_speed = self.settings.ship_speed
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x -= temp_speed
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x += temp_speed

        self.rect.x = int(self.x)

    def draw(self):
        """implement the representation of the ship onto the screen"""
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)

    def fire(self, ammo_type):
        """trigger the code to fire a bullet"""
        return self.arsenal.fire_bullet(ammo_type)
    
    def check_collisions(self, other_group):
        """determine if the ship has collided with another screen element"""
        if pygame.sprite.spritecollideany(self, other_group):
            self._center_ship()
            return True
        return False