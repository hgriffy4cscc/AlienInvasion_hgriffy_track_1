"""Generates and manages sprite representing a cannonball (gravity-affected)."""

# Python modules
from typing import TYPE_CHECKING
# Installed modules
import pygame
from pygame.sprite import Sprite
# Custom/game modules
if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Laser(Sprite):
    """Manages a laser-style ammunition Sprite"""

    def __init__(self, game: 'AlienInvasion') -> None:
        super().__init__()

        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(self.image,
            (self.settings.laser_w,self.settings.laser_h)
            )

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.midtop = game.ship.rect.midtop
        self.y: int = self.rect.y

    def update(self) -> None:
        """Updates variables based on game action"""
        self.y -= self.settings.laser_speed
        self.rect.y = int(self.y)

    def draw(self) -> None:
        """Represents the bullet on the screen."""
        self.screen.blit(self.image, self.rect)
