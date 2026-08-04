"""class to define and control a bullet that will obey gravity (ie fall back down)
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

class Cannon(Sprite):

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
        self.y: int = self.rect.y
        self.initial_y: int = self.rect.y
        self.x: int = self.rect.x
        self.initial_x: int = self.rect.x
        self.motion_h: int
        self._discern_horizontal_motion()
        self.launch_time: int = pygame.time.get_ticks()


    def _discern_horizontal_motion(self) -> None:
        if self.game.ship.moving_left:
            self.motion_h = -self.settings.ship_speed // 2
        elif self.game.ship.moving_right:
            self.motion_h = self.settings.ship_speed // 2
        else:
            self.motion_h = 0

    def update(self) -> None:
        """update variables based on game action"""
        gravity: int = self.settings.cannon_gravity
        velocity: int = self.settings.cannon_initial_velocity
        t: float = (pygame.time.get_ticks() - self.launch_time) / 1000
        motion_y: int = int((velocity * t) - (gravity * (t ** 2)))
        self.y = self.initial_y - motion_y
        self.rect.y = int(self.y)
        if self.motion_h:
            self.x += self.motion_h
            self.rect.x = int(self.x)

    def draw(self) -> None:
        """actually represent the bullet on the screen"""
        self.screen.blit(self.image, self.rect)
