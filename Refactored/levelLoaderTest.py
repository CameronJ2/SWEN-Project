import pygame as pg
import os

pg.init()

# Sets screen resolution
screen_width = 960
screen_height = 640

screen = pg.display.set_mode((screen_width, screen_height))

# Define game variables 
tile_size = 32
tile_folder = 'Refactored/level_editor/Tiles/1_Tiles'
tile_kill = 'Refactored/level_editor/Tiles/5 kill_Tiles'

# Load tiles from tile_folder directory
def load_tiles(tile_folder):
    tile_images = []
    for i in range(1, 65):
        tile_path = os.path.join(tile_folder, f'Tile_{i:02d}.png')
        tile_image = pg.image.load(tile_path).convert_alpha()
        tile_images.append(tile_image)
    return tile_images

#load kill tiles
def load_kill (tile_kill):
    tile_Images = []
    for i in range(1, 3):
        tile_Path = os.path.join(tile_kill, f'Tile_{i:00d}.png')
        Tile_image = pg.image.load(tile_Path).convert_alpha()
        tile_Images.append(Tile_image)
    return tile_Images

# Load level from a file
def load_level(level_path, cols, rows):
    level_data = [[0 for x in range(cols)] for y in range(rows)]
    tile_rects = []
    with open(level_path, 'r') as f:
        for row, line in enumerate(f):
            tile_indices = line.strip().split(',')
            for col, tile_index in enumerate(tile_indices):
                tile_x = col * tile_size
                tile_y = row * tile_size
                if int(tile_index) != 0:
                    tile_rect = pg.Rect(tile_x, tile_y, tile_size, tile_size)
                    tile_rects.append(tile_rect)
                level_data[row][col] = int(tile_index)
    return level_data, tile_rects
