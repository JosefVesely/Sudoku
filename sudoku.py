import pygame as pg

pg.init()
pg.display.set_caption("Sudoku")

# Constants
COLS, ROWS = (9, 9)
SQUARE_SIZE = 64
GRID_MARGIN = 32
WINDOW_WIDTH = ROWS * SQUARE_SIZE + 2 * GRID_MARGIN
WINDOW_HEIGHT = COLS * SQUARE_SIZE + 2 * GRID_MARGIN
KEY_DIGITS = [
    pg.K_0, pg.K_1, pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9
]

grid = [
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

grid1 = list(map(list, grid))

screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pg.time.Clock()
font = pg.font.Font(None, 100)

selected_num = 0


def get_square():
    mouse_pos = pg.mouse.get_pos()
    x = (mouse_pos[0] - GRID_MARGIN) // SQUARE_SIZE
    y = (mouse_pos[1] - GRID_MARGIN) // SQUARE_SIZE

    if (x >= 0 and x < 9) and (y >= 0 and y < 9):
        return (x, y)
    return None


def draw_grid(screen, grid):
    line_width = 2

    # Draw bg on selected numbers
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x] == selected_num and selected_num != 0:
                pg.draw.rect(screen, (179, 217, 255), pg.Rect(GRID_MARGIN + x*SQUARE_SIZE, GRID_MARGIN + y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    for i in range(ROWS + 1): # Vertical lines
        if i % 3 == 0:
            line_width = 4

        pg.draw.line(screen, (70, 70, 70), (GRID_MARGIN + i * SQUARE_SIZE, GRID_MARGIN), (GRID_MARGIN + i * SQUARE_SIZE, GRID_MARGIN + COLS * SQUARE_SIZE), width=line_width)
        line_width = 2

    for i in range(COLS + 1): # Horizontal lines
        if i % 3 == 0:
            line_width = 4

        pg.draw.line(screen, (70, 70, 70), (GRID_MARGIN, GRID_MARGIN + i * SQUARE_SIZE), (GRID_MARGIN + COLS * SQUARE_SIZE, GRID_MARGIN + i * SQUARE_SIZE), width=line_width)
        line_width = 2

    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x] != 0:
                if grid1[y][x] != 0:
                    color = (0, 0, 0)
                else:
                    color = (90, 90, 90)

                font = pg.font.Font(None, 64)
                text = font.render(str(grid[y][x]), True, color)
                screen.blit(text, (54 + x * SQUARE_SIZE, 46 + y * SQUARE_SIZE))



# Main game loop

while True:
    clock.tick(60)
    screen.fill((255, 255, 255))

    # Input
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

        if event.type == pg.KEYDOWN:
            if event.key in KEY_DIGITS:
                if get_square():
                    x, y = get_square()

                    if grid1[y][x] == 0:
                        num = event.key - pg.K_0
                        grid[y][x] = num
                        selected_num = num
        
        if event.type == pg.MOUSEBUTTONDOWN:
            if get_square():
                x, y = get_square()
                selected_num = grid[y][x]

    # UPDATE


    # RENDER
    draw_grid(screen, grid)

    pg.display.update()

pg.quit()