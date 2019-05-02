import pygame

class Settings():
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship setting
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 10
        self.bullet_color = 250, 90, 30
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.3

        # How quickly the alien point values increase
        self.score_scale = 1.5

        # File to store scores
        self.score_storage = "scores.csv"

        # Images of sound on/off buttons
        self.sound_on_button = "images\\sound_on.bmp"
        self.sound_off_button = "images\\sound_off.bmp"

        # Limit of score records printed on leader board
        self.score_records_limit = 20

        # Sounds
        # Sound of ship's shot
        self.shot_sound = pygame.mixer.Sound("sounds\\shot.wav")
        # Sound for cursor hovering on button
        self.button_direct_sound = pygame.mixer.Sound("sounds\\button_direct.wav")
        # Sound for ship hit
        self.ship_hit_sound = pygame.mixer.Sound("sounds\\ship_hit.wav")
        # Sound when entire fleet destroyed
        self.level_up_sound = pygame.mixer.Sound("sounds\\success.wav")
        # Sound for game starting
        self.game_start_sound = pygame.mixer.Sound("sounds\\game_start.wav")

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 2
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1.5

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 5

    def increase_speed(self):
        """Increase speed settings and alien point value."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
