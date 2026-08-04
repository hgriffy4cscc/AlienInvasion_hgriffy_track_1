"""class to define and control a bullet that will obey gravity (ie fall back down)"""

import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class CannonBullet(Sprite):

    def __init__(self, game: 'AlienInvasion') -> None:
        super().__init__()

        self.game = game

        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load(self.settings.cannon_file)
        self.image = pygame.transform.scale(
            self.image,
                (self.settings.cannon_w,
                 self.settings.cannon_h)
            )
        
        self.rect = self.image.get_rect()
        self.rect.midbottom = game.ship.rect.midtop
        self.y = float(self.rect.y)
        self.initial_y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.initial_x = float(self.rect.x)
        if game.ship.moving_left:
            self.motion_h = -self.settings.ship_speed
        elif game.ship.moving_right:
            self.motion_h = self.settings.ship_speed / 2
        else:
            self.motion_h = 0

        self.launch_time = pygame.time.get_ticks()

    def update(self):
        """update variables based on game action"""
        gravity = self.settings.cannon_gravity
        velocity = self.settings.cannon_initial_velocity
        t = (pygame.time.get_ticks() - self.launch_time) / 1000
        motion = (velocity * t) - (gravity * (t ** 2))
        self.y = self.initial_y - motion
        # print(f"elapsed {t} :: motion: {motion} :: self.y: {self.y}")
        self.rect.y = int(self.y)
        if self.motion_h:
            print(f'self.motion_h: {self.motion_h}')
            self.x += self.motion_h
            self.rect.x = int(self.x)

    def draw(self):
        """actually represent the bullet on the screen"""
        self.screen.blit(self.image, self.rect)
