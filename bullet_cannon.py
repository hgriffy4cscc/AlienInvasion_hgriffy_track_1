"""Generates and manages sprite representing a cannonball (gravity-affected)."""

# Python modules
from typing import TYPE_CHECKING
# Installed modules
import pygame
from pygame.sprite import Sprite
# Custom/game modules
if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Cannon(Sprite):
    """Manages a cannonball-style ammunition Sprite"""

    def __init__(self, game: 'AlienInvasion') -> None:
        super().__init__()

        self.game: AlienInvasion = game

        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load(self.settings.cannon_file)
        self.image = pygame.transform.scale(
            self.image,
                (self.settings.cannon_w,
                 self.settings.cannon_h)
            )

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.midbottom = game.ship.rect.midtop
        self.y: int = self.rect.y
        self.initial_y: int = self.rect.y
        self.x: int = self.rect.x
        self.initial_x: int = self.rect.x
        self.motion_h: int
        self._discern_horizontal_motion()
        self.launch_time: int = pygame.time.get_ticks()

        self.cost = self.settings.cannon_cost


    def _discern_horizontal_motion(self) -> None:
        """Based on ship motion, determines if cannonball should move horizontally.
        
        Effects:
            Updates attribute.
        """
        if self.game.ship.moving_left:
            self.motion_h = -self.settings.ship_speed // 2
        elif self.game.ship.moving_right:
            self.motion_h = self.settings.ship_speed // 2
        else:
            self.motion_h = 0

    def update(self) -> None:
        """Updates variables based on game action"""
        self._determine_vertical_motion()
        self.determine_horizontal_motion()

    def determine_horizontal_motion(self):
        """Per clock tick, determines new horizontal position of cannonball."""
        if self.motion_h:
            self.x += self.motion_h
            self.rect.x = int(self.x)

    def _determine_vertical_motion(self):
        """Per clock tick + imitating gravity, determines new vertical position of cannonball."""
        gravity: int = self.settings.cannon_gravity
        velocity: int = self.settings.cannon_initial_velocity
        t: float = (pygame.time.get_ticks() - self.launch_time) / 1000
        motion_y: int = int((velocity * t) - (gravity * (t ** 2)))
        self.y = self.initial_y - motion_y
        self.rect.y = int(self.y)

    def draw(self) -> None:
        """Represents the bullet on the screen."""
        self.screen.blit(self.image, self.rect)
