from game import Game


g = Game()

while g.running:

    g.cur_menu.display_menu()
    g.game_loop()






















# import sys
#
# import pygame
# from pygame.examples.scrap_clipboard import screen
#
# pygame.init()
#
# # SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# SCREEN = pygame.display.set_mode((1280, 720))
# WIDTH, HEIGHT = SCREEN.get_size()
# FONT = pygame.font.Font(None, 36)
#
# BG = pygame.image.load("assets/bg.png")
# BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
#
# def main_menu():
#     pygame.display.set_caption('Menu') # set window title
#
#     while True:
#         SCREEN.blit(BG, (0,0))
#
#         MENU_MOUSE_POS = pygame.mouse.get_pos()
#         MENU_TEXT = FONT.render('Play', True, '#b68f40')
#         MENU_RECT = MENU_TEXT.get_rect(center=(150, HEIGHT / 2))
#
#         SCREEN.blit(MENU_TEXT, MENU_RECT)
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#
#         pygame.display.update()
#
# if __name__ == '__main__':
#     main_menu()