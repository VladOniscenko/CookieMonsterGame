import random

import pygame


class MainGame:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W // 2, self.game.DISPLAY_H // 2

        self.run_display = True
        self.display_rules = True
        self.running = False

        self.total_attempts = 0
        self.attempt = 0
        self.correct = 0
        self.incorrect = 0
        self.title = ''
        self.rules = ''

        self.game_rules = {
            'rps': {
                'title': 'Rock Paper Scissor',
                'rules': "In Rock, Paper, Scissors, two players each choose one of three options: Rock, Paper, or Scissors. Rock beats Scissors, Scissors beats Paper, and Paper beats Rock. If both players choose the same option, the round is a tie. The game is usually played in multiple rounds, and the player with the most wins is the overall winner.",
                'total_attempts': {
                    'easy': 3,
                    'medium': 2,
                    'hard': 1
                }
            }
        }


    def configure(self):
        self.reset_game()
        self.total_attempts = self.get_rule_value('total_attempts')
        self.title = self.get_rule_value('title')
        self.rules = self.get_rule_value('rules')


    def reset_game(self):
        self.total_attempts = 0
        self.attempt = 0
        self.correct = 0
        self.incorrect = 0
        self.title = ''
        self.rules = ''


    def get_rule_value(self, column_name):
        rule = self.game_rules.get(self.game.game_mode, {}).get(column_name)
        if isinstance(rule, dict):
            return rule.get(self.game.difficulty, 1)
        return rule


    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


    def show_rules(self):
        self.display_rules = True
        font_size = 30
        line_height = font_size + 5
        lines = self.split_text(self.rules, font_size, self.mid_w)

        while self.display_rules:
            self.game.check_events()

            if self.game.START_KEY:
                self.display_rules = False

            self.game.display.fill(self.game.WHITE)

            for idx, line in enumerate(lines):
                self.game.draw_text(line, font_size, self.mid_w, self.mid_h - len(lines) * line_height // 2 + idx * line_height, font=self.game.second_font, position='center')

            self.game.draw_text(self.title, 50, self.mid_w, self.mid_h - 200, font=self.game.second_font, position='center')
            self.game.draw_text('PRESS ENTER TO PLAY >>', font_size, self.mid_w, self.mid_h + 200, font=self.game.second_font, position='center', color=self.game.RED)

            self.blit_screen()


    def split_text(self, text, font_size, max_width):
        """Breaks the text into multiple lines that fit within the given width."""
        font = pygame.font.Font(self.game.second_font, font_size)
        words = text.split(' ')
        lines = []
        current_line = ''

        for word in words:
            # Create a test line to check the width
            test_line = f"{current_line} {word}".strip()
            test_surface = font.render(test_line, True, self.game.RED)

            # If the line exceeds the max width, push the current line to lines and start a new one
            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        # Add the last line
        if current_line:
            lines.append(current_line)

        return lines


class RPSGame(MainGame):
    def __init__(self, game):
        MainGame.__init__(self, game)
        self.display_options = False
        self.state = 'paper'
        self.options = ('rock', 'paper', 'scissors')
        self.selected_option = False

        self.rock_img = pygame.transform.scale(self.game.get_image('rock.png'), (250, 250))
        self.paper_img = pygame.transform.scale(self.game.get_image('paper.png'), (250, 250))
        self.scissors_img = pygame.transform.scale(self.game.get_image('scissor.png'), (250, 250))

        self.rock_rect = pygame.Rect(self.mid_w - 400, self.mid_h - 125, 250, 250)
        self.paper_rect = pygame.Rect(self.mid_w - 125, self.mid_h - 125, 250, 250)
        self.scissors_rect = pygame.Rect(self.mid_w + 150, self.mid_h - 125, 250, 250)

        self.border_color = self.game.BLACK
        self.border_width = 5


    def play(self):
        self.run_display = True
        self.show_rules()

        while self.run_display:
            self.game.display.fill(self.game.BLACK)

            self.selected_option = random.choice(self.options)
            self.show_options()

            # todo show animation of shake and show results
            while True:
                self.game.display.fill(self.game.WHITE)
                self.blit_screen()



    def show_options(self):
        self.display_options = True
        while self.display_options:
            self.game.check_events()
            self.check_input()

            self.game.display.fill(self.game.WHITE)
            self.draw_options()

            self.blit_screen()


    def draw_options(self):
        if self.state == 'paper':
            pygame.draw.rect(self.game.display, self.border_color, self.paper_rect, self.border_width)
        elif self.state == 'rock':
            pygame.draw.rect(self.game.display, self.border_color, self.rock_rect, self.border_width)
        elif self.state == 'scissors':
            pygame.draw.rect(self.game.display, self.border_color, self.scissors_rect, self.border_width)

        self.game.display.blit(self.rock_img, self.rock_rect)
        self.game.display.blit(self.paper_img, self.paper_rect)
        self.game.display.blit(self.scissors_img, self.scissors_rect)


    def move_cursor(self):
        if self.game.LEFT_KEY:
            if self.state == 'paper':
                self.state = 'rock'
            elif self.state == 'rock':
                self.state = 'scissors'
            else:
                self.state = 'paper'
        elif self.game.RIGHT_KEY:
            if self.state == 'paper':
                self.state = 'scissors'
            elif self.state == 'rock':
                self.state = 'paper'
            else:
                self.state = 'rock'


    def check_input(self):
        self.move_cursor()

        if self.game.START_KEY:
            self.display_options = False