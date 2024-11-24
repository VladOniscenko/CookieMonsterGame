import time
from os.path import join, abspath
import os

import pygame
from pygame.examples.music_drop_fade import volume

pygame.mixer.init()

from Classes.menu import *
from Classes.rating import Rating
from Classes.mini_game import *
from functions import *


class Game:
    def __init__(self):
        pygame.init()

        self.total_score = 0
        self.guessed_characters = []
        self.password = 'challenge'
        self.pass_list = list(self.password)
        self.total_games = 1
        self.played_games = []

        # Game init settings
        self.WIDTH, self.HEIGHT = 1280, 720
        self.FPS = 60

        # Display setup
        self.display = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.DISPLAY_W, self.DISPLAY_H = self.display.get_size()
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))

        # Reference values
        self.running, self.playing, self.game_mode, self.start_time = True, False, False, False
        self.OTHER_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESC_KEY = [], False, False, False, False, False, False, False

        self.game_mode = False
        self.difficulty = False
        self.main_sound = self.play_music('main.wav', 99, 90, 20)

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
        self.cur_game = False

    def game_loop(self):
        # stop playing any music
        self.main_sound.music.pause()

        while self.playing:
            self.display.fill(self.WHITE)
            self.check_events()
            self.cur_game = False

            # select game
            self.mini_game_menu.display_menu()

            if self.cur_game:
                # set game rules, title, attempts etc.
                self.cur_game.configure()

                # show rules
                self.cur_game.display_rules()

                # play the game
                self.cur_game.play()

                # process after game
                if self.game_mode not in self.played_games:
                    self.played_games.append(self.game_mode)

                # if self.cur_game.is_winner:
                #     self.t

                # todo check if user won
                # todo update total score
                # todo show winning password characters
                # todo exclude played game from list

            self.window.blit(self.display, (0,0))
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

    import pygame

    def play_music(self, file_path, loops=1, start=0.0, fade=500, volume = 0.1):
        # Initialize a new mixer instance
        pygame.mixer.quit()  # Ensure no conflicts with existing mixer
        pygame.mixer.init()

        try:
            path = get_asset_path('Sound', file_path)
            pygame.mixer.music.load(path)  # Load the music file
            pygame.mixer.music.set_volume(volume)  # Set default volume
            pygame.mixer.music.play(loops, start, fade)  # Play the music
        except Exception as e:
            print(f"Error: {e}")

        return pygame.mixer

