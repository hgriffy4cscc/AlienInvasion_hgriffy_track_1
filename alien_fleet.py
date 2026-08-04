"""class to represent group of aliens in the game
Depends on:
* settings.py
* alien.py

Is Depended on:
* alien_invasion.py
* alien.py

Properties contain:
* fleet dimensions + position
* fleet motion parameters

Methods control:
* triggers creation of aliens
* drawing on screen
* motion
* collisions
* existence of fleet

"""

import pygame
from alien import Alien
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    

class AlienFleet:

    def __init__(self, game: 'AlienInvasion') -> None:

        # connect fleet to game environment
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.alien_fleet_direction: int = game.settings.alien_fleet_direction
        self.alien_fleet_drop_speed: int = game.settings.alien_fleet_drop_speed
        
        self.create_fleet()

    ##################################
    ### PREPARE AND POSITION FLEET ###
    def create_fleet(self) -> None:
        """determine initial dimensions of fleet within game boundaries"""
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

    def _create_rectangle_fleet(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset) -> None:
        """generate individual aliens to fill space of the fleet"""
        for row in range(fleet_h):
            current_y = (alien_h * row) + y_offset # determine how far down to place the alien
            for col in range(fleet_w):
                current_x = (alien_w * col) + x_offset # determine how far right to place alien
                if col % 2 == 0 or row % 2 == 0: # to create space between, skip odd numbers
                    continue
                self._create_alien(current_x, current_y)

    def calculate_offsets(self, alien_w, alien_h, screen_w, fleet_w, fleet_h) -> tuple[int, int]:
        """determine positioning of and space between aliens within fleet"""
        half_screen: int = self.settings.screen_h // 2
        fleet_horizontal_space: int = alien_w * fleet_w
        fleet_vertical_space: int = alien_h * fleet_h
        x_offset: int = (screen_w - fleet_horizontal_space)//2
        y_offset: int = (half_screen - fleet_vertical_space)//2
        return x_offset, y_offset

    def calculate_fleet_dimensions(self, alien_w, screen_w, alien_h, screen_h) -> tuple[int, int]:
        """determine area to be occupied by fleet as a whole"""

        fleet_w: int = screen_w // alien_w
        fleet_h: int = (screen_h // 2) // alien_h
                   
        if fleet_w %2 == 0: # if even number of columns, trim 1
            fleet_w -= 1
        else:               # otherwise trim 2
            fleet_w -+ 2
        
        if fleet_h %2 == 0: # if even number of rows, trim 1
            fleet_h -= 1
        else:               # otherwise trim 2
            fleet_h -= 2

        return fleet_w, fleet_h

    def _create_alien(self, current_x: int, current_y: int) -> None:
        """add an individual alien to the fleet at specific position"""
        new_alien: Alien = Alien(self, current_x, current_y)
        self.fleet.add(new_alien)

    #################
    ### GAME PLAY ###
    ### REPRESENT FLEET ON THE SCREEN ###
    def update_fleet(self) -> None:
        """per clock, update motion/position for entire fleet"""
        self._reverse_fleet_at_screen_edge()
        self.fleet.update()

    def draw(self) -> None:
        """per clock, update motion/position for each alien"""
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()

    def _reverse_fleet_at_screen_edge(self) -> None:
        """determine if fleet has reached side edge of game screen + reverse if so"""
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self.alien_fleet_direction *= -1
                self._drop_alien_fleet()
                break

    def check_fleet_bottom(self) -> bool:
        """determine + report if fleet has reached bottom of game space"""
        alien: Alien
        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_h:
                return True
        return False

    def _drop_alien_fleet(self) -> None:
        """move fleet down when it has reached screen side edge"""
        alien: Alien
        for alien in self.fleet:
            alien.y += self.settings.alien_fleet_drop_speed

    ### CHECK IF FLEET HAS HIT AMMO OR SHIP
    def check_laser_collisions(self, other_group) -> dict:
        """use built-in pygame method to 
        * determine whether alien fleet has collided with a laser
        * remove alien + bullet"""
        return pygame.sprite.groupcollide(other_group, self.fleet, True, True)
     
    def check_cannon_collisions(self, other_group) -> dict:
        """use built-in pygame method to 
        * determine whether alien fleet has collided with a laser
        * remove alien + bullet"""
        return pygame.sprite.groupcollide(other_group, self.fleet, False, True)
     
    def check_destroyed_status(self) -> bool:
        """report whether any aliens remain within the total fleet"""
        return not self.fleet
