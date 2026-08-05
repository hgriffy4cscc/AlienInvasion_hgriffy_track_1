"""Class to represent group of aliens in the game"""

# Python modules
from typing import TYPE_CHECKING
# Installed modules
import pygame
# Custom/game modules
from spectator import Spectator

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class SpectatorCrowd:
    """Defines the collection of Spectator Sprites"""

    def __init__(self, game: 'AlienInvasion') -> None:

        # connect crowd to game environment
        self.game: AlienInvasion = game
        self.settings = game.settings
        self.crowd: pygame.sprite.Group = pygame.sprite.Group()

        self.create_crowd()

    ##################################
    ### PREPARE AND POSITION CROWD ###
    def create_crowd(self) -> None:
        """Determine initial dimensions of crowd within game boundaries
                
                Effects:
                    Adds a collection of Spectator sprites to the game, numbered and arranged
                    in a single row near the top of the screen.
        """
        spectator_w: int = self.settings.spectator_w
        screen_w: int = self.settings.screen_w

        crowd_w: int = self.calculate_crowd_dimensions(spectator_w, screen_w)

        x_offset: int # in pixels, distance from edge of screen to crowd
        x_offset: int = self.calculate_offsets(spectator_w, screen_w, crowd_w)
        y_offset: int = 100 # add some space above to avoid HUD

        self._create_rectangle_crowd(spectator_w, crowd_w, x_offset, y_offset)

    def _create_rectangle_crowd(self,
                spectator_w,
                crowd_w,
                x_offset, y_offset) -> None:
        """Generates individual spectator sprites to fill space of the crowd
                
                Params:
                    spectator_w: Width in pixels for the image and rect for each sprite.
                    crowd_w: The number of alien sprites in the row.
                    x_offset, y_offset: The distance in pixels from the left and top of the screen to begin
                
                Effects:
                    Generates and aligns a sprite group of spectator sprites in a row.
        """
        current_y: int = y_offset # determine how far down to place the alien
        for col in range(crowd_w):
            current_x: int = (spectator_w * col) + x_offset # determine how far right to place alien
            if col % 2 == 0: # to create space between, skip odd numbers
                continue
            self._create_spectator(current_x, current_y)

    def calculate_offsets(self, spectator_w, screen_w, crowd_w) -> int:
        """Determines positioning of and space between spectators within crowd.
                
                Params:
                    spectator_w: Width in pixels for the image and rect for each sprite.
                    screen_w: Width in pixels of the entire screen
                    crowd_w: The number of spectator sprites in the row.
        
                Returns:
                    x_offset: the horizontal distance from screen edge to begin creating sprites
                """
        crowd_horizontal_space: int = spectator_w * crowd_w
        x_offset: int = (screen_w - crowd_horizontal_space)//2
        return x_offset

    def calculate_crowd_dimensions(self, spectator_w, screen_w) -> int:
        """Determines number of sprites to include in the crowd row.
                
                Params:
                    spectator_w: Width in pixels for the image and rect for each sprite
                    screen_w: Width in pixels of the entire screen
        
                Returns:
                    crowd_w: the number of alien sprites to create in each row and column
        """
        crowd_w: int = screen_w // spectator_w

        if crowd_w %2 == 0: # if even number of columns, trim 1
            crowd_w -= 1
        else:               # otherwise trim 2
            crowd_w -= 2

        return crowd_w

    def _create_spectator(self, current_x: int, current_y: int) -> None:
        """Adds an individual spectator sprite to the crowd group at specific position.
                
                Params:
                    current_x, current_y: The horizontal and vertical position for the sprite on the screen.
        
                Effects:
                    Appends one new spectator sprite to the sprite group.
                """
        new_spectator: Spectator = Spectator(self, current_x, current_y)
        self.crowd.add(new_spectator)

    #################
    ### GAME PLAY ###
    ### REPRESENT FLEET ON THE SCREEN ###
    def update_crowd(self) -> None:
        """Per clock tick, updates screen representation for the group.
                
                Effects:
                    Prepares screen image to be displayed at next clock tick.
                """
        self.crowd.update()

    def draw(self) -> None:
        """Per clock tick, generates screen image for each spectator sprite."""
        spectator: 'Spectator'
        for spectator in self.crowd:
            spectator.draw_spectator()

    ### CHECK IF FLEET HAS HIT AMMO OR SHIP
    def check_laser_collisions(self, other_group) -> dict:
        """Uses built-in pygame method to determine whether spectator crowd has collided with a laser.
                
                Params:
                    other_group: Any collection of laser sprites in the game.
        
                Returns:
                    [dict]: JSON object listing sprites that collided.
        
                Effects:
                    Remove spectator sprite + laser sprite from their respective sprite groups.
                """
        return pygame.sprite.groupcollide(other_group, self.crowd, True, True)

    def check_cannon_collisions(self, other_group) -> dict:
        """Uses built-in pygame method to determine whether spectator crowd has collided with a cannonball.
                
        Params:
            other_group: Any collection of cannon sprites in the game.

        Returns:
            [dict]: JSON object listing sprites that collided.

        Effects:
            Remove spectator sprite + cannonball sprite from their respective sprite groups.
        """
        return pygame.sprite.groupcollide(other_group, self.crowd, False, True)

    def check_destroyed_status(self) -> bool:
        """Reports whether any spectators remain within the total crowd"""
        return not self.crowd
