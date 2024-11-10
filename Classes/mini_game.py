import random
import time

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
        self.tie = 0
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
        self.win_condition = False
        self.display_options = False
        self.state = 'paper'
        self.options = ('rock', 'paper', 'scissors')
        self.random_option = False
        self.display_animation = False

        # load images
        self.rock_img = self.game.get_image('rock.png')
        self.paper_img = self.game.get_image('paper.png')
        self.scissors_img = self.game.get_image('scissors.png')

        self.l_rock_img = self.game.get_image('l_rock.png')
        self.l_paper_img = self.game.get_image('l_paper.png')
        self.l_scissors_img = self.game.get_image('l_scissors.png')

        # large right options
        self.right_rock = pygame.transform.scale(self.rock_img, (500, 500))
        self.right_rock_rect = pygame.Rect(self.game.DISPLAY_W - 400, self.mid_h // 2, 500, 500)
        self.right_paper = pygame.transform.scale(self.paper_img, (500, 500))
        self.right_paper_rect = pygame.Rect(self.game.DISPLAY_W - 400, self.mid_h // 2, 500, 500)
        self.right_scissors = pygame.transform.scale(self.scissors_img, (500, 500))
        self.right_scissors_rect = pygame.Rect(self.game.DISPLAY_W - 400, self.mid_h // 2, 500, 500)

        # large left options
        self.left_rock = pygame.transform.scale(self.l_rock_img, (500, 500))
        self.left_rock_rect = pygame.Rect(-100, self.mid_h // 2, 500, 500)
        self.left_paper = pygame.transform.scale(self.l_paper_img, (500, 500))
        self.left_paper_rect = pygame.Rect(-100, self.mid_h // 2, 500, 500)
        self.left_scissors = pygame.transform.scale(self.l_scissors_img, (500, 500))
        self.left_scissors_rect = pygame.Rect(-100, self.mid_h // 2, 500, 500)

        # small options for selection
        self.rock = pygame.transform.scale(self.rock_img, (250, 250))
        self.paper = pygame.transform.scale(self.paper_img, (250, 250))
        self.scissors = pygame.transform.scale(self.scissors_img, (250, 250))

        self.rock_rect = pygame.Rect(self.mid_w - 400, self.mid_h - 125, 250, 250)
        self.paper_rect = pygame.Rect(self.mid_w - 125, self.mid_h - 125, 250, 250)
        self.scissors_rect = pygame.Rect(self.mid_w + 150, self.mid_h - 125, 250, 250)

        # selection border
        self.border_color = self.game.RED
        self.border_width = 5

    def check_user_won(self):
        self.total_attempts += 1

        if self.state == self.random_option:
            self.win_condition = None
            self.tie += 1
        elif (self.state == 'rock' and self.random_option == 'scissors') or \
                (self.state == 'paper' and self.random_option == 'rock') or \
                (self.state == 'scissors' and self.random_option == 'paper'):
            self.win_condition = True
            self.correct += 1
        else:
            self.win_condition = False
            self.incorrect += 1


    def play(self):
        self.run_display = True
        self.show_rules()

        while self.run_display:
            self.game.display.fill(self.game.BLACK)

            self.random_option = random.choice(self.options)
            self.show_options()
            self.check_user_won()
            
            self.show_result()


    def show_options(self):
        self.display_options = True
        while self.display_options:
            self.game.check_events()
            self.check_input()

            self.game.display.fill(self.game.WHITE)

            self.show_score()
            self.draw_options()

            self.blit_screen()


    def show_result(self):
        self.display_animation = True
        start_time = time.time()

        cycle_duration = 0.5
        cycle_height = 250

        original_left_y = self.left_rock_rect.y
        original_right_y = self.right_rock_rect.y

        # Perform the animation
        while self.display_animation:
            elapsed_time = time.time() - start_time
            cycle_phase = (elapsed_time % cycle_duration) / (cycle_duration / 2)

            # check if time is not done max 2 sec and reset to default
            if elapsed_time > 2 * cycle_duration:
                self.display_animation = False
                self.left_rock_rect.y = original_left_y
                self.right_rock_rect.y = original_right_y
                break

            # Calculate vertical offset based on cycle phase
            if cycle_phase <= 1:
                offset = int(cycle_height * cycle_phase)  # Moving up
            else:
                offset = int(cycle_height * (2 - cycle_phase))  # Moving down

            # Apply the offset to the rock positions
            self.left_rock_rect.y = original_left_y - offset
            self.right_rock_rect.y = original_right_y - offset

            # Render the updated positions
            self.game.display.fill(self.game.WHITE)
            self.game.display.blit(self.right_rock, self.right_rock_rect)
            self.game.display.blit(self.left_rock, self.left_rock_rect)
            self.blit_screen()

            # Delay for smooth animation
            pygame.time.delay(20)

        start_time = time.time()
        while time.time() - start_time < 2:
            self.game.display.fill(self.game.WHITE)

            if self.state == 'rock':
                self.game.display.blit(self.right_rock, self.right_rock_rect)
            elif self.state == 'paper':
                self.game.display.blit(self.right_paper, self.right_paper_rect)
            else:
                self.game.display.blit(self.right_scissors, self.right_scissors_rect)

            if self.random_option == 'rock':
                self.game.display.blit(self.left_rock, self.left_rock_rect)
            elif self.random_option == 'paper':
                self.game.display.blit(self.left_paper, self.left_paper_rect)
            else:
                self.game.display.blit(self.left_scissors, self.left_scissors_rect)

            # Display result text
            if self.win_condition is None:
                self.game.draw_text('Tie', 30, self.mid_w, self.mid_h, position='center')
            elif self.win_condition:
                self.game.draw_text('You Win', 30, self.mid_w, self.mid_h, position='center', color=self.game.GREEN)
            else:
                self.game.draw_text('You Lose', 30, self.mid_w, self.mid_h, position='center', color=self.game.RED)

            self.blit_screen()

    def show_score(self):
        self.game.draw_text(str(self.incorrect), 50, 15, 10, color=self.game.RED)

        self.game.draw_text(str(self.correct), 50, self.game.DISPLAY_W - 15, 10, color=self.game.GREEN, position='topright')

        self.game.draw_text(str(self.tie), 50, self.game.DISPLAY_W // 2, 40, color=self.game.ORANGE, position='center')

    def draw_options(self):
        if self.state == 'paper':
            pygame.draw.rect(self.game.display, self.border_color, self.paper_rect, self.border_width)
        elif self.state == 'rock':
            pygame.draw.rect(self.game.display, self.border_color, self.rock_rect, self.border_width)
        elif self.state == 'scissors':
            pygame.draw.rect(self.game.display, self.border_color, self.scissors_rect, self.border_width)

        self.game.display.blit(self.rock, self.rock_rect)
        self.game.display.blit(self.paper, self.paper_rect)
        self.game.display.blit(self.scissors, self.scissors_rect)


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