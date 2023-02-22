import pygame as pg
import os

pg.init()

# Sets screen resolution
screen_width = 640
screen_height = 640

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Level Editor')

# Define game variables 
tile_size = 32
rows = 20
cols = 20
tile_folder = 'Tiles/1_Tiles'

# Create an empty level with no tiles
level = [[0 for x in range(rows)] for y in range(rows)]

# Load tiles from tile_folder directory
tile_images = []
for i in range(1, 61):
    tile_path = os.path.join(tile_folder, f'Tile_{i:02d}.png')
    tile_image = pg.image.load(tile_path).convert_alpha()
    tile_images.append(tile_image)

# Set up level editor display
def draw_grid():
    for row in range(rows):
        for col in range(cols):
            tile_x = col * tile_size
            tile_y = row * tile_size
            tile_index = level[row][col]
            if tile_index > 0 and tile_index < len(tile_images):
                tile_image = tile_images[tile_index]
                screen.blit(tile_image, (tile_x, tile_y))


# Handle user input for tile selection and placement
last_key = None

def handle_input():
    global last_key
    mouse_x, mouse_y = pg.mouse.get_pos()
    row = mouse_y // tile_size
    col = mouse_x // tile_size

    # Left mouse button selects tile
    if pg.mouse.get_pressed()[0] and not last_key:
        level[row][col] += 1
        if level[row][col] >= len(tile_images):
            level[row][col] = 0
        last_key = True

    # Right mouse button deletes tile
    elif pg.mouse.get_pressed()[2] and not last_key:
        level[row][col] = 0
        last_key = True

    # Clear last_key when mouse button is released
    elif not pg.mouse.get_pressed()[0] and not pg.mouse.get_pressed()[2]:
        last_key = False


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

        handle_input()
        draw_grid()

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

        pg.display.update()

    pg.quit()

if __name__ == '__main__':
    main()

