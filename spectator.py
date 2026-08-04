"""class to represent individual spectators in the game
Depends on:
* settings.py

Is Depended on:
* alien_invasion.py
* spectator_crowd.py

Properties contain:
* positioning
* media (image & sound)

Methods control:
* drawing on screen
* motion
"""

from typing import TYPE_CHECKING
import pygame
from pygame.sprite import Sprite

if TYPE_CHECKING:
    from spectator_crowd import SpectatorCrowd

class Spectator(Sprite):
    """define individual alien Sprites"""

    def __init__(self, crowd: 'SpectatorCrowd', x: int, y: int) -> None:
        super().__init__()

        # connect spectator to game environment
        self.screen = crowd.game.screen
        self.boundaries = crowd.game.screen.get_rect()
        self.settings = crowd.game.settings
        self.crowd = crowd

        # spectator media (image)
        self.image = pygame.image.load(self.settings.spectator_file)
        self.image = pygame.transform.scale(self.image,
            (self.settings.spectator_w,self.settings.spectator_h)
            )

        # positioning
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x: int = self.rect.x
        self.y: int = self.rect.y

        self.points: int = self.settings.spectator_points


    def update(self) -> None:
        """per clock, update location"""
        self.rect.x = self.x
        self.rect.y = self.y

    def draw_spectator(self) -> None:
        """represent spectator on the screen"""
        self.screen.blit(self.image, self.rect)
