import random
import time
from functions import *
import pygame
from dataclasses import dataclass

RPS_OPTIONS = ('rock', 'paper', 'scissors')

class MainGame:
    def __init__(self, game) -> None:
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W // 2, self.game.DISPLAY_H // 2

        self.run_display, self.show_rules, self.running = True, True, False
        self.total_attempts, self.attempt, self.correct, self.incorrect, self.tie, self.title, self.rules = 0, 0, 0, 0, 0, '', ''

        self.game_rules = {
            'rps': {
                'title': 'Rock Paper Scissor',
                'rules': "In Rock, Paper, Scissors, two players each choose one of three options: Rock, Paper, or Scissors. Rock beats Scissors, Scissors beats Paper, and Paper beats Rock. If both players choose the same option, the round is a tie. The game is usually played in multiple rounds, and the player with the most wins is the overall winner.",
                'total_attempts': {
                    'easy': 3,
                    'medium': 2,
                    'hard': 1
                }
            },
            'hangman': {
                'title': 'Hangman',
                'rules': "In Hangman, one player chooses a word, and the others guess letters to reveal it. Correct guesses fill in blanks, while wrong guesses bring the hangman closer to completion. The goal: guess the word before the drawing is finished!",
                'total_attempts': {
                    'easy': ['cat', 'book', 'tree', 'dog', 'fish'],
                    'medium': ['planet', 'guitar', 'ocean', 'jungle', 'basket'],
                    'hard': ['microscope', 'astronomy', 'philosophy', 'quadrilateral', 'hypothesis']
                }
            }
        }


    def configure(self) -> None:
        self.reset_game()
        self.total_attempts = self.get_rule_value('total_attempts')
        self.title = self.get_rule_value('title')
        self.rules = self.get_rule_value('rules')


    def reset_game(self) -> None:
        self.total_attempts, self.tie, self.attempt, self.correct, self.incorrect, self.title, self.rules = 0, 0, 0, 0, 0, '', ''


    def get_rule_value(self, column_name):
        rule = self.game_rules.get(self.game.game_mode, {}).get(column_name)
        if isinstance(rule, dict):
            return rule.get(self.game.difficulty, 1)
        return rule


    def blit_screen(self) -> None:
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


    def display_rules(self) -> None:
        self.show_rules = True
        font_size = 30
        line_height = font_size + 5
        lines = split_text(self.rules, self.game.second_font, font_size, self.mid_w)

        while self.show_rules:
            self.game.check_events()

            if self.game.START_KEY:
                self.show_rules = False

            self.game.display.fill(self.game.WHITE)

            for idx, line in enumerate(lines):
                self.game.draw_text(line, font_size, self.mid_w, self.mid_h - len(lines) * line_height // 2 + idx * line_height, font=self.game.second_font, position='center')

            self.game.draw_text(self.title, 50, self.mid_w, self.mid_h - 200, font=self.game.second_font, position='center')
            self.game.draw_text('PRESS ENTER TO PLAY >>', font_size, self.mid_w, self.mid_h + 200, font=self.game.second_font, position='center', color=self.game.RED)

            self.blit_screen()


class RPSGame(MainGame):
    def __init__(self, game):
        MainGame.__init__(self, game)
        self.is_winner = False
        self.user_selected = False
        self.state = 'paper'
        self.random_option = False
        self.show_animation = False

        self.result_text = {
            None: ('Tie', self.game.BLACK),
            True: ('You Win', self.game.GREEN),
            False: ('You Lose', self.game.RED)
        }

        # small right options
        sm_w, sm_h, gap = 150, 150, 175
        self.s_rock = Hand(game, 'rock', sm_w, sm_h, (self.game.DISPLAY_W - sm_w) // 2 - gap, (self.game.DISPLAY_H - sm_w) // 2)
        self.s_paper = Hand(game, 'paper', sm_w, sm_h, (self.game.DISPLAY_W - sm_w) // 2, (self.game.DISPLAY_H - sm_w) // 2)
        self.s_scissors = Hand(game, 'scissors', sm_w, sm_h, (self.game.DISPLAY_W - sm_w) // 2 + gap, (self.game.DISPLAY_H - sm_w) // 2)

        # large right options
        lg_w, lg_h, h_pos = 500, 500, self.mid_h // 2
        self.r_rock = Hand(game, 'rock', lg_w, lg_h, self.game.DISPLAY_W - 400, self.mid_h // 2)
        self.r_paper = Hand(game, 'paper', lg_w, lg_h, self.game.DISPLAY_W - 450, self.mid_h // 2)
        self.r_scissors = Hand(game, 'scissors', lg_w, lg_h, self.game.DISPLAY_W - 450, self.mid_h // 2)

        # large left options
        self.l_rock = Hand(game, 'rock', lg_w, lg_h, -100, self.mid_h // 2, True)
        self.l_paper = Hand(game, 'paper', lg_w, lg_h, -50, self.mid_h // 2, True)
        self.l_scissors = Hand(game, 'scissors', lg_w, lg_h, -50, self.mid_h // 2, True)

        self.options = {
            'paper': self.s_paper,'rock': self.s_rock,'scissors': self.s_scissors,
            'r_paper': self.r_paper,'r_rock': self.r_rock,'r_scissors': self.r_scissors,
            'l_paper': self.l_paper,'l_rock': self.l_rock,'l_scissors': self.l_scissors
        }


    def play(self) -> None:
        self.run_display = True
        while self.run_display:
            self.user_selected = False
            self.game.display.fill(self.game.WHITE)

            self.random_option = random.choice(RPS_OPTIONS)
            self.display_menu()
            self.display_score()

            if self.user_selected:
                self.attempt += 1
                self.did_user_win()
                self.display_result()

                if self.attempt == self.total_attempts or self.is_winner:
                    self.run_display = False

            self.blit_screen()


    def did_user_win(self) -> None:
        if self.state == self.random_option:
            self.is_winner = None
            self.tie += 1
        elif (self.state == 'rock' and self.random_option == 'scissors') or \
                (self.state == 'paper' and self.random_option == 'rock') or \
                (self.state == 'scissors' and self.random_option == 'paper'):
            self.is_winner = True
            self.correct += 1
        else:
            self.is_winner = False
            self.incorrect += 1


    def display_menu(self) -> None:
        self.game.check_events()
        self.check_input()
        self.draw_options()


    def display_result(self) -> None:
        self.display_animation()

        start_time = time.time()
        while time.time() - start_time < 2:
            self.game.display.fill(self.game.WHITE)

            # display right and left large hand selected by user and game
            self.options[f'r_{self.state}'].draw()
            self.options[f'l_{self.random_option}'].draw()

            # Display result text
            text, color = self.result_text[self.is_winner]
            self.game.draw_text(text, 30, self.mid_w, self.mid_h, position='center', color=color)

            self.blit_screen()


    def display_score(self) -> None:
        self.game.draw_text(self.incorrect, 50, 15, 10, color=self.game.RED)
        self.game.draw_text(self.correct, 50, self.game.DISPLAY_W - 15, 10, color=self.game.GREEN, position='topright')
        self.game.draw_text(self.tie, 50, self.game.DISPLAY_W // 2, 40, color=self.game.ORANGE, position='center')


    def display_animation(self) -> None:
        start_time = time.time()

        cycles = 2
        cycle_height = 250
        cycle_duration = 0.25

        original_left_y = self.l_rock.rect.y
        original_right_y = self.r_rock.rect.y

        # Perform the animation
        self.show_animation = True
        while self.show_animation:
            elapsed_time = time.time() - start_time
            cycle_phase = (elapsed_time % cycle_duration) / (cycle_duration / 2)

            # check if time is not done max 2 sec and reset to default
            if elapsed_time > cycles * cycle_duration:
                self.show_animation = False
                self.l_rock.rect.y = original_left_y
                self.r_rock.rect.y = original_right_y
                break

            # Calculate vertical offset based on cycle phase
            if cycle_phase <= 1:
                offset = int(cycle_height * cycle_phase)  # Moving up
            else:
                offset = int(cycle_height * (2 - cycle_phase))  # Moving down

            # Apply the offset to the rock positions
            self.l_rock.rect.y = original_left_y - offset
            self.r_rock.rect.y = original_right_y - offset

            # Render the updated positions
            self.game.display.fill(self.game.WHITE)
            self.display_large_hands()
            self.blit_screen()


    def draw_options(self) -> None:
        option = self.options[self.state]
        pygame.draw.rect(self.game.display, option.border_color, option.rect, option.border_width)

        self.s_rock.draw()
        self.s_paper.draw()
        self.s_scissors.draw()

        self.display_large_hands()


    def move_cursor(self) -> None:
        # get index of user selected option of (rock, paper, scissors)
        current_index = RPS_OPTIONS.index(self.state)

        # check if user clicks left or to the right
        # set current selected option
        if self.game.LEFT_KEY:
            self.state = RPS_OPTIONS[(current_index - 1) % len(RPS_OPTIONS)]
        elif self.game.RIGHT_KEY:
            self.state = RPS_OPTIONS[(current_index + 1) % len(RPS_OPTIONS)]


    def check_input(self) -> None:
        self.move_cursor()
        if self.game.START_KEY:
            self.user_selected = self.state


    def display_large_hands(self) -> None:
        self.r_rock.draw()
        self.l_rock.draw()


class Hand:
    def __init__(self, game, hand_type, w, h, x, y, left_handed=False) -> None:
        if hand_type not in RPS_OPTIONS:
            raise ValueError('Hand type is not valid!')

        self.game = game
        self.type = hand_type
        self.left_handed = left_handed
        self.w, self.h, self.x, self.y = w, h, x, y

        self.__loaded_img = get_image((f'{self.type}' if not self.left_handed else f'l_{self.type}') + '.png')
        self.img = pygame.transform.scale(self.__loaded_img, (self.w, self.h))

        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        self.border_color = self.game.RED
        self.border_width = 5

    def draw(self) -> None:
        self.game.display.blit(self.img, self.rect)


@dataclass
class Alphabet:
    name: str
    x: int
    y: int
    h: int
    w: int
    is_used: bool = False


class HangmanGame(MainGame):
    def __init__(self, game):
        MainGame.__init__(self, game)
        self.is_winner = False
        self.user_selected = False
        self.state = False
        self.alphabet_objects = []
        self.used_options = []

        x, y = 20, 20
        for letter in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
            self.alphabet_objects.append(Alphabet(name=letter.upper(), x=x, y=y, h=35, w=35))
            x += 30

    def play(self) -> None:
        self.run_display = True
        while self.run_display:
            self.user_selected = False

            self.game.display.fill(self.game.WHITE)
            self.game.draw_text('Make a choice', 40, self.mid_w, 75, position='center')

            self.draw_gallows()

            self.draw_options()

            self.blit_screen()


    def did_user_win(self) -> None:
        return False


    def display_menu(self) -> None:
        pass

    def display_result(self) -> None:
        pass


    def display_score(self) -> None:
        pass


    def draw_options(self) -> None:

        rect_x, rect_y, rect_width, rect_height = 50, self.game.DISPLAY_H - 90, 40, 40
        step = (self.game.DISPLAY_W - (len(self.alphabet_objects) * 3.5)) / len(self.alphabet_objects)

        for obj in self.alphabet_objects:
            color = self.game.BLACK
            if obj.name in self.used_options:
                color = self.game.RED

            self.game.draw_text(obj.name, 24, (rect_x + rect_width // 2) + 2, (rect_y + rect_height // 2) - 2.5,
                                position='center', color=color)
            rect_x += step


        self.blit_screen()


    def move_cursor(self) -> None:
        pass


    def check_input(self) -> None:
        self.move_cursor()
        if self.game.START_KEY:
            self.user_selected = self.state

    def draw_gallows(self):
        # horizontal bottom line
        pygame.draw.rect(self.game.display, self.game.BLACK,
                         (350, self.game.DISPLAY_H - 250, self.game.DISPLAY_W - 650, 10))

        # vertical right long line
        pygame.draw.rect(self.game.display, self.game.BLACK, (self.game.DISPLAY_W - 475, 200, 15, 275))

        # horizontal top line
        pygame.draw.rect(self.game.display, self.game.BLACK, (650, self.game.DISPLAY_H - 525, 170, 10))

        # vertical top line
        pygame.draw.rect(self.game.display, self.game.BLACK, (650, 200, 15, 50))

        # slanted line
        pygame.draw.line(self.game.display, self.game.BLACK, (750, self.game.DISPLAY_H - 525), (810, self.game.DISPLAY_H - 450), 15)

