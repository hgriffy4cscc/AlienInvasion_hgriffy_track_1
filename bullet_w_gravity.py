"""class to define and control a bullet that will obey gravity (ie fall back down)"""

import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class BulletWithGravity(Sprite):

    def __init__(self, game: 'AlienInvasion') -> None:
        super().__init__()

        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load(self.settings.bullet_w_gravity_file)
        self.image = pygame.transform.scale(self.image,
            (self.settings.bullet_w_gravity_w,self.settings.bullet_w_gravity_h)
            )
        
        self.rect = self.image.get_rect()
        self.rect.midbottom = game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        """update variables based on game action"""
        self.y -= self.settings.bullet_w_gravity_speed
        self.rect.y = int(self.y)

    def draw(self):
        """actually represent the bullet on the screen"""
        self.screen.blit(self.image, self.rect)
