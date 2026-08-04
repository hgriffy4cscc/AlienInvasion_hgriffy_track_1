"""file to hold durable settings for Alien Invasion and related games
Depends on:
* none

Is Depended on:
* all

Basic (__init__) Properties contain: ('display variables' = file path + sizing + color)
* game:
    * screen dimensions + clock speed
    * initial difficulties
    * top-level Path variables
* ship:
    * display variables
    * ship count
* bullets: laser + cannon
    * display variables
* alien:
    * display variables
* HUD + control button:
    * display variables

Dynamic Properties contain:
* ship:
    * motion
* bullets: laser + cannon
    * size
    * motion parameters
    * cost
* aliens:
    * size
    * motion parameters
    * points


Methods control:
* changing settings between rounds to increase difficulty

"""

from pathlib import Path

class Settings:
    """class for game-wide settings"""

    def __init__(self) -> None:

        # game screen and environment
        self.name: str = "Track 1: Alien Invasion w Cannon Ammo + Spectators"
        self.screen_w: int = 1200
        self.screen_h: int = 1000
        self.FPS: int = 60
        self.difficulty_scale: float = 1.1

        # define some standard paths (for shorter lines)
        self.images_path: Path = Path.cwd() / 'Assets' / 'images'
        self.sound_path: Path = Path.cwd() / 'Assets' / 'sound'
        self.fonts_path: Path = Path.cwd() / 'Assets' / 'Fonts'
        self.bg_file: Path = self.images_path / 'webb_butterfly_lg.jpg'
        self.scores_file: Path = Path.cwd() / 'Assets' / 'file' / 'scores.json'

        # ship
        self.ship_file: Path = self.images_path / 'ship2(no bg).png'
        self.ship_w: int = 40
        self.ship_h: int = 60
        self.starting_ship_count: int = 3

        # bullet: lasers
        self.bullet_file: Path = self.images_path / 'laserBlast.png'
        self.bullet_sound_file: Path = self.sound_path / 'laser.mp3'
        self.impact_sound_file: Path = self.sound_path / 'impactSound.mp3'

        # bullet: cannon
        self.cannon_file: Path = self.images_path / 'cannonball_PNG19.png'
        self.cannon_sound_file: Path = self.sound_path / 'freesound_community-cannonball-89596.mp3'
        self.cannon_impact_sound_file: Path = self.sound_path / 'impactSound.mp3'

        # alien
        self.alien_file: Path = self.images_path / 'enemy_4.png'
        self.alien_fleet_direction: int = 1

        # spectator
        self.spectator_file: Path = self.images_path / 'enemy_4.png'
        self.spectator_fleet_direction: int = 1

        # button to start game
        self.button_w: int = 300
        self.button_h: int = 75
        self.button_color: tuple[int, int, int] = (0, 135, 50)

        # HUD
        self.text_color: tuple[int, int, int] = (255, 255, 255)
        self.button_font_size: int = 48
        self.HUD_font_size: int = 20
        self.font_file: Path = self.fonts_path / 'Silkscreen' / \
            'Silkscreen-Bold.ttf'

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self) -> None:
        """settings for game elements that may change between levels"""
        # ship
        self.ship_speed: int = 5

        # bullets: lasers
        self.laser_w: int = 25
        self.laser_h: int = 80
        self.laser_speed: int = 7
        self.laser_arsenal_max: int = 5
        self.laser_cost: int = 10

        # bullets: cannon
        self.cannon_w: int = 25
        self.cannon_h: int = 25
        self.cannon_arsenal_max: int = 1
        self.cannon_cost: int = 40
        self.cannon_gravity: int = 100
        self.cannon_initial_velocity: int = 550

        # aliens
        self.alien_w: int = 60
        self.alien_h: int = 60
        self.alien_fleet_speed: int = 3
        self.alien_fleet_drop_speed: int = 20
        self.alien_points: int = 50

        # spectators
        self.spectator_w: int = 60
        self.spectator_h: int = 60
        self.spectator_points: int = -500

    def increase_difficulty(self) -> None:
        """when player completes a round, make game more difficult"""
        self.ship_speed *= round(self.difficulty_scale)
        self.laser_speed *= round(self.difficulty_scale)
        self.alien_fleet_speed *= round(self.difficulty_scale)
