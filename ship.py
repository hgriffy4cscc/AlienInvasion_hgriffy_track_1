"""Class to define protagonist ship + actions
Depends on:
* settings.py
* 

Is Depended on:
* alien_invasion.py
* 

Properties contain:
* 

Methods control:
* 
"""

from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Ship():
    """Sprite to represent the ship/playable character"""

    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal') -> None:
        self.game: AlienInvasion = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image,
            (self.settings.ship_w,self.settings.ship_h)
            )

        self.rect = self.image.get_rect()
        self.x: int
        self._center_ship()

        self.moving_left: bool = False
        self.moving_right: bool = False

        self.arsenal: Arsenal = arsenal

    def _center_ship(self) -> None:
        """return ship to the middle of the screen"""
        self.rect.midbottom = self.boundaries.midbottom
        self.x = self.rect.x

    def update(self) -> None:
        """update the position of the ship"""
        self._update_ship_movement()
        self.arsenal.update_arsenals()

    def _update_ship_movement(self) -> None:
        """calculate position of the ship (for self.update())"""
        temp_speed: int = self.settings.ship_speed
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x -= temp_speed
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x += temp_speed
        self.rect.x = self.x

    def draw(self) -> None:
        """implement the representation of the ship onto the screen"""
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)

    def fire(self, ammo_type) -> bool:
        """trigger the code to fire a bullet"""
        return self.arsenal.fire_bullet(ammo_type)

    def check_collisions(self, other_group) -> bool:
        """determine if the ship has collided with another screen element (ie alien)"""
        if pygame.sprite.spritecollideany(self, other_group):
            self._center_ship()
            return True
        return False
