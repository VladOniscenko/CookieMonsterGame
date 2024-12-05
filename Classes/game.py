from functions import get_asset_path
import pygame
import time
import sys
import random
import math

from Classes.menu import MainMenu, DifficultyMenu, MiniGameMenu
from Classes.mini_game import RPSGame, HangmanGame
from Classes.rating import Rating


class Game:
    def __init__(self):
        self.guessing_password = False
        self.display_rules, self.cur_game, self.display_story, self.display_winscreen, self.display_losescreen = None, None, None, None, None
        pygame.init()
        pygame.mixer.init()

        self.total_score = 0
        self.guessed_characters = []
        self.password = 'challenge'
        self.pass_list = list(self.password)
        self.amount_games_unplayed = 2
        self.played_games = []
        self.inputted_chars = []
        self.alphabet = list('abcdefghijklmnopqrstuvwxyz')

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
        self.sound = self.play_music('main.wav', 99, 90, 20)

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

    def game_loop(self) -> None:
        self.playing = True
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

                # todo fix 2 if more games available
                if len(self.played_games) >= 2:
                    self.playing = False

                self.win_logic(self.game_controller.is_winner)


            self.window.blit(self.display,  (0, 0))
            pygame.display.update()

            self.reset_keys()

        # display password guessing screen
        self.guess_password()

    def check_events(self) -> None:
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

    def reset_keys(self) -> None:
        self.OTHER_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESC_KEY = [], False, False, False, False, False, False, False

    def draw_text(self, text: str, size: int | float, x: int | float, y: int | float, **kwargs) -> None:

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

    def start_game(self) -> None:
        self.start_time = int(time.time())

    def get_background(self, name: str) -> pygame.image:
        # Use the helper function to get the correct path for the background
        path = get_asset_path('Background', name)

        # Load and scale the background image
        selected_image = pygame.image.load(path)
        return pygame.transform.scale(selected_image, (self.DISPLAY_W, self.DISPLAY_H))

    def play_music(self, file_path: str, loops: int = 1, start: float = 0.0, fade: int = 500, volume: float = 0.03, play: bool = True) -> pygame.mixer:
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

    def get_game_controller(self) -> RPSGame | HangmanGame | None:
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

    def show_rules(self) -> None:
        # stop playing any music
        if self.sound.music:
            self.sound.music.pause()

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

    def pre_story(self) -> None:
        self.sound = self.play_music('horror.mp3', 99, 90, 20, volume=.1)
        # Story text
        story = [
            "WARNING: A malicious entity has infiltrated your computer!",
            "The Cookie Monster, driven by his hunger for cookies, has spread a virus across your system.",
            "Your files are at risk, and he demands the ultimate password to unleash his sugary chaos!",
            "You must fight back by playing games to get letters and decrypt the password.",
            "Only then can you save your computer from his cookie-fueled mayhem..."
        ]

        self.display_story = True
        story_line_index = 0
        current_line = ""
        char_index = 0
        line_speed = 40
        last_time = pygame.time.get_ticks()

        while self.display_story:
            self.check_events()
            if self.START_KEY:
                self.display_story = False

            self.display.fill(self.BLACK)

            y_start = 250
            y_offset = 50

            if story_line_index < len(story):
                now = pygame.time.get_ticks()
                if now - last_time > line_speed:
                    if char_index < len(story[story_line_index]):
                        current_line += story[story_line_index][char_index]
                        char_index += 1
                    else:
                        story_line_index += 1
                        current_line = ""
                        char_index = 0
                    last_time = now

            # Draw all fully written lines and the current line being typed
            for i in range(story_line_index):
                self.draw_text(story[i], 30, self.mid_w, y_start + (y_offset * i), color=self.WHITE, position='center',
                               font=self.second_font)

            if current_line:
                self.draw_text(
                    current_line,
                    30,
                    self.mid_w,
                    y_start + (y_offset * story_line_index),
                    color=self.WHITE,
                    position='center',
                    font=self.second_font
                )

            self.draw_text(
                'PRESS ENTER TO SKIP >>',
                50,
                self.mid_w,
                y_start + (y_offset * (len(story) + 2)),
                font=self.second_font,
                position='center',
                color=self.RED
            )

            self.blit_screen()

    def blit_screen(self) -> None:
        self.window.blit(self.display, (0, 0))
        pygame.display.update()
        self.reset_keys()

    def guess_password(self):
        self.guessing_password = True
        while self.guessing_password:
            self.check_events()

            for char in self.OTHER_KEY:
                if char in self.alphabet and len(self.inputted_chars) < len(self.password):
                    self.inputted_chars.append(char)

            if self.BACK_KEY and len(self.inputted_chars) > 0:
                self.inputted_chars.pop()

            if self.START_KEY and len(self.inputted_chars) == len(self.password):
                self.guessing_password = False


            self.display.fill(self.BLACK)
            self.draw_text('GUESS THE PASSWORD', 20, self.DISPLAY_W / 2, 100, color=self.WHITE, position='center')

            self.draw_password_lines(self.inputted_chars)

            self.blit_screen()

    def draw_password_lines(self, inputted_chars: list[str]) -> None:
        word = self.password
        display = self.display

        line_length = 60
        space_between_lines = 15
        start_x = (self.DISPLAY_W // 2 -
                   (len(word) * (line_length +
                                 space_between_lines)) // 2)

        start_y = 400
        f_size = 20

        # Draw lines for each letter in the word
        for i, char in enumerate(word):
            # Draw the line for the current character
            # (even if it's not guessed yet)
            pygame.draw.line(
                display,
                self.WHITE,
                (start_x + i * (line_length +
                                space_between_lines), start_y),
                (start_x + i * (line_length +
                                space_between_lines) + line_length, start_y),
                3
            )

            # Calculate the width of the character to center it on the line
            font = pygame.font.Font(self.font, f_size)

            # Get both width and height
            char_width, char_height = font.size(char)

            # Calculate the x-coordinate to center the text
            char_x = (start_x + i * (line_length + space_between_lines)
                      + (line_length - char_width) // 2)

            self.draw_text(
                inputted_chars[i] if i < len(inputted_chars) else '',
                f_size,
                char_x,
                start_y - 50,
                color=self.WHITE,
                position='topleft'
            )

        self.draw_text(
            'PRESS ENTER TO SUBMIT >>',
            f_size,
            self.DISPLAY_W / 2,
            600,
            color=self.RED,
            position='center',
            font=self.second_font
        )


    def win_logic(self, has_user_won: bool):
        if has_user_won:
            amount_letters = len(self.pass_list) //self.amount_games_unplayed
            self.amount_games_unplayed -= 1
            new_letters = ""

            for _ in range(amount_letters):
                index = random.randint(0, len(self.pass_list) - 1)
                new_letter = self.pass_list.pop(index)
                new_letters += new_letter
                self.guessed_characters.append(new_letter)
            self.display_winscreen = True

            while self.display_winscreen:
                self.check_events()
                if self.START_KEY:
                    self.display_winscreen = False
                self.display.fill(self.WHITE)

                y_start = 250
                y_offset = 50

                self.draw_text(
                    'YOU WIN! HERE ARE YOUR LETTERS: ' + new_letters,
                    50,
                    self.mid_w,
                    y_start + y_offset,
                    font=self.second_font,
                    position='center',
                    color=self.BLACK
                )
                self.blit_screen()

        else:
            self.display_losescreen = True
            while self.display_losescreen:
                self.check_events()
                if self.START_KEY:
                    self.display_losescreen = False
                self.display.fill(self.RED)

                y_start = 250
                y_offset = 50

                self.draw_text(
                    'YOU LOSE',
                    50,
                    self.mid_w,
                    y_start + y_offset,
                    font=self.second_font,
                    position='center',
                    color=self.BLACK
                )
                self.blit_screen()



