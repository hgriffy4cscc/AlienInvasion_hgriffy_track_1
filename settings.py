"""file to hold durable settings for Alien Invasion and related games"""

from pathlib import Path

class Settings:
    """class for game-wide settings"""

    def __init__(self) -> None:

        # game screen and environment
        self.name: str = "Track 1: Alien Invasion w Cannon Ammo + Spectators"
        self.screen_w: int = 1200
        self.screen_h: int = 1000
        self.FPS: int = 60
        self.difficulty_scale = 1.1
        self.images_path: Path = Path.cwd() / 'Assets' / 'images'
        self.bg_file: Path = self.images_path / 'webb_butterfly_lg.jpg'
        self.scores_file: Path = Path.cwd() / 'Assets' / 'file' / 'scores.json'

        # ship
        self.ship_file: Path = self.images_path / 'ship2(no bg).png'
        self.ship_w: int = 40
        self.ship_h: int = 60
        self.starting_ship_count = 3

        # bullet: lasers
        self.bullet_file: Path = self.images_path / 'laserBlast.png'
        self.bullet_sound_file: Path = Path.cwd() / 'Assets' / 'sound' / 'laser.mp3'
        self.impact_sound_file: Path = Path.cwd() / 'Assets' / 'sound' / 'impactSound.mp3'

        # bullet: cannon
        self.cannon_file: Path = self.images_path / 'cannonball_PNG19.png'
        self.cannon_sound_file: Path = Path.cwd() / 'Assets' / 'sound' / 'freesound_community-cannonball-89596.mp3'
        self.cannon_impact_sound_file: Path = Path.cwd() / 'Assets' / 'sound' / 'impactSound.mp3'
        
        # alien
        self.alien_file: Path = self.images_path / 'enemy_4.png'
        self.alien_fleet_direction = 1

        # button to start game
        self.button_w = 300
        self.button_h = 75
        self.button_color = (0, 135, 50)

        # HUD
        self.text_color = (255, 255, 255)
        self.button_font_size = 48
        self.HUD_font_size = 20
        self.font_file = Path.cwd() / 'Assets' / 'Fonts' / 'Silkscreen' / 'Silkscreen-Bold.ttf'

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """settings for game elements that may change between levels"""
        # ship
        self.ship_speed: int = 5

        # bullets: lasers
        self.laser_w = 25
        self.laser_h = 80
        self.laser_speed = 7
        self.laser_count = 5

        # bullets: cannon
        self.cannon_w = 25
        self.cannon_h = 25
        self.cannon_arsenal_max = 1
        self.cannon_gravity = 100
        self.cannon_initial_velocity = 600

        # aliens
        self.alien_w = 40
        self.alien_h = 40
        self.alien_fleet_speed = 3
        self.alien_fleet_drop_speed = 20

        self.alien_points = 50

    def increase_difficulty(self):
        self.ship_speed *= self.difficulty_scale
        self.laser_speed *= self.difficulty_scale
        self.alien_fleet_speed *= self.difficulty_scale
