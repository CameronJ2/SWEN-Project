import pygame as pg
import os

pg.init()

# Sets screen resolution
screen_width = 960
screen_height = 640

screen = pg.display.set_mode((screen_width, screen_height))

# Define game variables 
tile_size = 32
rows = 100
cols = 30
tile_folder = 'Refactored/level_editor/Tiles/1_Tiles'

# Create an empty level with no tiles
level = [[0 for x in range(cols)] for y in range(rows)]

# Load tiles from tile_folder directory
tile_images = []
for i in range(1, 61):
    tile_path = os.path.join(tile_folder, f'Tile_{i:02d}.png')
    tile_image = pg.image.load(tile_path).convert_alpha()
    tile_images.append(tile_image)

# Load level from a file
def load_level():
    with open('Refactored\level_editor\level.txt', 'r') as f:
        for row, line in enumerate(f):
            tile_indices = line.strip().split(',')
            for col, tile_index in enumerate(tile_indices):
                level[row][col] = int(tile_index)