import sys
import pygame

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2

        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)

        self.offset = -50

    def draw_cursor(self, **kwargs):
        color = self.game.BLACK
        if 'color' in kwargs:
            color = kwargs['color']

        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y, color)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.start_pos = 100

        self.playx, self.playy = self.start_pos, self.mid_h - 50
        self.scoreboardx, self.scoreboardy = self.start_pos, self.mid_h
        self.quitx, self.quity = self.start_pos, self.mid_h + 50

        self.cursor_rect.midtop = (self.start_pos + self.offset, self.playy)


    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()

            self.game.display.fill(self.game.BLACK)
            self.game.display.blit(self.game.BG, (0, 0))

            self.game.draw_text('Start', 20, self.playx, self.playy, self.game.BLACK)
            self.game.draw_text('Scoreboard', 20, self.scoreboardx, self.scoreboardy, self.game.BLACK)
            self.game.draw_text('Quit', 20, self.quitx, self.quity, self.game.BLACK)

            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.scoreboardx + self.offset, self.scoreboardy)
                self.state = "Scoreboard"

            elif self.state == "Scoreboard":
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = "Quit"

            else:
                self.cursor_rect.midtop = (self.playx + self.offset, self.playy)
                self.state = "Start"
        elif self.game.UP_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = "Quit"

            elif self.state == "Quit":
                self.cursor_rect.midtop = (self.scoreboardx + self.offset, self.scoreboardy)
                self.state = "Scoreboard"

            else:
                self.cursor_rect.midtop = (self.playx + self.offset, self.playy)
                self.state = "Start"

    def check_input(self):
        self.move_cursor()

        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.cur_menu = self.game.difficulties
            elif self.state == 'Scoreboard':
                self.game.rating.run_display = True
            elif self.state == 'Quit':
                pygame.quit()
                sys.exit()
            self.run_display = False


class DifficultyMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Easy'

        self.easyx, self.easyy = self.mid_w - 50, self.mid_h - 30
        self.mediumx, self.mediumy = self.mid_w - 50, self.mid_h
        self.hardx, self.hardy = self.mid_w - 50, self.mid_h + 30
        self.cursor_rect.midtop = (self.easyx + self.offset, self.easyy)


    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()

            self.game.display.fill(self.game.BLACK)

            self.game.draw_text('DIFFICULTY', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100, position='center')
            self.game.draw_text('Easy', 20, self.easyx, self.easyy, color=(1, 50, 32))
            self.game.draw_text('Medium', 20, self.mediumx, self.mediumy, color=(199, 110, 0))
            self.game.draw_text('Hard', 20, self.hardx, self.hardy, color=(139, 0, 0))

            self.draw_cursor(color=self.game.WHITE)
            self.blit_screen()

    def move_cursor(self):
        if self.game.UP_KEY:
            if self.state == "Easy":
                self.state = 'Hard'
                self.cursor_rect.midtop = (self.hardx + self.offset, self.hardy)
            elif self.state == "Hard":
                self.state = "Medium"
                self.cursor_rect.midtop = (self.mediumx + self.offset, self.mediumy)
            else:
                self.state = "Easy"
                self.cursor_rect.midtop = (self.easyx + self.offset, self.easyy)
        elif self.game.DOWN_KEY:
            if self.state == "Easy":
                self.state = "Medium"
                self.cursor_rect.midtop = (self.mediumx + self.offset, self.mediumy)
            elif self.state == "Medium":
                self.state = 'Hard'
                self.cursor_rect.midtop = (self.hardx + self.offset, self.hardy)
            else:
                self.state = "Easy"
                self.cursor_rect.midtop = (self.easyx + self.offset, self.easyy)

    def check_input(self):
        self.move_cursor()

        if self.game.START_KEY:
            self.game.game_mode = self.state
            self.game.playing = True
        elif self.game.BACK_KEY or self.game.ESC_KEY:
            self.game.cur_menu = self.game.main_menu
        self.run_display = False