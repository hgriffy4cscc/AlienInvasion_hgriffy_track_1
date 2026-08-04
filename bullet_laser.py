"""class to define and control a laser style bullet
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

import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Laser(Sprite):

    def __init__(self, game: 'AlienInvasion') -> None:
        super().__init__()

        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(self.image,
            (self.settings.laser_w,self.settings.laser_h)
            )
        
        self.rect = self.image.get_rect()
        self.rect.midtop = game.ship.rect.midtop
        self.y: int = self.rect.y

    def update(self):
        """modify variables based on game action"""
        self.y -= self.settings.laser_speed
        self.rect.y = int(self.y)

    def draw(self):
        """actually put the bullet on the screen"""
        self.screen.blit(self.image, self.rect)
