"""Construct + represent individual spectator sprites in the game"""

# Python modules
from typing import TYPE_CHECKING
# Installed modules
import pygame
from pygame.sprite import Sprite
# Custom/game modules

if TYPE_CHECKING:
    from spectator_crowd import SpectatorCrowd

class Spectator(Sprite):
    """Define individual spectator Sprites"""

    def __init__(self, crowd: 'SpectatorCrowd', x: int, y: int) -> None:
        """Initialize individual spectator
        
        Args:
            crowd: reference to the full Sprite group of spectators
            x: horizontal position on the screen
            y: vertical position on the screen
        """
        super().__init__()

        # connect spectator to game environment
        self.screen = crowd.game.screen
        self.boundaries: pygame.Rect = crowd.game.screen.get_rect()
        self.settings = crowd.game.settings
        self.crowd: SpectatorCrowd = crowd

        # spectator media (image)
        self.image = pygame.image.load(self.settings.spectator_file)
        self.image = pygame.transform.scale(self.image,
            (self.settings.spectator_w,self.settings.spectator_h)
            )

        # positioning
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x: int = self.rect.x
        self.y: int = self.rect.y

        self.points: int = self.settings.spectator_points


    def draw_spectator(self) -> None:
        """Represents spectator on the screen"""
        self.screen.blit(self.image, self.rect)
