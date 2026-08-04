"""class to represent group of spectators in the game
Depends on:
* settings.py
* spectator.py

Is Depended on:
* alien_invasion.py
* spectator.py

Properties contain:
* group dimensions + position

Methods control:
* triggers creation of spectators
* drawing on screen
* collisions
* existence of fleet

"""

from typing import TYPE_CHECKING
import pygame
from spectator import Spectator

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class SpectatorCrowd:
    """define the collection of Alien Sprites"""

    def __init__(self, game: 'AlienInvasion') -> None:

        # connect crowd to game environment
        self.game = game
        self.settings = game.settings
        self.crowd = pygame.sprite.Group()
        # self.spectator_crowd_direction: int = game.settings.spectator_crowd_direction
        # self.spectator_crowd_drop_speed: int = game.settings.spectator_crowd_drop_speed

        self.create_crowd()

    ##################################
    ### PREPARE AND POSITION FLEET ###
    def create_crowd(self) -> None:
        """determine initial dimensions of fleet within game boundaries"""
        spectator_w: int = self.settings.spectator_w
        screen_w: int = self.settings.screen_w

        crowd_w: int # how many aliens in each row/column of the fleet
        crowd_w = self.calculate_crowd_dimensions(spectator_w, screen_w)

        x_offset: int # in pixels, distance from edge of screen to crowd
        x_offset = self.calculate_offsets(spectator_w, screen_w, crowd_w)
        y_offset: int = 100 # add some space above to avoid HUD

        self._create_rectangle_crowd(spectator_w, crowd_w, x_offset, y_offset)

    def _create_rectangle_crowd(self,
                spectator_w,
                crowd_w,
                x_offset, y_offset) -> None:
        """generate individual spectators to fill space of the fleet"""
        current_y = y_offset # determine how far down to place the alien
        for col in range(crowd_w):
            current_x = (spectator_w * col) + x_offset # determine how far right to place alien
            if col % 2 == 0: # to create space between, skip odd numbers
                continue
            self._create_spectator(current_x, current_y)

    def calculate_offsets(self, spectator_w, screen_w, crowd_w) -> int:
        """determine positioning of and space between spectators within fleet"""
        crowd_horizontal_space: int = spectator_w * crowd_w
        x_offset: int = (screen_w - crowd_horizontal_space)//2
        return x_offset

    def calculate_crowd_dimensions(self, spectator_w, screen_w) -> int:
        """determine area to be occupied by crowd as a whole"""

        crowd_w: int = screen_w // spectator_w

        if crowd_w %2 == 0: # if even number of columns, trim 1
            crowd_w -= 1
        else:               # otherwise trim 2
            crowd_w -= 2

        return crowd_w

    def _create_spectator(self, current_x: int, current_y: int) -> None:
        """add an individual alien to the fleet at specific position"""
        new_spectator: Spectator = Spectator(self, current_x, current_y)
        self.crowd.add(new_spectator)

    #################
    ### GAME PLAY ###
    ### REPRESENT FLEET ON THE SCREEN ###
    def update_crowd(self) -> None:
        """per clock, update motion/position for entire fleet"""
        self.crowd.update()

    def draw(self) -> None:
        """per clock, update motion/position for each alien"""
        spectator: 'Spectator'
        for spectator in self.crowd:
            spectator.draw_spectator()

    ### CHECK IF FLEET HAS HIT AMMO OR SHIP
    def check_laser_collisions(self, other_group) -> dict:
        """use built-in pygame method to 
        * determine whether spectator crowd has collided with a laser
        * remove spectator + bullet"""
        return pygame.sprite.groupcollide(other_group, self.crowd, True, True)

    def check_cannon_collisions(self, other_group) -> dict:
        """use built-in pygame method to 
        * determine whether spectator crowd has collided with a cannon
        * remove spectator"""
        return pygame.sprite.groupcollide(other_group, self.crowd, False, True)

    def check_destroyed_status(self) -> bool:
        """report whether any spectators remain within the total crowd"""
        return not self.crowd
