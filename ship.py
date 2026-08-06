"""Manages the ship that the player, aka, playable character in the game."""

# Python modules
from typing import TYPE_CHECKING
# Installed modules
import pygame
# Custom/game modules
if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Ship():
    """Sprite to represent the ship/playable character."""

    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal') -> None:
        self.game: AlienInvasion = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries: pygame.Rect = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image,
            (self.settings.ship_w,self.settings.ship_h)
            )

        self.rect: pygame.Rect = self.image.get_rect()
        self.x: int
        self._center_ship()

        self.moving_left: bool = False
        self.moving_right: bool = False

        self.arsenal: Arsenal = arsenal

    def _center_ship(self) -> None:
        """Returns ship to the middle of the screen.
        
        Effects:
            Changes ship location variable to default.
        """
        self.rect.midbottom = self.boundaries.midbottom
        self.x = self.rect.x

    def update(self) -> None:
        """Updates + represents the ship + triggers update of lasers/cannonballs."""
        self._update_ship_movement()
        self.arsenal.update_arsenals()

    def _update_ship_movement(self) -> None:
        """Calculates position of the ship (for self.update())"""
        temp_speed: int = self.settings.ship_speed # holder to simplify lines below
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x -= temp_speed
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x += temp_speed
        self.rect.x = self.x

    def draw(self) -> None:
        """implements the representation of the ship onto the screen."""
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)

    def fire(self, ammo_type) -> bool:
        """Triggers the code to fire a bullet.
        
        Returns:
            [bool]: Indicates whether laser/cannonball was fired.
        """
        return self.arsenal.fire_bullet(ammo_type)

    def check_collisions(self, other_group) -> bool:
        """Determines if the ship has collided with another screen element (ie alien).
        
        Returns:
            [bool]: True if there was a collision, False otherwise.
        """
        if pygame.sprite.spritecollideany(self, other_group):
            self._center_ship()
            return True
        return False
    
