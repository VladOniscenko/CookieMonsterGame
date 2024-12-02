from functions import get_asset_path
import pygame
import time
import sys

from Classes.menu import MainMenu, DifficultyMenu, MiniGameMenu
from Classes.mini_game import RPSGame, HangmanGame
from Classes.rating import Rating


class Game:
    def __init__(self):
        self.display_rules = None
        self.cur_game = None
        pygame.init()
        pygame.mixer.init()

        self.total_score = 0
        self.guessed_characters = []
        self.password = 'challenge'
        self.pass_list = list(self.password)
        self.played_games = []

        # Game init settings
        self.WIDTH, self.HEIGHT = 1280, 720
        self.FPS = 60

        # Display setup
        self.display = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.DISPLAY_W, self.DISPLAY_H = self.display.get_size()
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.mid_w, self.mid_h = self.DISPLAY_W / 2, self.DISPLAY_H / 2

        # Reference values
        self.running, self.playing, self.game_mode, self.start_time = True, False, False, False
        self.OTHER_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESC_KEY = [], False, False, False, False, False, False, False

        self.game_mode = False
        self.difficulty = False

        # todo enable music
        # self.main_sound = self.play_music('main.wav', 99, 90, 20)
        self.main_sound = None

        # Styling
        self.font = get_asset_path('Font', '8-BIT WONDER.TTF')
        self.second_font = get_asset_path('Font', 'Miguel De Northern.ttf')
        self.BLACK, self.WHITE, self.BLUE, self.GREEN, self.RED, self.ORANGE = (0, 0, 0), (255, 255, 255), (0, 0, 128), (1, 50, 32), (139, 0, 0), (199, 110, 0)

        # Classes
        self.main_menu = MainMenu(self)
        self.difficulties = DifficultyMenu(self)
        self.mini_game_menu = MiniGameMenu(self)
        self.rating = Rating(self)

        self.rps_game = RPSGame(self)
        self.hangman_game = HangmanGame(self)
        self.binarize_game = None
        self.encrypter_game = None
        self.math_champ_game = None

        self.game_controller = None

    def game_loop(self):
        # stop playing any music
        try:
            if self.main_sound.music:
                self.main_sound.music.pause()
        except Exception as e:
            print(e)
            pass

        while self.playing:
            self.display.fill(self.WHITE)
            self.check_events()
            self.cur_game = False

            # select game
            self.mini_game_menu.display_menu()

            self.game_controller = self.get_game_controller()

            if self.game_controller:
                # set game rules, title, attempts etc.
                self.game_controller.configure()

                # show rules
                self.game_controller.display_rules()

                # play the game
                self.game_controller.play()

                # process after game
                if self.game_mode not in self.played_games:
                    self.played_games.append(self.game_mode)

                # if self.cur_game.is_winner:
                #     self.t

                # todo check if user won
                # todo update total score
                # todo show winning password characters
                # todo exclude played game from list

            self.window.blit(self.display,  (0, 0))
            pygame.display.update()

            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.ESC_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True

                if pygame.K_a <= event.key <= pygame.K_z:
                    self.OTHER_KEY.append(chr(event.key).lower())

    def reset_keys(self):
        self.OTHER_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESC_KEY = [], False, False, False, False, False, False, False

    def draw_text(self, text, size, x, y, **kwargs):

        if not isinstance(text, str):
            text = str(text)

        color = self.BLACK
        if 'color' in kwargs and kwargs['color']:
            color = kwargs['color']

        selected_font = self.font
        if 'font' in kwargs and kwargs['font']:
            selected_font = kwargs['font']
        font = pygame.font.Font(selected_font, size)

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        position = 'topleft'
        if 'position' in kwargs:
            position = kwargs['position']

        setattr(text_rect, position, (x, y))

        self.display.blit(text_surface, text_rect)

    def start_game(self):
        self.playing = True
        self.start_time = int(time.time())

    def get_background(self, name):
        # Use the helper function to get the correct path for the background
        path = get_asset_path('Background', name)

        # Load and scale the background image
        selected_image = pygame.image.load(path)
        return pygame.transform.scale(selected_image, (self.DISPLAY_W, self.DISPLAY_H))

    def play_music(self, file_path, loops=1, start=0.0, fade=500, volume=0.03, play=True):
        # Initialize a new mixer instance
        pygame.mixer.quit()  # Ensure no conflicts with existing mixer
        pygame.mixer.init()

        try:
            path = get_asset_path('Sound', file_path)
            if not path:
                raise FileNotFoundError(f"Asset path not found for {file_path}")

            pygame.mixer.music.load(path)  # Load the music file
            pygame.mixer.music.set_volume(volume)  # Set default volume
            pygame.mixer.music.play(loops, start, fade)  # Play the music

            if not play:
                pygame.mixer.music.pause()

        except Exception as e:
            print(f"Error: {e}")

        return pygame.mixer

    def get_game_controller(self):
        if self.game_mode == 'rps':
            return self.rps_game
        elif self.game_mode == 'hangman':
            return self.hangman_game
        elif self.game_mode == 'math_champ':
            return self.math_champ_game
        elif self.game_mode == 'encrypter':
            return self.encrypter_game
        elif self.game_mode == 'binarize':
            return self.binarize_game
        else:
            return None

    def show_rules(self):
        # Rules text
        rules = [
            "You will play a series of mini-games.",
            "For each mini-game, you will earn letters.",
            "If you win the most mini-games, you can decrypt the password in a later stage.",
            "There are a total of 5 mini-games."
        ]

        self.display_rules = True
        while self.display_rules:
            self.check_events()
            if self.START_KEY:
                self.display_rules = False
                
            # Clear screen
            self.display.fill(self.BLACK)

            # Display each line of text
            y_offset = 40
            y_start = 250

            self.draw_text("Game Rules:", 40, self.mid_w, y_start - y_offset, color=self.WHITE, position='center', font=self.second_font)
            for i, line in enumerate(rules):
                self.draw_text(line, 30, self.mid_w, y_start + (y_offset * i), color=self.WHITE, position='center', font=self.second_font)

            self.draw_text(
                'PRESS ENTER TO START >>',
                50,
                self.mid_w,
                y_start + (y_offset * len(rules)) + 50,
                font=self.second_font,
                position='center',
                color=self.RED
            )

            self.blit_screen()

    def pre_story(self):
        pass

    def blit_screen(self) -> None:
        self.window.blit(self.display, (0, 0))
        pygame.display.update()
        self.reset_keys()