import pygame
import sys
import copy

# Modify these
width = 250 # columns
height = 250 # rows

# Set cell and window size
cell_size = 3 # Size of each square cell in pixels
window_width = width * cell_size
window_height = height * cell_size

#
drop_size = 20

closest_zero_y = None

# Initialize the grid to all 0s
grid = [[0 for _ in range(width)] for _ in range(height)]

def set_cell(x, y, value):
    """Set the value of a specific cell (x: column, y: row)."""
    if 0 <= x < width and 0 <= y < height:
        grid[y][x] = value

def draw_grid(screen):
    """Draw the grid on the Pygame screen."""
    for y in range(height):
        for x in range(width):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            color = (255, 255, 255) if grid[y][x] == 1 else (0, 0, 0)
            pygame.draw.rect(screen, color, rect)
            # Optional: draw cell borders
            # pygame.draw.rect(screen, (40, 40, 40), rect, 1)

def update():
    prev_grid = [row[:] for row in grid]
    for y in range(height - 2, -1, -1):  # from second-to-last row up to 0, going upwards
        for x in range(width):
            if prev_grid[y][x] == 1 and prev_grid[y+1][x] == 0:
                grid[y][x] = 0
                grid[y+1][x] = 1
            else:
                if prev_grid[y][x] == 1:
                    closest_zero_y = None
                    for check_y in range(y+1, height):
                        if prev_grid[check_y][x] == 0:
                            closest_zero_y = check_y
                            break
                    if closest_zero_y is not None:
                        break
                    elif x > 0 and prev_grid[y+1][x-1] == 0:
                        grid[y][x] = 0
                        grid[y+1][x-1] = 1
                    elif x < width - 1 and prev_grid[y+1][x+1] == 0:
                        grid[y][x] = 0
                        grid[y+1][x+1] = 1


def mouse_drag():
    pressed = pygame.mouse.get_pressed()
    if pressed[0]:  # Left mouse button is held
        x, y = pygame.mouse.get_pos()
        grid[int(y / cell_size)][int(x / cell_size)] = 1
        """for a in range(drop_size):
            for b in range(drop_size):
                print(a)
                if int((y + a - 0.5*drop_size) / cell_size) % 2 == 0 and int((x + b - 0.5*drop_size) / cell_size) % 2 ==0:

                    print("even")
                    grid[int((y + a - 0.5*drop_size) / cell_size)][int((x + b - 0.5*drop_size) / cell_size)] = 1"""

pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Cellular Automaton Grid")

# Example: modify some cells to be white
set_cell(1, 1, 1)
set_cell(2, 3, 1)
set_cell(25, 10, 1)

clock = pygame.time.Clock()

running = True
while running:
    screen.fill((0, 0, 0))
    draw_grid(screen)
    pygame.display.flip()

    clock.tick(40) # Slowed down for easier viewing

    update()
    mouse_drag()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()
