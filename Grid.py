import pygame as pg
from colors import Color

class Grid:
    def __init__(self):
        # Constants
        self.COLS, self.ROWS = 9, 9
        self.SQUARE_SIZE = 64
        self.MARGIN = 32
        # Grid
        self.grid = []
        self.grid_initial = []
        self.grid_solved = []
        # Highlighting
        self.highlighted_num = 0
        self.selected_square = ()
        # Init
        self.generate()
        self.solve()

    def generate(self): # Just this for now
        self.grid = [
            [ 4, 0, 5, 7, 0, 0, 0, 0, 6 ],
            [ 0, 0, 0, 0, 0, 2, 0, 9, 0 ],
            [ 8, 9, 0, 0, 0, 0, 0, 3, 7 ],
            [ 1, 3, 4, 8, 9, 0, 6, 7, 0 ],
            [ 9, 6, 0, 2, 7, 4, 5, 1, 0 ],
            [ 0, 0, 0, 0, 0, 3, 8, 4, 0 ],
            [ 3, 0, 9, 0, 2, 6, 0, 0, 0 ],
            [ 0, 5, 0, 0, 0, 0, 0, 0, 4 ],
            [ 0, 0, 0, 9, 5, 0, 0, 6, 0 ]
        ]
        self.grid_initial = list(map(list, self.grid))

    def solve(self): # Just this for now
        self.grid_solved = [
            [ 4, 2, 5, 7, 3, 9, 1, 8, 6 ],
            [ 7, 1, 3, 6, 8, 2, 4, 9, 5 ],
            [ 8, 9, 6, 5, 4, 1, 2, 3, 7 ],
            [ 1, 3, 4, 8, 9, 5, 6, 7, 2 ],
            [ 9, 6, 8, 2, 7, 4, 5, 1, 3 ],
            [ 5, 7, 2, 1, 6, 3, 8, 4, 9 ],
            [ 3, 8, 9, 4, 2, 6, 7, 5, 1 ],
            [ 6, 5, 7, 3, 1, 8, 9, 2, 4 ],
            [ 2, 4, 1, 9, 5, 7, 3, 6, 8 ]
        ]

    def get_square(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        x = (mouse_x - self.MARGIN) // self.SQUARE_SIZE
        y = (mouse_y - self.MARGIN) // self.SQUARE_SIZE

        if (0 <= x and x < 9) and (0 <= y and y < 9):
            return [x, y]
        return None
    
    def update(self):
        self.highlighted_num = self.grid[self.selected_square[0], self.selected_square[0]]

    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                # Keys 1 to 9
                if self.selected_square and event.key in [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9,
                                                          pg.K_KP_1, pg.K_KP_2, pg.K_KP_3, pg.K_KP_4, pg.K_KP_5, pg.K_KP_6, pg.K_KP_7, pg.K_KP_8, pg.K_KP_9]:
                    x, y = self.selected_square

                    if self.grid_initial[y][x] == 0:
                        if event.key >= pg.K_KP_1: # Numpad
                            num = event.key - pg.K_KP_1 + 1
                        else:
                            num = event.key - pg.K_0

                        if self.grid[y][x] == num:
                            self.grid[y][x] = 0
                        else:
                            self.grid[y][x] = num
                            self.highlighted_num = num

                if event.key in [pg.K_0, pg.K_KP0, pg.K_BACKSPACE, pg.K_DELETE]:
                    x, y = self.selected_square

                    if self.grid_initial[y][x] == 0:
                        self.grid[y][x] = 0

                if event.key == pg.K_ESCAPE:
                    self.highlighted_num = 0
                    self.selected_square = None
                    
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 or event.button == 3: # Left or right click
                    if self.get_square(): # Select square
                        x, y = self.get_square()
                        self.highlighted_num = self.grid[y][x]
                        self.selected_square = (x, y)

    def draw(self, screen):
        # Highlighting
        if self.selected_square:
            x, y = self.selected_square

            # 3x3 box
            box_x, box_y = x // 3, y // 3
            pg.draw.rect(screen, Color.LIGHTERBLUE, pg.Rect(self.MARGIN+3*box_x*self.SQUARE_SIZE, self.MARGIN+3*box_y*self.SQUARE_SIZE, 3*self.SQUARE_SIZE, 3*self.SQUARE_SIZE))

            # Horizontal squares
            pg.draw.rect(screen, Color.LIGHTERBLUE, pg.Rect(self.MARGIN, self.MARGIN+y*self.SQUARE_SIZE, self.COLS*self.SQUARE_SIZE, self.SQUARE_SIZE))

            # Vertical squares
            pg.draw.rect(screen, Color.LIGHTERBLUE, pg.Rect(self.MARGIN+x*self.SQUARE_SIZE, self.MARGIN, self.SQUARE_SIZE, self.ROWS*self.SQUARE_SIZE))

            # Selected square
            pg.draw.rect(screen, Color.LIGHTBLUE, pg.Rect(self.MARGIN+x*self.SQUARE_SIZE, self.MARGIN+y*self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

        # Draw bg on selected numbers
        for y in range(self.ROWS):
            for x in range(self.COLS):
                if self.grid[y][x] == self.highlighted_num and self.highlighted_num != 0:
                    pg.draw.rect(screen, Color.BLUE, pg.Rect(self.MARGIN+x*self.SQUARE_SIZE, self.MARGIN+y*self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

        # Lines
        for i in range(self.ROWS+1): # Vertical lines
            if i % 3 == 0: color, line_width = Color.GRAY, 2
            else:          color, line_width = Color.LIGHTGRAY, 1

            pg.draw.line(screen, color, (self.MARGIN+i*self.SQUARE_SIZE, self.MARGIN), (self.MARGIN+i*self.SQUARE_SIZE, self.MARGIN+self.COLS*self.SQUARE_SIZE), width=line_width)
                
        for i in range(self.COLS+1): # Horizontal lines
            if i % 3 == 0: color, line_width = Color.GRAY, 2
            else:          color, line_width = Color.LIGHTGRAY, 1

            pg.draw.line(screen, color, (self.MARGIN, self.MARGIN+i*self.SQUARE_SIZE), (self.MARGIN+self.COLS*self.SQUARE_SIZE, self.MARGIN+i*self.SQUARE_SIZE), width=line_width)

        # Numbers
        for y in range(self.ROWS):
            for x in range(self.COLS):
                num = self.grid[y][x]

                if num == 0: continue

                if self.grid_initial[y][x]:
                    color = Color.BLACK
                elif self.grid_solved[y][x] != self.grid[y][x]:
                    color = Color.RED
                else:
                    color = Color.LIGHTGRAY

                font = pg.font.Font(pg.font.match_font("malgungothicsemilight"), 45)
                text = font.render(str(num), True, color)
                text_rect = text.get_rect(center=(self.MARGIN+x*self.SQUARE_SIZE+self.SQUARE_SIZE/2, 
                                                  self.MARGIN+y*self.SQUARE_SIZE+self.SQUARE_SIZE/2))
                screen.blit(text, text_rect)
