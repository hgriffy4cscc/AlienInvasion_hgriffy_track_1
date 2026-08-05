"""keep track of scores and components thereof
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
from pathlib import Path
import json

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class GameStats():
    """manage scores and other statistics about gameplay"""

    def __init__(self, game: 'AlienInvasion') -> None:
        self.game = game
        self.settings = game.settings
        self.score: int = 0
        self.max_score: int = 0
        self.hi_score: int
        self.init_saved_scores()
        self.reset_stats()

    def init_saved_scores(self) -> None:
        """update score values from saved file (if saved)"""
        self.path: Path = self.settings.scores_file
        if self.path.exists():
            contents: str = self.path.read_text()
            if not contents:
                contents = '{}'
            scores = json.loads(contents)
            self.hi_score = scores.get('hi_score', 0)
        else:
            self.hi_score = 0
            self.save_scores()

    def save_scores(self) -> None:
        """write non-session scores to file for future retrieval"""
        scores = {
            'hi_score': self.hi_score
        }
        contents = json.dumps(scores, indent=4)
        try:
            self.path.write_text(contents)
        except FileNotFoundError as e:
            print(f'File Not Found: {e.filename2}')

    def reset_stats(self) -> None:
        """when game restarted (not launched) reset scores"""
        self.ships_remaining = self.settings.ship_count
        self.game_level = 1
        self.score = 0

    def update(self, collisions) -> None:
        """based on game events update scores (via sub-functions)"""
        # update score
        self._update_score(collisions)
        # update max_score
        self._update_max_score()
        # update high_score
        self._update_hi_score()

    def _update_score(self, collisions) -> None:
        """update score for current game"""
        for other_group in collisions.values():
            for sprite in other_group:
                self.score += sprite.points
        # print(f'Score: {self.score}')

    def _update_max_score(self) -> None:
        """update the highest score for this session"""
        if self.score > self.max_score:
            self.max_score = self.score
        # print(f'Max: {self.max_score}')

    def _update_hi_score(self) -> None:
        """update the all-time highest score"""
        if self.score > self.hi_score:
            self.hi_score = self.score

    def update_level(self) -> None:
        """when level completed update"""
        self.game_level += 1
        # print(f'Level: {self.game_level}')
