"""class to represent individual aliens in the game
Depends on:
* settings.py

Is Depended on:
* alien_invasion.py
* alien_fleet.py

Properties contain:
* positioning
* media (image & sound)

Methods control:
* drawing on screen
* motion
"""

import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_fleet import AlienFleet

class Alien(Sprite):

    def __init__(self, fleet: 'AlienFleet', x: int, y: int) -> None:
        super().__init__()

        # connect alien to game environment
        self.screen = fleet.game.screen
        self.boundaries = fleet.game.screen.get_rect()
        self.settings = fleet.game.settings
        self.fleet = fleet

        # alien media (image)
        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image,
            (self.settings.alien_w,self.settings.alien_h)
            )

        # positioning
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x: int = self.rect.x
        self.y: int = self.rect.y

    def update(self) -> None:
        """per clock, update location"""
        temp_speed: int = self.settings.alien_fleet_speed
        self.x += temp_speed * self.fleet.alien_fleet_direction
        self.rect.x = self.x
        self.rect.y = self.y

    def check_edges(self) -> bool:
        """report if alien within screen boundaries"""
        return (self.rect.right >= self.boundaries.right 
                or self.rect.left <= self.boundaries.left)

    def draw_alien(self) -> None:
        """represent alien on the screen"""
        self.screen.blit(self.image, self.rect)
