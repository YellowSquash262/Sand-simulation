import pygame
import sys

# Modify these
width = 250
height = 250

cell_size = 3
window_width = width * cell_size
window_height = height * cell_size

# Use lists; for even better speed, use numpy (see note below)
grid = [[0]*width for _ in range(height)]
new_grid = [[0]*width for _ in range(height)]  # For double buffering

def set_cell(x, y, value):
    if 0 <= x < width and 0 <= y < height:
        grid[y][x] = value

def draw_grid(screen):
    """Draw the grid on the Pygame screen."""
    surf = pygame.Surface((window_width, window_height))
    arr = pygame.PixelArray(surf)
    for y in range(height):
        for x in range(width):
            color = 0xFFFFFF if grid[y][x] else 0x000000
            px = x * cell_size
            py = y * cell_size
            for i in range(cell_size):
                for j in range(cell_size):
                    arr[px+i, py+j] = color
    del arr
    screen.blit(surf, (0,0))

def update():
    # Swap grid references instead of deep copy
    global grid, new_grid
    for y in range(height):
        for x in range(width):
            new_grid[y][x] = grid[y][x]

    for y in range(height-2, -1, -1):  # Process from bottom up
        for x in range(width):
            if grid[y][x] == 1:
                # Fall straight down
                if grid[y+1][x] == 0:
                    new_grid[y][x] = 0
                    new_grid[y+1][x] = 1
                else:
                    # Check diagonals
                    moved = False
                    if x > 0 and grid[y+1][x-1] == 0:
                        new_grid[y][x] = 0
                        new_grid[y+1][x-1] = 1
                        moved = True
                    elif x < width-1 and grid[y+1][x+1] == 0:
                        new_grid[y][x] = 0
                        new_grid[y+1][x+1] = 1
                        moved = True
                    # If can't move, try to "fall through" column below
                    if not moved:
                        for check_y in range(y+2, height):
                            if grid[check_y][x] == 0:
                                new_grid[y][x] = 0
                                new_grid[check_y][x] = 1
                                break
    # Swap grids for next frame
    grid, new_grid = new_grid, grid

def mouse_drag():
    pressed = pygame.mouse.get_pressed()
    if pressed[0]:
        mx, my = pygame.mouse.get_pos()
        gx, gy = mx // cell_size, my // cell_size
        if 0 <= gx < width and 0 <= gy < height:
            grid[gy][gx] = 1

pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Cellular Automaton Grid")

set_cell(1, 1, 1)
set_cell(2, 3, 1)
set_cell(25, 10, 1)

clock = pygame.time.Clock()

running = True
while running:
    screen.fill((0, 0, 0))
    draw_grid(screen)
    pygame.display.flip()
    # clock.tick(2000)  # Uncomment to limit FPS

    mouse_drag()
    update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()
