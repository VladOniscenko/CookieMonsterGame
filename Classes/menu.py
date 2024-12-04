import sys
import pygame


class Menu:
    def __init__(self, game) -> None:
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.option_offset = 40

        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)

        self.offset = -50

    def draw_cursor(self, **kwargs) -> None:
        color = self.game.BLACK
        if 'color' in kwargs:
            color = kwargs['color']

        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y, color=color)

    def blit_screen(self) -> None:
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game) -> None:
        Menu.__init__(self, game)
        self.state = "Start"
        self.start_pos = 100

        self.playx, self.playy = self.start_pos, self.mid_h - 50
        self.scoreboardx, self.scoreboardy = self.start_pos, self.playy + self.option_offset
        self.quitx, self.quity = self.start_pos, self.scoreboardy + self.option_offset

        self.cursor_rect.midtop = (self.start_pos + self.offset, self.playy)

    def display_menu(self) -> None:
        while self.run_display:
            self.game.check_events()
            self.check_input()

            self.game.display.fill(self.game.WHITE)
            self.game.display.blit(self.game.get_background('main.png'), (0, 0))

            self.game.draw_text('Start', 20, self.playx, self.playy, color=self.game.BLACK)
            self.game.draw_text('Scoreboard', 20, self.scoreboardx, self.scoreboardy, color=self.game.BLACK)
            self.game.draw_text('Quit', 20, self.quitx, self.quity, color=self.game.BLACK)

            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self) -> None:
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

    def check_input(self) -> None:
        self.move_cursor()

        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.difficulties.run_display = True
            elif self.state == 'Scoreboard':
                self.game.rating.run_display = True
            elif self.state == 'Quit':
                pygame.quit()
                sys.exit()
            self.run_display = False


class DifficultyMenu(Menu):
    def __init__(self, game) -> None:
        Menu.__init__(self, game)
        self.state = 'easy'
        self.run_display = False

        self.easyx, self.easyy = self.mid_w - 50, self.mid_h - 30
        self.mediumx, self.mediumy = self.mid_w - 50, self.easyy + self.option_offset
        self.hardx, self.hardy = self.mid_w - 50, self.mediumy + self.option_offset
        self.cursor_rect.midtop = (self.easyx + self.offset, self.easyy)

    def display_menu(self) -> None:
        while self.run_display:
            self.game.check_events()
            self.check_input()

            self.game.display.fill(self.game.WHITE)

            self.game.draw_text('DIFFICULTY', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100, position='center')
            self.game.draw_text('easy', 20, self.easyx, self.easyy, color=self.game.GREEN)
            self.game.draw_text('medium', 20, self.mediumx, self.mediumy, color=self.game.ORANGE)
            self.game.draw_text('hard', 20, self.hardx, self.hardy, color=self.game.RED)

            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self) -> None:
        if self.game.UP_KEY:
            if self.state == "easy":
                self.state = 'hard'
                self.cursor_rect.midtop = (self.hardx + self.offset, self.hardy)
            elif self.state == "hard":
                self.state = "medium"
                self.cursor_rect.midtop = (self.mediumx + self.offset, self.mediumy)
            else:
                self.state = "easy"
                self.cursor_rect.midtop = (self.easyx + self.offset, self.easyy)
        elif self.game.DOWN_KEY:
            if self.state == "easy":
                self.state = "medium"
                self.cursor_rect.midtop = (self.mediumx + self.offset, self.mediumy)
            elif self.state == "medium":
                self.state = 'hard'
                self.cursor_rect.midtop = (self.hardx + self.offset, self.hardy)
            else:
                self.state = "easy"
                self.cursor_rect.midtop = (self.easyx + self.offset, self.easyy)

    def check_input(self) -> None:
        self.move_cursor()

        if self.game.START_KEY or self.game.BACK_KEY or self.game.ESC_KEY:
            self.run_display = False

        if self.game.START_KEY:
            self.game.difficulty = self.state
            self.game.start_game()
        elif self.game.BACK_KEY or self.game.ESC_KEY:
            self.game.main_menu.run_display = True


class MiniGameMenu(Menu):
    def __init__(self, game) -> None:
        Menu.__init__(self, game)
        self.encrypter_color = None
        self.math_champ_color = None
        self.binarize_color = None
        self.hangman_color = None
        self.rps_color = None
        self.state = 'rps'

        self.rpsx, self.rpsy = self.mid_w - 100, self.mid_h - 150
        self.hangmanx, self.hangmany = self.rpsx, self.rpsy + self.option_offset
        self.binarizex, self.binarizey = self.rpsx, self.hangmany + self.option_offset
        self.encrypterx, self.encryptery = self.rpsx, self.binarizey + self.option_offset
        self.math_champx, self.math_champy = self.rpsx, self.encryptery + self.option_offset

        self.cursor_rect.midtop = (self.rpsx + self.offset, self.rpsy)

    def display_menu(self) -> None:
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()

            self.game.display.fill(self.game.WHITE)
            self.rps_color = False if 'rps' not in self.game.played_games else self.game.RED
            self.hangman_color = False if 'hangman' not in self.game.played_games else self.game.RED
            self.binarize_color = False if 'binarize' not in self.game.played_games else self.game.RED
            self.encrypter_color = False if 'encrypter' not in self.game.played_games else self.game.RED

            self.game.draw_text('SELECT MINI GAME', 30, self.mid_w, self.mid_h - 250, position='center')
            self.game.draw_text('Rock Paper Scissors', 20, self.rpsx, self.rpsy, color=self.rps_color)
            self.game.draw_text('Hangman', 20, self.hangmanx, self.hangmany, color=self.hangman_color)
            self.game.draw_text('Binarize in dev', 20, self.binarizex, self.binarizey, color=self.binarize_color, font=self.game.second_font)
            self.game.draw_text('Encrypter in dev', 20, self.encrypterx, self.encryptery, color=self.encrypter_color, font=self.game.second_font)
            self.game.draw_text('Math Champ in dev', 20, self.math_champx, self.math_champy, color=self.math_champ_color, font=self.game.second_font)

            self.draw_cursor(color=self.game.BLACK)
            self.blit_screen()

    def move_cursor(self) -> None:
        if self.game.UP_KEY:
            if self.state == 'rps':
                self.state = 'math_champ'
                self.cursor_rect.midtop = (self.math_champx + self.offset, self.math_champy)
            elif self.state == 'binarize':
                self.state = 'hangman'
                self.cursor_rect.midtop = (self.hangmanx + self.offset, self.hangmany)
            elif self.state == 'hangman':
                self.state = "rps"
                self.cursor_rect.midtop = (self.rpsx + self.offset, self.rpsy)
            elif self.state == 'encrypter':
                self.state = "binarize"
                self.cursor_rect.midtop = (self.binarizex + self.offset, self.binarizey)
            elif self.state == 'math_champ':
                self.state = "encrypter"
                self.cursor_rect.midtop = (self.encrypterx + self.offset, self.encryptery)
            else:
                self.state = "rps"
                self.cursor_rect.midtop = (self.rpsx + self.offset, self.rpsy)
        elif self.game.DOWN_KEY:
            if self.state == "rps":
                self.state = "hangman"
                self.cursor_rect.midtop = (self.hangmanx + self.offset, self.hangmany)
            elif self.state == 'hangman':
                self.state = 'binarize'
                self.cursor_rect.midtop = (self.binarizex + self.offset, self.binarizey)
            elif self.state == 'binarize':
                self.state = 'encrypter'
                self.cursor_rect.midtop = (self.encrypterx + self.offset, self.encryptery)
            elif self.state == 'encrypter':
                self.state = 'math_champ'
                self.cursor_rect.midtop = (self.math_champx + self.offset, self.math_champy)
            else:
                self.state = "rps"
                self.cursor_rect.midtop = (self.rpsx + self.offset, self.rpsy)

    def check_input(self) -> None:
        self.move_cursor()

        if self.game.START_KEY and self.state not in self.game.played_games:
            self.run_display = False
            self.game.game_mode = self.state
