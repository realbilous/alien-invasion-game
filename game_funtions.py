import sys
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, app_settings, screen, stats, scores, sb,
                         ship, aliens, bullets):
    """Respond to keypresses"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(app_settings, stats, screen, ship, bullets)
    elif event.key == pygame.K_p:
        if not stats.menu_open:
            if not stats.pause:
                stats.pause = True
            else:
                stats.pause = False
    elif event.key == pygame.K_RETURN:
        if stats.menu_open:
            start_game(app_settings, screen, stats, scores,
                       sb, ship, aliens, bullets)
    elif event.key == pygame.K_ESCAPE:
        stats.menu_open = True
        stats.game_active = False
        stats.pause = False
        pygame.mouse.set_visible(True)


def fire_bullet(app_settings, stats, screen, ship, bullets):
    """Fire a bullet if limit not reached yet"""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < app_settings.bullets_allowed and not stats.pause:
        new_bullet = Bullet(app_settings, screen, ship)
        if stats.sounds_on:
            pygame.mixer.Sound.play(app_settings.shot_sound)
        bullets.add(new_bullet)


def check_keyup_evenets(event, ship):
    """Respond to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(app_settings, screen, stats, scores, sb, play_button,
                 scores_button, exit_button, sound_on_button, ship, aliens,
                 bullets):
    """Respond to key and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, app_settings, screen, stats, scores,
                                 sb, ship, aliens, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_evenets(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(app_settings, screen, stats, scores, sb,
                              play_button, ship, aliens, bullets,
                              mouse_x, mouse_y)
            check_exit_button(stats, exit_button, mouse_x, mouse_y)
            check_scores_button(stats, scores_button, mouse_x, mouse_y)
            check_sound_button(stats, sound_on_button, mouse_x, mouse_y)
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_mouse_coord(app_settings, stats, mouse_x, mouse_y,
                              play_button, scores_button, exit_button)


def check_sound_button(stats, sound_on_button, mouse_x, mouse_y):
    """If sound button was clicked, change value of flag variable on opposite"""
    button_clicked = sound_on_button.image_rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and stats.menu_open:
        if stats.sounds_on:
            stats.sounds_on = False
        else:
            stats.sounds_on = True


def check_mouse_coord(app_settings, stats, mouse_x, mouse_y, *buttons):
    for button in buttons:
        button_directed = button.msg_rect.collidepoint(mouse_x, mouse_y)
        if button_directed and stats.menu_open:
            button.text_color = button.text_color_hover
            if button.cursor_directed != 2:
                button.cursor_directed = 1
        elif not button_directed and stats.menu_open:
            button.text_color = button.text_color_inactive
            button.cursor_directed = 3
        if button.cursor_directed == 1:
            button.cursor_directed = 2
            if stats.sounds_on:
                pygame.mixer.Sound.play(app_settings.button_direct_sound)


def check_play_button(app_settings, screen, stats, scores, sb, play_button, ship,
                      aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.msg_rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and stats.menu_open:
        start_game(app_settings, screen, stats, scores, sb, ship,
                   aliens, bullets)


def check_scores_button(stats, scores_button, mouse_x, mouse_y):
    """Show the best scores"""
    button_clicked = scores_button.msg_rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and stats.menu_open:
        stats.menu_open = False


def check_exit_button(stats, exit_button, mouse_x, mouse_y):
    """Close the app when the player clicks Exit."""
    button_clicked = exit_button.msg_rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and stats.menu_open:
        sys.exit()


def start_game(app_settings, screen, stats, scores, sb, ship, aliens, bullets):
    """Reset all statistic to start a new game"""
    if stats.sounds_on:
        pygame.mixer.Sound.play(app_settings.game_start_sound)

    # Update high score
    scores.update_high_score()

    # Mark that menu is not open
    stats.menu_open = False

    # Reset the game settings.
    app_settings.initialize_dynamic_settings()

    # Hide the mouse cursor.
    pygame.mouse.set_visible(False)

    # Reset the game statistic.
    stats.reset_stats()
    stats.game_active = True

    # Reset the scoreboard images.
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    # Empty the list of aliens and bullets
    aliens.empty()
    bullets.empty()

    # Create a new fleet and center the ship.
    create_fleet(app_settings, screen, ship, aliens)
    ship.center_ship()


def create_menu(screen, app_settings, stats, play_button, scores_button,
                exit_button, sound_on_button, sound_off_button):
    """Create buttons and fill background"""
    # Fill background
    screen.fill(app_settings.bg_color)

    # Draw buttons
    buttons = [play_button, scores_button, exit_button]
    first_button_position = screen.get_rect().centery - 2 * play_button.height
    for i, button in enumerate(buttons):
        button.set_y(first_button_position + 2 * i * button.height)
        button.draw_button()
    if stats.sounds_on:
        sound_on_button.draw_button()
    else:
        sound_off_button.draw_button()


def update_screen(app_settings, screen, stats, scores, sb, ship, aliens, bullets,
                  play_button, scores_button, exit_button, sound_on_button,
                  sound_off_button):
    """Update images on the screen and flip to the new screen"""

    if not stats.game_active and stats.menu_open:
        create_menu(screen, app_settings, stats, play_button, scores_button,
                    exit_button, sound_on_button, sound_off_button)
    elif not stats.game_active and stats.game_lost:
        scores.ask_name()
        stats.menu_open = True
        stats.game_lost = False
    elif not stats.game_active and not stats.menu_open:
        scores.draw_background(screen)
        scores.print_score(screen)
    elif stats.game_active:

        # Redraw the screen during each pass through the loop
        screen.fill(app_settings.bg_color)

        # Redraw all bullets behind ship and aliens.
        for bullet in bullets.sprites():
            bullet.draw_bullet()

        ship.blitme()
        aliens.draw(screen)

        # Draw the score information
        sb.show_score()

    # Make the most recently drawn screen visible
    pygame.display.flip()


def update_bullets(app_settings, screen, stats, sb,
                   ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update bullets position
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(app_settings, screen, stats, sb,
                                  ship, aliens, bullets)


def check_bullet_alien_collisions(app_settings, screen, stats, sb, ship,
                                  aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += app_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        app_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(app_settings, screen, ship, aliens)
        if stats.sounds_on:
            pygame.mixer.Sound.play(app_settings.level_up_sound)


def get_number_aliens_x(app_settings, alien_width):
    """Determine the number of aliens that fit in a row"""
    available_space_x = app_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(app_setting, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (app_setting.screen_height - (3 * alien_height) -
                         ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(app_settings, screen, aliens, alien_number, row_number):
    # Create an alien and place it in the row.
    alien = Alien(app_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(app_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    alien = Alien(app_settings, screen)
    number_aliens_x = get_number_aliens_x(app_settings, alien.rect.width)
    number_rows = get_number_rows(app_settings, ship.rect.height,
                                  alien.rect.height)

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(app_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(app_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(app_settings, aliens)
            break


def change_fleet_direction(app_settings, aliens):
    """Drop the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += app_settings.fleet_drop_speed
    app_settings.fleet_direction *= -1


def ship_hit(app_settings, stats, sb, screen, ship, aliens, bullets):
    """Respond to ship being hit by alien"""
    if stats.sounds_on:
        pygame.mixer.Sound.play(app_settings.ship_hit_sound)
    if stats.ships_left > 0:
        # Decrement ship_left
        stats.ships_left -= 1

        # Update scoreboard
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(app_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)

    else:
        stats.game_lost = True
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(app_settings, stats, sb, screen, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this same as if ship got hit.
            ship_hit(app_settings, stats, sb, screen, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_aliens(app_settings, stats, sb, screen, ship, aliens, bullets):
    """
    Check if the fleet is at an edge,
    and then update the positions of all aliens in the fleet.
    """

    check_fleet_edges(app_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(app_settings, stats, sb, screen, ship, aliens, bullets)

    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(app_settings, stats, sb, screen, ship, aliens, bullets)