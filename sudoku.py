import pygame as pg
from pygame import gfxdraw
import tkinter as tk
from tkinter import messagebox

pg.init()
pg.display.set_caption("Sudoku")
pg.display.set_icon(pg.image.load("icon.png"))
tk.Tk().wm_withdraw()

# Constants
COLS, ROWS = 9, 9
SQUARE_SIZE = 64
GRID_MARGIN = 32
WINDOW_WIDTH = ROWS*SQUARE_SIZE + 2*GRID_MARGIN + 256
WINDOW_HEIGHT = COLS*SQUARE_SIZE + 3*GRID_MARGIN + SQUARE_SIZE
KEY_DIGITS = [pg.K_0, pg.K_1, pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]

class Color:
    LIGHTERBLUE = (204, 230, 255)
    LIGHTBLUE   = (153, 204, 255)
    BLUE        = (128, 193, 255)
    GRAY        = (60, 60, 60)
    LIGHTGRAY   = (100, 100, 100)
    BLACK       = (0, 0, 0)
    GREEN       = (179, 255, 179)
    RED         = (255, 77, 77)


screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pg.time.Clock()

grid = [
    [ 4, 2, 5, 7, 3, 9, 1, 8, 6 ],
    [ 7, 1, 3, 6, 8, 2, 4, 9, 5 ],
    [ 8, 9, 6, 5, 4, 1, 2, 3, 7 ],
    [ 1, 3, 4, 8, 9, 5, 6, 7, 2 ],
    [ 9, 6, 8, 2, 7, 4, 5, 1, 3 ],
    [ 5, 7, 2, 1, 6, 3, 8, 4, 9 ],
    [ 3, 8, 9, 4, 2, 6, 0, 5, 1 ],
    [ 6, 5, 7, 3, 1, 8, 9, 2, 4 ],
    [ 2, 4, 1, 9, 5, 7, 3, 6, 8 ]
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

selected_num = 0
selected_square = None
mistakes = 0
time = 0 # seconds

def get_square():
    mouse_x, mouse_y = pg.mouse.get_pos()
    x = (mouse_x - GRID_MARGIN) // SQUARE_SIZE
    y = (mouse_y - GRID_MARGIN) // SQUARE_SIZE

    if (0 <= x and x < 9) and (0 <= y and y < 9):
        return (x, y)
    return None


def draw_grid(screen, grid) -> None:
    # Draw selected square
    if selected_square:
        x, y = selected_square

        # 3x3 box
        box_x, box_y = x // 3, y // 3
        pg.draw.rect(screen, Color.LIGHTERBLUE, pg.Rect(GRID_MARGIN+3*box_x*SQUARE_SIZE, GRID_MARGIN+3*box_y*SQUARE_SIZE, 3*SQUARE_SIZE, 3*SQUARE_SIZE))

        # Horizontal squares
        pg.draw.rect(screen, Color.LIGHTERBLUE, pg.Rect(GRID_MARGIN, GRID_MARGIN+y*SQUARE_SIZE, COLS*SQUARE_SIZE, SQUARE_SIZE))

        # Vertical squares
        pg.draw.rect(screen, Color.LIGHTERBLUE, pg.Rect(GRID_MARGIN + x*SQUARE_SIZE, GRID_MARGIN, SQUARE_SIZE, ROWS*SQUARE_SIZE))

        # Selected square
        pg.draw.rect(screen, Color.LIGHTBLUE, pg.Rect(GRID_MARGIN + x*SQUARE_SIZE, GRID_MARGIN + y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Draw bg on selected numbers
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x] == selected_num and selected_num != 0:
                pg.draw.rect(screen, Color.BLUE, pg.Rect(GRID_MARGIN + x*SQUARE_SIZE, GRID_MARGIN + y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Lines
    for i in range(ROWS+1): # Vertical lines
        if i % 3 == 0:
            line_width = 2
            color = Color.GRAY
        else:
            line_width = 1
            color = Color.LIGHTGRAY

        pg.draw.line(screen, color, (GRID_MARGIN+i*SQUARE_SIZE, GRID_MARGIN), (GRID_MARGIN+i*SQUARE_SIZE, GRID_MARGIN+COLS*SQUARE_SIZE), width=line_width)
        
    for i in range(COLS+1): # Horizontal lines
        if i % 3 == 0:
            line_width = 2
            color = Color.GRAY
        else:
            line_width = 1
            color = Color.LIGHTGRAY

        pg.draw.line(screen, color, (GRID_MARGIN, GRID_MARGIN+i*SQUARE_SIZE), (GRID_MARGIN+COLS*SQUARE_SIZE, GRID_MARGIN+i*SQUARE_SIZE), width=line_width)
        
    # Draw numbers
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x] != 0:
                color = Color.BLACK if grid_initial[y][x] else Color.LIGHTGRAY

                if grid_initial[y][x]:
                    color = Color.BLACK
                elif grid_solved[y][x] != grid[y][x]:
                    color = Color.RED
                else:
                    color = Color.LIGHTGRAY

                font = pg.font.Font(pg.font.match_font("malgungothicsemilight"), 45)
                text = font.render(str(grid[y][x]), True, color)
                x_offset = 57 if grid[y][x] == 1 else 53
                
                screen.blit(text, (x_offset + x*SQUARE_SIZE, 33 + y*SQUARE_SIZE))


def draw_number_selection(screen) -> None:
    # Draw circles
    for i in range(9):
        left = GRID_MARGIN + i*SQUARE_SIZE + SQUARE_SIZE/2
        top = 2*GRID_MARGIN+ROWS*SQUARE_SIZE + SQUARE_SIZE/2
        radius = SQUARE_SIZE/2.25


        # Draw green background if all 9 numbers are in the grid
        if sum([j.count(i+1) for j in grid]) >= 9:
            gfxdraw.filled_circle(screen, int(left), int(top), int(radius), Color.GREEN)

        elif selected_num == i+1:
            gfxdraw.filled_circle(screen, int(left), int(top), int(radius), Color.BLUE)
        
        gfxdraw.aacircle(screen, int(left), int(top), int(radius), Color.GRAY)
        

    # Draw numbers
    for i in range(9):
        x_offset = 25 if i == 0 else 23
        left = GRID_MARGIN + i*SQUARE_SIZE + x_offset

        top = 2*GRID_MARGIN+ROWS*SQUARE_SIZE + 7
        radius = SQUARE_SIZE/2.25

        font = pg.font.Font(pg.font.match_font("malgungothicsemilight"), 35)
        text = font.render(str(i+1), True, Color.BLACK)

                
        screen.blit(text, (left, top))


def draw_sidebar(screen) -> None:
    left = GRID_MARGIN*2+SQUARE_SIZE*COLS+SQUARE_SIZE/2
    top = GRID_MARGIN - 2

    # Title
    font_large = pg.font.Font(pg.font.match_font("malgungothicsemilight"), 50)
    font_small = pg.font.Font(pg.font.match_font("malgungothicsemilight"), 30)

    text = font_large.render("Sudoku", True, Color.BLACK)
    screen.blit(text, (left, top))

    # Mistakes
    top += SQUARE_SIZE*1.2

    timer = f"{time//60:0>2}:{time%60:0>2}"
    text = font_large.render(timer, True, Color.BLACK)
    screen.blit(text, (left, top))

    # Time
    top += SQUARE_SIZE*1.2
    text = font_small.render(f"Mistakes: {mistakes}", True, Color.BLACK)
    screen.blit(text, (left, top))


def check_gameover():
    if grid == grid_solved:
        tk.messagebox.showinfo("Sudoku", f"You won!\nTime: {time//60:0>2}:{time%60:0>2}\nMistakes: {mistakes}")
        exit()


pg.time.set_timer(pg.USEREVENT, 1000)

# Game loop
while True:
    clock.tick(60)
    screen.fill((255, 255, 255))

    # INPUT
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        
        if event.type == pg.USEREVENT:
            time += 1

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
                        if num != grid_solved[y][x] and num != 0:
                            mistakes += 1

            if event.key == pg.K_ESCAPE:
                selected_square = None
                selected_num = 0
                   
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                if get_square(): # Select square
                    x, y = get_square()
                    selected_num = grid[y][x]
                    selected_square = (x, y)

    # UPDATE
    check_gameover()

    # RENDER
    draw_grid(screen, grid)
    draw_number_selection(screen)
    draw_sidebar(screen)

    pg.display.update()

pg.quit()