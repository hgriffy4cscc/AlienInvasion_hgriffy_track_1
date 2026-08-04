"""create button to begin the game
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
from typing import TYPE_CHECKING
import pygame.font

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Button():
    """create and manage button to begin the game"""

    def __init__(self, game: 'AlienInvasion') -> None:
        self.game: AlienInvasion = game
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.settings = game.settings

        self.play_button_font = pygame.font.Font(self.settings.font_file, self.settings.button_font_size)
        self.rules_font = pygame.font.Font(self.settings.font_file, self.settings.rules_font_size)

        # build holders and objects
        self.play_button_rect = pygame.Rect(0,0, self.settings.play_button_w, self.settings.play_button_h)
        self.play_button_rect.center = self.boundaries.center
        self.rules_rect = pygame.Rect(0,0, self.settings.rules_box_w, self.settings.rules_box_h)
        self.rules_rect.center = self.boundaries.center
        self._prep_rules_msg(self.settings.the_rules)
        self._prep_play_msg(self.settings.button_msg)

    def _prep_play_msg(self, msg):
        self.play_msg_image = self.play_button_font.render(msg, True, self.settings.text_color, None)
        self.play_msg_image_rect = self.play_msg_image.get_rect()
        self.play_msg_image_rect.center = self.play_button_rect.center

    def _prep_rules_msg(self, msg):
        print(msg)
        self.rules_msg_image = self.rules_font.render(msg, True, self.settings.text_color, None)
        self.rules_msg_image_rect = self.rules_msg_image.get_rect()
        self.rules_msg_image_rect.center = self.rules_rect.center

    def draw(self) -> None:
        """put the play button and rules object on the screen"""
        # the rules object
        self.screen.fill(self.settings.rules_box_color, self.rules_rect)
        self.screen.blit(self.rules_msg_image, self.rules_msg_image_rect)

        # the button object
        self.screen.fill(self.settings.play_button_color, self.play_button_rect)
        self.screen.blit(self.play_msg_image, self.play_msg_image_rect)

    def check_clicked(self, mouse_pos) -> bool:
        """determine if user has clicked button"""
        return self.play_button_rect.collidepoint(mouse_pos)
