"""class to define and control a bullet that will obey gravity (ie fall back down)"""

import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class BulletWithGravity(Sprite):

    def __init__(self, game: 'AlienInvasion') -> None:
        super().__init__()

        self.game = game

        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load(self.settings.bullet_w_gravity_file)
        self.image = pygame.transform.scale(
            self.image,
                (self.settings.bullet_w_gravity_w,
                 self.settings.bullet_w_gravity_h)
            )
        
        self.rect = self.image.get_rect()
        self.rect.midbottom = game.ship.rect.midtop
        self.y = float(self.rect.y)
        self.initial_y = float(self.rect.y)

        self.launch_time = pygame.time.get_ticks()

    def update(self):
        """update variables based on game action"""
        gravity = self.settings.bullet_w_gravity_gravity
        velocity = self.settings.bullet_w_gravity_initial_velocity
        t = (pygame.time.get_ticks() - self.launch_time) / 1000
        motion = (velocity * t) - (gravity * (t ** 2))
        self.y = self.initial_y - motion
        print(f"elapsed {t} :: motion: {motion} :: self.y: {self.y}")
        self.rect.y = int(self.y)

    def draw(self):
        """actually represent the bullet on the screen"""
        self.screen.blit(self.image, self.rect)
