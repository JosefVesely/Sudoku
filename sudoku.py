import pygame as pg

pg.init()
pg.display.set_caption("Sudoku")

# Constants
COLS, ROWS = (9, 9)
SQUARE_SIZE = 64
GRID_MARGIN = 32
WINDOW_WIDTH = ROWS*SQUARE_SIZE + 2*GRID_MARGIN
WINDOW_HEIGHT = COLS*SQUARE_SIZE + 2*GRID_MARGIN
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

grid_solved = [
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

grid_initial = list(map(list, grid))

screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pg.time.Clock()
font = pg.font.Font(None, 100)

selected_num = 0
selected_square = None

def get_square():
    mouse_pos = pg.mouse.get_pos()
    x = (mouse_pos[0] - GRID_MARGIN) // SQUARE_SIZE
    y = (mouse_pos[1] - GRID_MARGIN) // SQUARE_SIZE

    if (x >= 0 and x < 9) and (y >= 0 and y < 9):
        return (x, y)
    return None

def print_grid(grid) -> None:
    for y in range(ROWS):
        if y % 3 == 0 and y != 0: # Horizontal line
            print("-" * 21)

        for x in range(COLS):
            if (x % 3 == 0 and x != 0): # Vertical line
                print("| ", end="") 
            
            if grid[y][x] == 0:
                print(". ", end="")
            else:
                print(grid[y][x], end=" ")
        print()


def draw_grid(screen, grid) -> None:
    line_width = 1
    color = (70, 70, 70)

    # Draw selected square
    if selected_square:
        x, y = selected_square

        # 3x3 box
        box_x, box_y = x // 3, y // 3
        pg.draw.rect(screen, (204, 230, 255), pg.Rect(GRID_MARGIN + 3 * box_x * SQUARE_SIZE, GRID_MARGIN + 3 * box_y * SQUARE_SIZE, 3 * SQUARE_SIZE, 3 * SQUARE_SIZE))

        # Horizontal squares
        pg.draw.rect(screen, (204, 230, 255), pg.Rect(GRID_MARGIN, GRID_MARGIN + y*SQUARE_SIZE, COLS * SQUARE_SIZE, SQUARE_SIZE))

        # Vertical squares
        pg.draw.rect(screen, (204, 230, 255), pg.Rect(GRID_MARGIN + x*SQUARE_SIZE, GRID_MARGIN, SQUARE_SIZE, ROWS * SQUARE_SIZE))

        # Selected square
        pg.draw.rect(screen, (153, 204, 255), pg.Rect(GRID_MARGIN + x*SQUARE_SIZE, GRID_MARGIN + y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))



    # Draw bg on selected numbers
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x] == selected_num and selected_num != 0:
                pg.draw.rect(screen, (128, 193, 255), pg.Rect(GRID_MARGIN + x*SQUARE_SIZE, GRID_MARGIN + y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Lines
    

    for i in range(ROWS+1): # Vertical lines
        if i % 3 == 0:
            line_width = 2
            color = (60, 60, 60)
        else:
            color = (100, 100, 100)

        pg.draw.line(screen, color, (GRID_MARGIN + i*SQUARE_SIZE, GRID_MARGIN), (GRID_MARGIN + i*SQUARE_SIZE, GRID_MARGIN + COLS*SQUARE_SIZE), width=line_width)
        line_width = 1

    for i in range(COLS+1): # Horizontal lines
        if i % 3 == 0:
            line_width = 2
            color = (60, 60, 60)
        else:
            color = (100, 100, 100)

        pg.draw.line(screen, color, (GRID_MARGIN, GRID_MARGIN + i*SQUARE_SIZE), (GRID_MARGIN + COLS*SQUARE_SIZE, GRID_MARGIN + i*SQUARE_SIZE), width=line_width)
        line_width = 1

    # Draw numbers
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x] != 0:
                color =  (0, 0, 0) if grid_initial[y][x] else (100, 100, 100)

                font = pg.font.Font(pg.font.match_font("malgungothicsemilight"), 45)
                text = font.render(str(grid[y][x]), True, color)
                x_offset = 57 if grid[y][x] == 1 else 53
                
                screen.blit(text, (x_offset + x*SQUARE_SIZE, 33 + y*SQUARE_SIZE))



# Main game loop

while True:
    clock.tick(60)
    screen.fill((255, 255, 255))

    # Input
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

        if event.type == pg.KEYDOWN:
            if event.key in KEY_DIGITS and selected_square:
                x, y = selected_square

                if grid_initial[y][x] == 0:
                    num = event.key - pg.K_0

                    if grid[y][x] == num:
                        grid[y][x] = 0
                    else:
                        grid[y][x] = num
                        selected_num = num

            if event.key == pg.K_ESCAPE:
                selected_square = None
                selected_num = 0
                   
        
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                if get_square():
                    x, y = get_square()
                    selected_num = grid[y][x]
                    selected_square = (x, y)

    # UPDATE


    # RENDER
    draw_grid(screen, grid)

    pg.display.update()

pg.quit()