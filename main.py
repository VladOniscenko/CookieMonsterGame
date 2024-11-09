import pygame.time

from game import Game


def main():
    # game initialization
    g = Game()
    clock = pygame.time.Clock()

    # main loop that checks if game is still running
    while g.running:

        # clock speed Frames Per Second
        clock.tick(g.FPS)

        # display selection menu
        g.cur_menu.display_menu()

        # display rating scoreboard
        g.rating.display_rating()

        # main game loop
        g.game_loop()


if __name__ == '__main__':
    main()