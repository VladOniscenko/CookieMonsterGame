import time
from os.path import join, abspath
import os

import pygame

from Classes.menu import *
from Classes.rating import Rating
from Classes.mini_game import *

class Game:
    def __init__(self):
        pygame.init()

        # Game init settings
        self.WIDTH, self.HEIGHT = 1280, 720
        self.FPS = 60

        # Display setup
        self.display = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.DISPLAY_W, self.DISPLAY_H = self.display.get_size()
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))

        # Reference values
        self.running, self.playing, self.game_mode, self.start_time = True, False, False, False
        self.LEFT_KEY, self.RIGHT_KEY, self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESC_KEY = False, False, False, False, False, False, False

        self.game_mode = False
        self.difficulty = False

        # Styling
        self.font = self.get_asset_path('Font', '8-BIT WONDER.TTF')
        self.second_font = self.get_asset_path('Font', 'Miguel De Northern.ttf')
        self.BLACK, self.WHITE, self.BLUE, self.GREEN, self.RED, self.ORANGE = (0, 0, 0), (255, 255, 255), (0, 0, 128), (1, 50, 32), (139, 0, 0), (199, 110, 0)

        # Classes
        self.main_menu = MainMenu(self)
        self.difficulties = DifficultyMenu(self)
        self.mini_game_menu = MiniGameMenu(self)
        self.rating = Rating(self)

        self.rps_game = RPSGame(self)

        self.cur_game = self.rps_game
        self.cur_menu = self.main_menu


    def game_loop(self):
        while self.playing:
            self.display.fill(self.WHITE)
            self.check_events()


            # select game
            self.reset_game_mode()
            self.mini_game_menu.display_menu()


            # set game rules, title, attempts etc.
            self.cur_game.configure()
            self.cur_game.play()

            # todo start mini game based on selection
            # todo print game rules
            # todo let user play the game


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


    def reset_keys(self):
        self.LEFT_KEY, self.RIGHT_KEY, self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESC_KEY = False, False, False, False, False, False, False


    def draw_text(self, text, size, x, y, **kwargs):

        if not isinstance(text, str):
            text = str(text)

        color = self.BLACK
        if 'color' in kwargs:
            color = kwargs['color']

        selected_font = self.font
        if 'font' in kwargs:
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


    def get_asset_path(self, asset_type, name):
        # For the deployed version (PyInstaller)
        base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

        # If running in the development environment, use the current working directory
        if not hasattr(sys, '_MEIPASS'):
            assets_path = os.path.join(os.getcwd(), 'assets', asset_type)
        else:
            # If running as a bundled executable, use the _MEIPASS path
            assets_path = os.path.join(base_path, 'assets', asset_type)

        return os.path.join(assets_path, name)

    def get_background(self, name):
        # Use the helper function to get the correct path for the background
        path = self.get_asset_path('Background', name)

        # Load and scale the background image
        selected_image = pygame.image.load(path)
        return pygame.transform.scale(selected_image, (self.DISPLAY_W, self.DISPLAY_H))

    def get_image(self, name):
        # Use the helper function to get the correct path for the image
        path = self.get_asset_path('Other', name)

        # Load the image
        return pygame.image.load(path)


    def reset_game_mode(self):
        self.game_mode = False
