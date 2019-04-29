import datetime
import tkinter as tk

import pygame


class Score():
    """A class to manage score tab and processes relating to it"""

    def __init__(self, app_settings, stats):
        # Initializing attributes
        self.app_settings = app_settings
        self.stats = stats

        # Regular text settings
        self.regular_font = pygame.font.SysFont("cambria", 20)

        # Title settings
        self.title_txt = "LEADERBOARD"
        self.title_font = pygame.font.SysFont("cambria", 40)
        self.title_img = self.title_font.render(self.title_txt, True, (0, 0, 0))
        self.title_width, self.title_height = self.title_font.size(self.title_txt)

    # Methods for reading saved data

    def update_high_score(self):
        if self.get_score_sorted():
            self.stats.high_score = int(self.get_score_sorted()[0][1])

    def print_score(self, screen):
        """Print all score records on the screen"""
        for i, values in enumerate(self.get_score_sorted()):
            # Converting all values to images
            position = self.regular_font.render(str(i + 1) + ".", True, (0, 0, 0))
            player_name = self.regular_font.render(values[0], True, (0, 0, 0))
            score = self.regular_font.render(str(values[1]), True, (0, 0, 0))
            date = self.regular_font.render(values[2], True, (0, 0, 0))

            # Get needed sizes to make right positioning of text
            position_size_x = self.regular_font.size(str(i + 1) + ".")[0]
            score_size_x, text_height = self.regular_font.size(str(values[1]))
            date_size_x = self.regular_font.size(values[2])[0]
            screen_rect = screen.get_rect()

            # Print a record
            screen.blit(position, (screen_rect.left + 30, 30 + i*text_height +
                                   self.title_height))
            screen.blit(player_name, (screen_rect.left + 40 + position_size_x,
                                      30 + i*text_height + self.title_height))
            screen.blit(score, (screen_rect.centerx - score_size_x / 2,
                                30 + i * text_height + self.title_height))
            screen.blit(date, (screen_rect.right - date_size_x - 30,
                               30 + i*text_height + self.title_height))

    def draw_background(self, screen):
        """Draw background of score records without records"""
        screen.fill(self.app_settings.bg_color)
        screen.blit(self.title_img, (screen.get_rect().centerx -
                                     self.title_width / 2, 20))

    def get_score_sorted(self):
        """Sort list of score records by magnitude of a score"""
        data = []
        for line in self.read_scores():
            data.append(tuple(line.strip().split(",")))
        data.sort(key=lambda x: int(x[1]), reverse=True)
        return data[:self.app_settings.score_records_limit]

    def read_scores(self):
        """Open file and get list of score records"""
        lines = []
        try:
            with open(self.app_settings.score_storage) as file_obj:
                for line in file_obj:
                    lines.append(line)
        except FileNotFoundError:
            pass
        return lines

    # Methods for recording new data

    def ask_name(self):
        """Create pop-up window to ask player name"""

        # Create window
        root = tk.Tk()
        root.title("Save your score")
        root.resizable(False, False)  # Disable resize
        window_height = 100  # Window size
        window_width = 165  #
        screen_width = root.winfo_screenwidth()  # Size of the screen
        screen_height = root.winfo_screenheight()  #

        # Positioning window; creating and setting label, entry box and button
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        root.geometry = root.geometry("{}x{}+{}+{}".format(
            window_width, window_height, x, y))
        label = tk.Label(root, text="Enter your name :",
                              font=("cambria", 14, "bold"),
                              fg="black").place(x=5, y=5)
        name = tk.StringVar()
        tk.entry_box = tk.Entry(root, textvariable=name,
                                width=25).place(x=5, y=40)
        button = tk.Button(root, text="Enter", width=10, height=1,
                           command=lambda: self.save_score(name.get(),
                           root)).place(x=42, y=68)
        root.mainloop()

    def get_date(self):
        """Get current date"""
        now = datetime.datetime.now()
        return "{}/{}/{}".format(now.day, now.month, now.year)

    def save_score(self, name, root):
        """Record stores to a file"""
        root.destroy()
        if not name:
            return
        record = "{},{},{}".format(name, self.stats.score,
                                   self.get_date())
        with open(self.app_settings.score_storage, 'a') as file_obj:
            file_obj.write(record + "\n")





