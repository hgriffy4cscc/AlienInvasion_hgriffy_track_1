"""Displays selected game information on the screen."""

# Python modules
from typing import TYPE_CHECKING
# Installed modules
import pygame.font
# Custom/game modules
if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class HUD:
    """Displays selected information about the game to the player"""

    def __init__(self, game: 'AlienInvasion') -> None:
        self.game: AlienInvasion = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries: pygame.Rect = game.screen.get_rect()
        self.game_stats = game.game_stats
        self.font: pygame.font.Font = pygame.font.Font(self.settings.font_file,
                                     self.settings.HUD_font_size)
        self.screen_padding = 20
        # declare variables defined below
        self.score_str: str
        self.score_image: pygame.surface.Surface
        self.score_rect: pygame.rect.Rect
        self.max_score_str: str
        self.max_score_image: pygame.surface.Surface
        self.max_score_rect: pygame.rect.Rect
        self.hi_score_str: str
        self.hi_score_image: pygame.surface.Surface
        self.hi_score_rect: pygame.rect.Rect

        self.update_scores()
        self._setup_life_image()
        self.update_level()

    def _setup_life_image(self) -> None:
        """Creates images to represent how many 'lives' remain for player."""
        self.life_image = pygame.image.load(self.settings.ship_file)
        self.life_image = pygame.transform.scale(self.life_image,
                (self.settings.ship_w, self.settings.ship_h))
        self.life_rect = self.life_image.get_rect()

    def update_scores(self) -> None:
        """Updates display of various scores"""
        self._update_max_score()
        self._update_score()
        self._update_hi_score()

    def _update_score(self) -> None:
        """Updates current score in current game"""
        self.score_str = f'Score: {self.game_stats.score: ,.0f}'
        self.score_image = self.font.render(self.score_str, True, \
                self.settings.text_color, None)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.boundaries.right - self.screen_padding
        self.score_rect.top = self.max_score_rect.bottom + self.screen_padding

    def _update_max_score(self) -> None:
        """Updates highest score in current session."""
        self.max_score_str = f'Max Score: {self.game_stats.max_score: ,.0f}'
        self.max_score_image = self.font.render(self.max_score_str, True, \
                self.settings.text_color, None)
        self.max_score_rect = self.max_score_image.get_rect()
        self.max_score_rect.right = self.boundaries.right - self.screen_padding
        self.max_score_rect.top = self.boundaries.top + self.screen_padding

    def _update_hi_score(self) -> None:
        """Updates highest score across all sessions."""
        self.hi_score_str = f'High Score: {self.game_stats.hi_score: ,.0f}'
        self.hi_score_image = self.font.render(self.hi_score_str, True, \
                self.settings.text_color, None)
        self.hi_score_rect = self.hi_score_image.get_rect()
        self.hi_score_rect.midtop = (self.boundaries.centerx, \
                                     self.boundaries.top + self.screen_padding)

    def update_level(self) -> None:
        """Updates the number of alien fleets destroyed."""
        self.level_str = f'Level: {self.game_stats.game_level: ,.0f}'
        self.level_image = self.font.render(self.level_str, True, \
                self.settings.text_color, None)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.boundaries.left + self.screen_padding
        self.level_rect.top = self.life_rect.bottom + self.screen_padding

    def _draw_lives(self) -> None:
        """Represent the 'lives' count on the screen."""
        current_x = self.screen_padding
        current_y = self.screen_padding
        for _ in range(self.game_stats.ships_remaining):
            self.screen.blit(self.life_image, (current_x, current_y))
            current_x += self.life_rect.width + self.screen_padding

    def draw(self) -> None:
        """Stages all information for on-screen display."""
        self.screen.blit(self.hi_score_image, self.hi_score_rect)
        self.screen.blit(self.max_score_image, self.max_score_rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self._draw_lives()
