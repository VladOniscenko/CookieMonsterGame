from symtable import Class

import pygame

class MiniGame:
    def __init__(self, game):
        self.game = game
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
                'class': RPSGame,
                'title': 'Rock Paper Scissor',
                'rules': "In Rock, Paper, Scissors, two players each choose one of three options: Rock, Paper, or Scissors. \nRock beats Scissors, Scissors beats Paper, and Paper beats Rock. \nIf both players choose the same option, the round is a tie. \nThe game is usually played in multiple rounds, and the player with the most wins is the overall winner.",
                'total_attempts': {
                    'easy': 3,
                    'medium': 2,
                    'hard': 1
                }
            }
        }


    def configure(self):
        self.reset_config()
        self.total_attempts = self.get_rule_value('total_attempts')
        self.title = self.get_rule_value('title')
        self.rules = self.get_rule_value('rules')

        # todo set cur_game and call play()
        # self.cur_game = self.get_rule_value('class')

    def reset_config(self):
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


class RPSGame(MiniGame):
    def __init__(self, game):
        MiniGame.__init__(self, game)
        self.run_display = False


    def play(self):
        self.run_display = True
        while self.run_display:
            print(self.rules)