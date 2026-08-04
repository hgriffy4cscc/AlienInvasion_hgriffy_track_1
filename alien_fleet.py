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
        self.alien_fleet_direction = game.settings.alien_fleet_direction
        self.alien_fleet_drop_speed = game.settings.alien_fleet_drop_speed
        
        self.create_fleet()

    ##################################
    ### PREPARE AND POSITION FLEET ###
    def create_fleet(self):
        """determine initial dimensions of fleet within game boundaries"""
        alien_w = self.settings.alien_w
        alien_h = self.settings.alien_h
        screen_w = self.settings.screen_w
        screen_h = self.settings.screen_h

        fleet_w, fleet_h = self.calculate_fleet_dimensions(alien_w, screen_w, alien_h, screen_h)

        x_offset, y_offset = self.calculate_offsets(alien_w, alien_h, screen_w, fleet_w, fleet_h)

        self._create_rectangle_fleet(alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset)

    def _create_rectangle_fleet(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset):
        """generate individual aliens to fill space of the fleet"""
        for row in range(fleet_h):
            current_y = (alien_h * row) + y_offset
            for col in range(fleet_w):
                current_x = (alien_w * col) + x_offset
                if col % 2 == 0 or row % 2 == 0:
                    continue
                self._create_alien(current_x, current_y)

    def calculate_offsets(self, alien_w, alien_h, screen_w, fleet_w, fleet_h):
        """determine positioning of and space between aliens within fleet"""
        half_screen = self.settings.screen_h // 2
        fleet_horizontal_space = alien_w * fleet_w
        fleet_vertical_space = alien_h * fleet_h
        x_offset = int((screen_w - fleet_horizontal_space)//2)
        y_offset = int((half_screen - fleet_vertical_space)//2)
        return x_offset,y_offset

    def calculate_fleet_dimensions(self, alien_w, screen_w, alien_h, screen_h):
        """determine area to be occupied by fleet as a whole"""

        fleet_w = (screen_w // alien_w)
        fleet_h = ((screen_h / 2) // alien_h)
                   
        if fleet_w %2 == 0: # if even number of columns
            fleet_w -= 1
        else:
            fleet_w -+ 2
        
        if fleet_h %2 == 0: # if even number of rows
            fleet_h -= 1
        else:
            fleet_h -= 2

        return int(fleet_w), int(fleet_h)

    def _create_alien(self, current_x: int, current_y: int):
        """add an individual alien to the fleet at specific position"""
        new_alien = Alien(self, current_x, current_y)
        self.fleet.add(new_alien)

    #################
    ### GAME PLAY ###
    def _check_fleet_edges(self):
        """determine if fleet has reached side edge of game screen"""
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self.alien_fleet_direction *= -1
                self._drop_alien_fleet()
                break
                # self.y += self.settings.alien_fleet_drop_speed

    def check_fleet_bottom(self):
        """determine if fleet has reached bottom of game space"""
        alien: Alien
        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_h:
                return True
                break
        return False

    def _drop_alien_fleet(self):
        """move fleet down when it has reached screen side edge"""
        for alien in self.fleet:
            alien.y += self.settings.alien_fleet_drop_speed

    ### REPRESENT FLEET ON THE SCREEN ###
    def update_fleet(self):
        """per clock, update motion/position for entire fleet"""
        self._check_fleet_edges()
        self.fleet.update()

    def draw(self):
        """per clock, update motion/position for each alien"""
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()

    ### CHECK IF FLEET HAS HIT AMMO OR SHIP
    def check_collisions(self, other_group):
        """report whether alien fleet has collided with a bullet or the main ship"""
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)
    
    def check_destroyed_status(self):
        """report whether any aliens remain within the total fleet"""
        return not self.fleet
