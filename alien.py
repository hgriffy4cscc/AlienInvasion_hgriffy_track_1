"""Construct + represent individual alien sprites in the game"""

# Python modules
from typing import TYPE_CHECKING
# Installed modules
import pygame
from pygame.sprite import Sprite
# Custom/game modules

if TYPE_CHECKING:
    from alien_fleet import AlienFleet

class Alien(Sprite):
    """Define individual alien Sprites"""

    def __init__(self, fleet: 'AlienFleet', x: int, y: int) -> None:
        """Initialize individual alien
        
        Args:
            fleet: reference to the full Sprite group of aliens
            x: horizontal position on the screen
            y: vertical position on the screen
        """
        super().__init__()

        # connect alien to game environment
        self.screen = fleet.game.screen
        self.boundaries: pygame.Rect = fleet.game.screen.get_rect()
        self.settings = fleet.game.settings
        self.fleet: AlienFleet = fleet

        # alien media (image)
        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image,
            (self.settings.alien_w,self.settings.alien_h)
            )

        # positioning
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x: int = self.rect.x
        self.y: int = self.rect.y

        self.points: int = self.settings.alien_points

    def update(self) -> None:
        """Per clock tick, updates location of this Sprite"""
        temp_speed: int = self.settings.alien_fleet_speed
        self.x += temp_speed * self.fleet.alien_fleet_direction
        self.rect.x = self.x
        self.rect.y = self.y

    def check_edges(self) -> bool:
        """Reports if alien is at or outside screen horizontal boundaries.
        
        Returns:
            [bool]: True if alien is at or beyond horizontal boundaries"""
        return (self.rect.right >= self.boundaries.right
                or self.rect.left <= self.boundaries.left)

    def draw_alien(self) -> None:
        """Represents alien on the screen"""
        self.screen.blit(self.image, self.rect)
