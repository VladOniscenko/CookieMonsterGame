import pygame
import csv

class Rating:
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.run_display = False


    def display_rating(self):
        while self.run_display:
            self.game.check_events()
            self.check_input()

            self.game.display.fill(self.game.WHITE)
            self.game.draw_text('High Scores', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 300, position='center')

            headers = ["Name", "Score", "Time", "Mode"]
            header_text = "   ".join(headers)
            self.game.draw_text(header_text, 25, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 150, position='center')

            line_height = 25
            index = 0
            start_pos = -100

            for row in self.get_scores():
                y = start_pos + ((index + 1) * line_height)
                score_text = "   ".join(row)
                self.game.draw_text(score_text, 15, self.game.DISPLAY_W / 2, (self.game.DISPLAY_H / 2) + y, position='center')
                index += 1

            self.blit_screen()

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

    def get_scores(self):
        with open(self.game.get_asset_path('Other', 'scoreboard.csv'), mode='r') as file:
            data = list(csv.reader(file))
        return sorted(data, key=lambda line: int(line[1]))[:11]


    def check_input(self):
        if self.game.BACK_KEY or self.game.ESC_KEY:
            self.game.cur_menu = self.game.main_menu
            self.run_display = False
