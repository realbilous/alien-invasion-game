import pygame.font


class Button():

    def __init__(self, app_settings, screen, msg=None, img_path=None):
        """Initialize button attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        if msg:
            self.image = None
            self.msg = msg


            # Set the dimensions, font and properties of the button.
            self.width, self.height = 200, 50
            self.button_color = (0, 140, 0)
            self.font = pygame.font.SysFont("cambria", 36, bold=True)

            # Hover - mouse hovers over a button, inactive - mouse doesn't hover over
            self.text_color_hover = (100, 0, 180)
            self.text_color_inactive = (255, 255, 255)
            self.text_color = self.text_color_inactive

            # Build the button's rect object and center it
            self.msg_rect = pygame.Rect(0, 0, self.width, self.height)
            self.msg_rect.center = self.screen_rect.center
        elif img_path:
            # Set position for sounds volume button(default)
            self.msg = None
            self.image = pygame.image.load(img_path)
            self.screen_rect = screen.get_rect()
            self.image_rect = self.image.get_rect()
            self.image_rect.right = (self.screen_rect.right -
                                     self.image_rect.width)
            self.image_rect.top = (self.screen_rect.top +
                                     self.image_rect.width)

        # The button message needs to be prepared only once.
        if msg:
            self.prep_msg(msg)

        # Flag for playing sound just one time after mouse was directed on a button
        # 1 - cursor was just directed, trigger the sound
        # 2 - cursor was directed before, do not trigger the sound
        # 3 - cursor wasn't directed at all, do not trigger the sound
        self.cursor_directed = 3

    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.msg_rect.center

    def set_y(self, y):
        self.msg_rect.centery = y
        if self.msg:
            self.prep_msg(self.msg)

    def set_x(self, x):
        self.msg_rect.centerx = x
        if self.msg:
            self.prep_msg(self.msg)

    def draw_button(self):
        # Draw blank button and then draw a message.
        if self.msg:
            self.screen.fill(self.button_color, self.msg_rect)
            self.screen.blit(self.msg_image, self.msg_image_rect)
        # Draw an image
        elif self.image:
            self.screen.blit(self.image, self.image_rect)