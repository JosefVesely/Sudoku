import pygame as pg
from enum import Enum
from colors import Color
from Grid import Grid

class GameState(Enum):
    MENU = 1
    GAME = 2
    GAMEOVER = 3

class Sudoku:
    def __init__(self):
        # Constants
        self.WINDOW_WIDTH = 640
        self.WINDOW_HEIGHT = 640
        self.FPS = 60
        # Init PyGame
        pg.init()
        pg.display.set_caption("Sudoku")
        pg.display.set_icon(pg.image.load("icon.png"))
        
        self.screen = pg.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.clock = pg.time.Clock()      
        self.game_state = GameState.GAME

    def run(self):
        grid = Grid()

        # Game loop
        while self.game_state == GameState.GAME:
            self.clock.tick(self.FPS)
            self.screen.fill(Color.WHITE)

            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            # Render
            grid.draw(self.screen)

            # Handle events
            grid.handle_events(events)

            pg.display.update()

        pg.quit()