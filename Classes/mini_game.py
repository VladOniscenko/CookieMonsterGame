import pygame


class MainGame:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.option_offset = 40

        self.run_display = True
        self.display_rules = True
        self.running = False

        self.total_attempts = 0
        self.attempt = 0
        self.correct = 0
        self.incorrect = 0
        self.title = ''
        self.rules = ''

        self.cur_game = False
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


    def play(self):
        self.run_display = True
        self.show_rules()

        while self.run_display:
            self.game.display.fill(self.game.BLACK)

            # todo make game


            self.blit_screen()