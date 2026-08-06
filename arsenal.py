"""Manages sprite group for sprites representing ammunition: lasers and cannonballs."""

# Python modules
from typing import TYPE_CHECKING
# Installed modules
import pygame
# Custom/game modules
from bullet_laser import Laser
from bullet_cannon import Cannon

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Arsenal:
    """Manages sprite group for sprites representing ammunition."""

    def __init__(self, game: 'AlienInvasion') -> None:
        self.game: AlienInvasion = game
        self.settings = game.settings
        #self.screen = game.screen
        #self.boundaries = game.screen.get_rect()
        self.laser_arsenal: pygame.sprite.Group = pygame.sprite.Group()
        self.cannon_arsenal: pygame.sprite.Group = pygame.sprite.Group()
        # group arsenals for easier bulk processing
        self.all_arsenals: list[pygame.sprite.Group] = [self.laser_arsenal, self.cannon_arsenal]

    def update_arsenals(self) -> None:
        """Changes game display to account for game actions."""
        arsenal: pygame.sprite.Group
        for arsenal in self.all_arsenals:
            arsenal.update()
            self._remove_bullets_offscreen()

    def _remove_bullets_offscreen(self) -> None:
        """Determines if any bullets have left the screen + removes them from game.
        
        Effects:
            [contingent]: Optionally removes sprites from group.
        """
        arsenal: pygame.sprite.Group
        bullet: Laser | Cannon
        for arsenal in self.all_arsenals:
            for bullet in arsenal.copy(): # work with copy of array to avoid looping issues
                if bullet.rect.bottom <= 0 or bullet.rect.top >= self.settings.screen_h \
                    or bullet.rect.right <= 0 or bullet.rect.left >= self.settings.screen_w:
                    arsenal.remove(bullet)

    def draw(self) -> None:
        """Represents bullet objects on the screen."""
        bullet: Laser | Cannon
        for arsenal in self.all_arsenals:
            for bullet in arsenal:
                bullet.draw()

    def fire_bullet(self, bullet_type: str) -> bool:
        """Per player action, launches new bullet.
        
        Returns:
            [bool]: Indicates whether or not sprite was created.
        Params:
            bullet_type: "laser" or "cannon" to determine which kind of sprite to create.
        """
        if bullet_type == 'laser':
            if len(self.laser_arsenal) < (self.settings.laser_arsenal_max):
                new_bullet = Laser(self.game)
                self.laser_arsenal.add(new_bullet)
                return True
        elif bullet_type == 'cannon':
            if len(self.cannon_arsenal) < ( self.settings.cannon_arsenal_max ):
                new_bullet = Cannon(self.game)
                self.cannon_arsenal.add(new_bullet)
                return True
        return False
