import pygame as pg
import os

pg.init()

# Sets screen resolution
screen_width = 960
screen_height = 640

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Level Editor')

# Define game variables 
tile_size = 32
rows = 100
cols = 30
tile_folder = 'Tiles/1_Tiles'

# Create an empty level with no tiles
level = [[0 for x in range(cols)] for y in range(rows)]

# Load tiles from tile_folder directory
tile_images = []
for i in range(1, 61):
    tile_path = os.path.join(tile_folder, f'Tile_{i:02d}.png')
    tile_image = pg.image.load(tile_path).convert_alpha()
    tile_images.append(tile_image)

# Set up level editor display
offset_y = 0  # Vertical offset of the screen

def draw_grid():
    global offset_y
    # Maximum offset based on level size
    max_offset_y = (rows * tile_size) - screen_height 

    # Check if offset_y exceeds the maximum or minimum values, and adjust if necessary
    if offset_y < 0:
        offset_y = 0
    elif offset_y > max_offset_y:
        offset_y = max_offset_y

    # Draw tiles
    for row in range(rows):
        for col in range(cols):
            tile_x = col * tile_size
            tile_y = (row * tile_size) - offset_y
            
            #Edits tiles depending where I scrolled in the editor. Without this it can't edit properly.
            if row < rows and col < cols:
                tile_index = level[row][col]
                if tile_index > 0 and tile_index < len(tile_images):
                    tile_image = tile_images[tile_index]
                    screen.blit(tile_image, (tile_x, tile_y))
                else:
                    blank_surface = pg.Surface((tile_size, tile_size))
                    blank_surface.fill((255, 255, 255))
                    screen.blit(blank_surface, (tile_x, tile_y))

            # Draw the tile again to fill in any empty space at the bottom of the screen
            tile_index = level[row][col]
            if tile_index > 0 and tile_index < len(tile_images):
                tile_image = tile_images[tile_index]
                screen.blit(tile_image, (tile_x, tile_y))
            else:
                blank_surface = pg.Surface((tile_size, tile_size))
                blank_surface.fill((255, 255, 255))
                screen.blit(blank_surface, (tile_x, tile_y))

    #Draws the grid lines in the level editor
    for i in range(rows + 1):
        pg.draw.line(screen, (0, 0, 0), (0, i * tile_size - offset_y), (cols * tile_size, i * tile_size - offset_y))
    for i in range(cols + 1):
        pg.draw.line(screen, (0, 0, 0), (i * tile_size, -offset_y), (i * tile_size, (rows * tile_size) - offset_y))

    # Handle scrolling
    keys = pg.key.get_pressed()
    if keys[pg.K_UP]:
        offset_y -= tile_size
    elif keys[pg.K_DOWN]:
        offset_y += tile_size

# Handle user input for tile selection and placement
last_left_key = False
last_right_key = False

def handle_input():
    global last_left_key, last_right_key
    mouse_x, mouse_y = pg.mouse.get_pos()
    row = (mouse_y + offset_y) // tile_size
    col = mouse_x // tile_size


    # Left mouse button selects tile
    if pg.mouse.get_pressed()[0] and not last_left_key:
        level[row][col] += 1
        if level[row][col] >= len(tile_images):
            level[row][col] = 0
        last_left_key = True

    # Right mouse button deletes tile
    elif pg.mouse.get_pressed()[2] and not last_right_key:
        level[row][col] = 0
        print(f"Deleted tile at row {row}, column {col}")
        last_right_key = True

    # Reset last_left_key and last_right_key when both mouse buttons are released
    if not pg.mouse.get_pressed()[0] and not pg.mouse.get_pressed()[2]:
        last_left_key = False
        last_right_key = False

# Save level to a file
def save_level():
    with open('level.txt', 'w') as f:
        for row in level:
            f.write(','.join(str(tile_index) for tile_index in row))
            f.write('\n')

# Load level from a file
def load_level():
    with open('level.txt', 'r') as f:
        for row, line in enumerate(f):
            tile_indices = line.strip().split(',')
            for col, tile_index in enumerate(tile_indices):
                level[row][col] = int(tile_index)

# Run the level editor loop
def main():
    clock = pg.time.Clock()
    run = True
    while run:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                elif event.key == pg.K_s:
                    save_level()
                elif event.key == pg.K_l:
                    load_level()

        handle_input()
        draw_grid()

        pg.display.update()

    pg.quit()

if __name__ == '__main__':
    main()
