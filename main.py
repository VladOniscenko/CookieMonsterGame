import pygame.time

from Classes.game import Game


def main():
    # game initialization
    g = Game()
    clock = pygame.time.Clock()

    # main loop that checks if game is still running
    while g.running:
        # clock speed Frames Per Second
        clock.tick(g.FPS)

        # display rating scoreboard
        g.rating.display_rating()

        # display selection menu
        g.main_menu.display_menu()

        # display selection menu
        g.difficulties.display_menu()

        # main game loop
        g.game_loop()


if __name__ == '__main__':
    main()
