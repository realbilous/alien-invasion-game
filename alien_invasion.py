import os

import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
import game_funtions as gf
from button import Button
from scoreboard import Scoreboard
from score import Score

def run_game():
    # Center window that will be created
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Initialize pygame, settings and screen object.
    pygame.init()
    app_settings = Settings()
    screen = pygame.display.set_mode((app_settings.screen_width,
                                      app_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    # Make a ship, a group of bullets, and a group of aliens
    ship = Ship(app_settings, screen)
    bullets = Group()
    aliens = Group()

    # Create the fleet of aliens.
    gf.create_fleet(app_settings, screen, ship, aliens)

    # Create an instance to store game statistics and create a scoreboard
    stats = GameStats(app_settings)
    sb = Scoreboard(app_settings, screen, stats)

    # Make buttons
    play_button = Button(app_settings, screen, "Play")
    scores_button = Button(app_settings, screen, "Scores")
    exit_button = Button(app_settings, screen, "Exit")
    sound_on_button = Button(app_settings, screen,
                             img_path=app_settings.sound_on_button)
    sound_off_button = Button(app_settings, screen,
                              img_path=app_settings.sound_off_button)

    # Make an object for managing scores
    scores = Score(app_settings, stats)

    # Start the main loop for the game.
    while True:
        gf.check_events(app_settings, screen, stats, scores, sb, play_button,
                        scores_button, exit_button, sound_on_button, ship,
                        aliens, bullets)
        if not stats.pause:
            if stats.game_active:
                ship.update()
                gf.update_bullets(app_settings, screen, stats, sb,
                                  ship, aliens, bullets)
                gf.update_aliens(app_settings, stats, sb,
                                 screen, ship, aliens, bullets)

            gf.update_screen(app_settings, screen, stats, scores, sb, ship,
                             aliens, bullets, play_button, scores_button,
                             exit_button, sound_on_button, sound_off_button)

run_game()
