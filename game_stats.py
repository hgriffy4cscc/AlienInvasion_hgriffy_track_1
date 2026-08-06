"""Manages keeping + updating scores based on game events."""

# Python modules
from pathlib import Path
import json
from typing import TYPE_CHECKING
# Installed modules
import pygame
# Custom/game modules
if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from alien_fleet import AlienFleet
    from alien import Alien
    from spectator_crowd import SpectatorCrowd
    from spectator import Spectator
    from arsenal import Arsenal
    from bullet_laser import Laser
    from bullet_cannon import Cannon


class GameStats():
    """Manages keeping + updating scores based on game events."""

    def __init__(self, game: 'AlienInvasion') -> None:
        self.game: AlienInvasion = game
        self.settings = game.settings
        self.score: int = 0
        self.max_score: int = 0
        self.hi_score: int
        self.init_saved_scores()
        self.reset_stats()

    def init_saved_scores(self) -> None:
        """Updates score values from saved file (if saved)."""
        self.path: Path = self.settings.scores_file
        if self.path.exists():
            contents: str = self.path.read_text()
            if not contents:
                contents = '{}'
            scores: dict = json.loads(contents)
            self.hi_score = scores.get('hi_score', 0)
        else:
            self.hi_score = 0
            self.save_scores()

    def save_scores(self) -> None:
        """Writes non-session scores to file for future retrieval.
        
        Effects:
            File created (or exception raised)
        """
        scores: dict = {
            'hi_score': self.hi_score
        }
        contents = json.dumps(scores, indent=4)
        try:
            self.path.write_text(contents)
        except FileNotFoundError as e:
            print(f'File Not Found: {e.filename2}')

    def reset_stats(self) -> None:
        """When game restarted (not launched), reset scores accordingly."""
        self.ships_remaining = self.settings.ship_count
        self.game_level = 1
        self.score = 0

    def update(self, collisions = None, bullet = None) -> None:
        """Based on game events, update scores (via sub-functions).
        
        Params:
            collisions [dict]: list of sprites involved in collisions to be scored.
            bullet [Laser | Cannon]: bullet fired in game to be scored
        """
        print(f'Score after: {self.score}')
        # update score if triggerd by collision
        if collisions:
            self._update_score_for_collisions(collisions)
        # update score if triggerd by bullet firing
        if bullet:
            self._update_score_for_cost(bullet)
        print(f'Score after: {self.score}')
        # update max_score
        self._update_max_score()
        # update high_score
        self._update_hi_score()

    def _update_score_for_collisions(self, collisions: dict) -> None:
        """Update score for current game.
        
        Params:
            collisions: dictionary of sprites involved in collisions to be scored.
        """
        other_group: AlienFleet | SpectatorCrowd
        sprite: Alien | Spectator
        for other_group in collisions.values():
            for sprite in other_group:
                self.score += sprite.points
        # print(f'Score: {self.score}')

    def _update_score_for_cost(self, bullet) -> None:
        """Update score for current game to reflect cost of ammunition.
        
        Params:
            bullet: sprite representing bullet fired.
        """
        self.score -= bullet.cost
        # print(f'Score: {self.score}')

    def _update_max_score(self) -> None:
        """Update the highest score for this session."""
        if self.score > self.max_score:
            self.max_score = self.score
        # print(f'Max: {self.max_score}')

    def _update_hi_score(self) -> None:
        """Update the all-time highest score."""
        if self.score > self.hi_score:
            self.hi_score = self.score

    def update_level(self) -> None:
        """Update indicator that level completed."""
        self.game_level += 1
        # print(f'Level: {self.game_level}')
