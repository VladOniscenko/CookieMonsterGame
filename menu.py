import pygame

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2

        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)

        self.offset = -100

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y, self.game.BLACK)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.start_pos = 200
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
                self.game.playing = True
            elif self.state == 'Scpreboard':
                pass
            elif self.state == 'Quit':
                pass
            self.run_display = False

