"""alien_invasion.py

This project customizes the Alien Invasion game
by modifying the ammunition fired by the ship to follow gravitational arcs
and by introducing another set of entities representing friendlies
who need to be spared from the falling ammo.
Also, a pause in game action (on pressing the p key)

Resources:
    * course materials (obvi)
    * cannonball image for ammo from https://pngimg.com/image/108039
        license: attribution non commercial
    * cannon sound for ammo from https://pixabay.com/sound-effects/film-special-effects-cannonball-89596/
        license: free for use

Todo:
    o re-enable alien + alien fleet
    o add cost and score data for alien + alien fleet
    o add spectators (~= aliens + cost and score)
"""

import sys
import pygame
from time import sleep
from settings import Settings
from ship import Ship
from arsenal import Arsenal
from alien import Alien
from alien_fleet import AlienFleet
# from button import Button
# from game_stats import GameStats
# from hud import HUD

class AlienInvasion:
    """class to manage the entire game"""

    def __init__(self) -> None:

        # invoke pygame and set things up
        pygame.init()
        self.settings = Settings()
        # self.game_stats = GameStats(self)

        ### build the screen
        self.screen = pygame.display.set_mode(
            (self.settings.screen_w,self.settings.screen_h)
            )
        pygame.display.set_caption(self.settings.name)
        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg,
            (self.settings.screen_w,self.settings.screen_h)
            )
        # self.HUD = HUD(self)

        # set things in motion
        self.running: bool = True
        self.clock = pygame.time.Clock()

        # add some sounds
        self._initialize_game_sounds()

        # add ship and other game entities
        self.initialize_game_entities()

        # self.play_button = Button(self, 'Play')
        self.game_active: bool = True

        # enable player to pause the aliens to catch up
        self.pause_aliens: bool = False

    def run_game(self) -> None:
        """core method to coordinate the game -- called from top level of the program"""
        # Game Loop
        while self.running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                if not self.pause_aliens:
                    self.alien_fleet.update_fleet()
                self._check_game_collisions()
            self._update_screen()
            self.clock.tick(self.settings.FPS)

    def initialize_game_entities(self) -> None:
        """initialize game entities"""
        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)
        self.alien_fleet.create_fleet()

    def _initialize_game_sounds(self) -> None:
        """prepare stuff to make sounds"""
        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.bullet_sound_file)
        self.laser_sound.set_volume(0.7)

        self.cannon_sound = pygame.mixer.Sound(self.settings.cannon_sound_file)
        self.cannon_sound.set_volume(0.7)

        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound_file)
        self.impact_sound.set_volume(0.8)
    
    def _check_game_collisions(self) -> None:
        """determine if any game entities have collided with any others"""
        # check ship collisions viz aliens
        if self.ship.check_collisions( self.alien_fleet.fleet):
            self._check_game_status()
            # de-increment 1 life

        # check aliens viz bottom of screen
        if self.alien_fleet.check_fleet_bottom():
            self._check_game_status()
        
        # check lasers viz aliens
        laser_collisions = self.alien_fleet.check_laser_collisions(self.ship.arsenal.laser_arsenal)
        cannon_collisions = self.alien_fleet.check_cannon_collisions(self.ship.arsenal.cannon_arsenal)
        if laser_collisions or cannon_collisions:
            self.impact_sound.play()
            self.impact_sound.fadeout(500)
            # self.game_stats.update(collisions)
            # self.HUD.update_scores()

        if self.alien_fleet.check_destroyed_status():
            self._reset_level()
            self.settings.increase_difficulty()
            # # update game stats for level
            # self.game_stats.update_level()
            # # update HUD view
            # self.HUD.update_level()

    def _check_game_status(self) -> None:
        """upon certain collisions, determine if game is over or if a new level should begin"""
        # if self.game_stats.ships_remaining > 0:
        #     self.game_stats.ships_remaining -= 1
        self._reset_level()
        sleep(0.5)
        # else:
        #     self.game_active = False

    def _reset_level(self) -> None:
        """trigger actions required to start a new level"""
        for arsenal in self.ship.arsenal.all_arsenals:
            arsenal.remove()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()

    def restart_game(self) -> None:
        """trigger actions to start a new game"""
        pass
        # self.settings.initialize_dynamic_settings()
        # self.game_stats.reset_stats()
        # self.HUD.update_scores()
        # self._reset_level()
        # self.ship._center_ship()
        # self.game_active = True
        # pygame.mouse.set_visible(False)


    def _update_screen(self) -> None:
        """implement steps to redraw the various game entities and make changes visible"""
        self.screen.blit(self.bg, (0,0))
        self.ship.draw()
        self.alien_fleet.draw()
        # self.HUD.draw()

        # if not self.game_active:
        #     self.play_button.draw()
        #     pygame.mouse.set_visible(True)
        pygame.display.flip()

    def _check_events(self) -> None:
        """monitor player input and respond accordingly"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # self.game_stats.save_scores()
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and self.game_active:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()

    def _check_button_clicked(self) -> None:
        """process when player clicks the start game button"""
        pass
        # mouse_pos = pygame.mouse.get_pos()
        # if self.play_button.check_clicked(mouse_pos):
        #     self.restart_game()

    def _check_keyup_events(self, event) -> None:
        """process when a key is released"""
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def _check_keydown_events(self, event) -> None:
        """process when a key is pressed"""
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_c:
            if self.ship.fire('cannon'):
                self.cannon_sound.play()
                self.cannon_sound.fadeout(1500)
        if event.key == pygame.K_SPACE:
            if self.ship.fire('laser'):
                self.laser_sound.play()
                self.laser_sound.fadeout(250)
        if event.key == pygame.K_q:
            self.running = False
            # self.game_stats.save_scores()
            pygame.quit()
            sys.exit()
        if event.key == pygame.K_p:
            if self.pause_aliens:
                self.pause_aliens = False
            else:
                self.pause_aliens = True

if __name__ == '__main__':
    """start the whole thing running"""
    ai = AlienInvasion()
    ai.run_game()
