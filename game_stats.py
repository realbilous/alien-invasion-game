class GameStats():
    """Track statistic for ALien Invasion."""

    def __init__(self, app_settings):
        """Initialize statistic."""
        self.app_settings = app_settings
        self.reset_stats()

        # Start game in an inactive state.
        self.game_active = False

        # High score should never be reset.
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.app_settings.ship_limit
        self.score = 0
        self.level = 1