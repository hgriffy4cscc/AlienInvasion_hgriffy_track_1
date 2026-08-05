"""Class to represent group of aliens in the game"""

# Python modules
from typing import TYPE_CHECKING
# Installed modules
import pygame
# Custom/game modules
from alien import Alien

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class AlienFleet:
    """Defines the collection of Alien Sprites"""

    def __init__(self, game: 'AlienInvasion') -> None:

        # connect fleet to game environment
        self.game: AlienInvasion = game
        self.settings = game.settings
        self.fleet: pygame.sprite.Group = pygame.sprite.Group()
        self.alien_fleet_direction: int = game.settings.alien_fleet_direction
        self.alien_fleet_drop_speed: int = game.settings.alien_fleet_drop_speed

        self.create_fleet()

    ##################################
    ### PREPARE AND POSITION FLEET ###
    def create_fleet(self) -> None:
        """Determine initial dimensions of fleet within game boundaries
        
        Effects:
            Adds a collection of Alien sprites to the game, numbered and arranged to almost fill the top
            part of the screen in a rectangular formation.
        """
        alien_w: int = self.settings.alien_w
        alien_h: int = self.settings.alien_h
        screen_w: int = self.settings.screen_w
        screen_h: int = self.settings.screen_h

        fleet_w: int # how many aliens in each row/column of the fleet
        fleet_h: int
        fleet_w, fleet_h = self.calculate_fleet_dimensions(alien_w, screen_w, alien_h, screen_h)

        x_offset: int # in pixels, distance from edge of screen to fleet
        y_offset: int
        x_offset, y_offset = self.calculate_offsets(alien_w, alien_h, screen_w, fleet_w, fleet_h)

        self._create_rectangle_fleet(alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset)

    def _create_rectangle_fleet(self,
            alien_w: int, alien_h: int,
                fleet_w: int, fleet_h: int,
                x_offset: int, y_offset: int) -> None:
        """Generates individual alien sprites to fill space of the fleet
        
        Params:
            alien_w, alien_h: Width and height in pixels for the image and rect for each sprite.
            fleet_w, fleet_h: The number of alien sprites in each row and column.
            x_offset, y_offset: The distance in pixels from the left and top of the screen to begin
        
        Effects:
            Generates and aligns a sprite group of alien sprites in rows and columns.
        """
        for row in range(fleet_h):
            current_y = (alien_h * row) + y_offset # determine how far down to place the alien
            for col in range(fleet_w):
                current_x = (alien_w * col) + x_offset # determine how far right to place alien
                if col % 2 == 0 or row % 2 == 0: # to create space between, skip odd numbers
                    continue
                self._create_alien(current_x, current_y)

    def calculate_offsets(self, alien_w: int, alien_h: int, screen_w: int, fleet_w: int, fleet_h: int) -> tuple[int, int]:
        """Determines positioning of and space between aliens within fleet.
        
        Params:
            alien_w, alien_h: Width and height in pixels for the image and rect for each sprite.
            screen_w: Width in pixels of the entire screen
            fleet_w, fleet_h: The number of alien sprites in each row and column.

        Returns:
            [tuple]: the horizontal and vertical distances from screen edges to begin creating sprites
        """
        half_screen: int = self.settings.screen_h // 2
        fleet_horizontal_space: int = alien_w * fleet_w
        fleet_vertical_space: int = alien_h * fleet_h
        x_offset: int = (screen_w - fleet_horizontal_space)//2
        y_offset: int = (half_screen - fleet_vertical_space)//2
        return x_offset, y_offset

    def calculate_fleet_dimensions(self, alien_w: int, screen_w: int, alien_h: int, screen_h: int) -> tuple[int, int]:
        """Determines number of alien sprites to include in each row and column.
        
        Params:
            alien_w, alien_h: Width and height in pixels for the image and rect for each sprite.
            screen_w, screen_h: Width and height in pixels of the entire screen

        Returns:
            fleet_w, fleet_h [tuple]: the number of alien sprites to create in each row and column
        """
        fleet_w: int = screen_w // alien_w
        fleet_h: int = (screen_h // 2) // alien_h

        if fleet_w %2 == 0: # if even number of columns, trim 1
            fleet_w -= 1
        else:               # otherwise trim 2
            fleet_w -= 2

        if fleet_h %2 == 0: # if even number of rows, trim 1
            fleet_h -= 1
        else:               # otherwise trim 2
            fleet_h -= 2

        return fleet_w, fleet_h

    def _create_alien(self, current_x: int, current_y: int) -> None:
        """Adds an individual alien sprite to the fleet group at specific position.
        
        Params:
            current_x, current_y: The horizontal and vertical position for the sprite on the screen.

        Effects:
            Appends one new alien sprite to the sprite group.
        """
        new_alien: Alien = Alien(self, current_x, current_y)
        self.fleet.add(new_alien)

    #################
    ### GAME PLAY ###
    ### REPRESENT CROWD ON THE SCREEN ###
    def update_fleet(self) -> None:
        """Per clock tick, updates screen representation for entire fleet.
        
        Effects:
            Changes the location value for each sprite in the sprite group.
        """
        self._reverse_fleet_at_screen_edge()
        self.fleet.update()

    def draw(self) -> None:
        """Per clock tick, generates screen image for each alien sprite."""
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()

    def _reverse_fleet_at_screen_edge(self) -> None:
        """Determines if fleet has reached side edge of game screen + reverses direction if so.
        
        Effects:
            [if triggered]: Update value for direction.
            [if triggered]: Triggers method to change vertical location of alien fleet sprite group
        """
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self.alien_fleet_direction *= -1
                self._drop_alien_fleet()
                break

    def check_fleet_bottom(self) -> bool:
        """Determines + reports if fleet has reached bottom of game space.
        
        Returns:
            [bool]: True if any alien sprite touches the bottom edge of the screen, False otherwise.
        """
        alien: Alien
        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_h:
                return True
        return False

    def _drop_alien_fleet(self) -> None:
        """Moves fleet down when it has reached screen side edge"""
        alien: Alien
        for alien in self.fleet:
            alien.y += self.settings.alien_fleet_drop_speed

    ### CHECK IF FLEET HAS HIT AMMO OR SHIP
    def check_laser_collisions(self, other_group: pygame.sprite.Group) -> dict:
        """Uses built-in pygame method to determine whether alien fleet has collided with a laser.
        
        Params:
            other_group: Any collection of laser sprites in the game.

        Returns:
            [dict]: JSON object listing sprites that collided.

        Effects:
            Removes alien sprite + laser sprite from their respective sprite groups.
        """
        return pygame.sprite.groupcollide(other_group, self.fleet, True, True)

    def check_cannon_collisions(self, other_group) -> dict:
        """Uses built-in pygame method to determine whether alien fleet has collided with a cannonball.
        
        Params:
            other_group: Any collection of cannon sprites in the game.

        Returns:
            [dict]: JSON object listing sprites that collided.

        Effects:
            Remove alien sprite + cannonball sprite from their respective sprite groups.
        """
        return pygame.sprite.groupcollide(other_group, self.fleet, False, True)

    def check_destroyed_status(self) -> bool:
        """Reports whether any aliens remain within the total fleet."""
        return not self.fleet
