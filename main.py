from game import Game

# game initialization
g = Game()

# main loop that checks if game is still running
while g.running:
    # display selection menu
    g.cur_menu.display_menu()

    # display rating scoreboard
    g.rating.display_rating()

    # main game loop
    g.game_loop()
