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

# Load tiles from tile_folder directory
def load_tiles(tile_folder):
    tile_images = []
    for i in range(1, 62):
        tile_path = os.path.join(tile_folder, f'Tile_{i:02d}.png')
        tile_image = pg.image.load(tile_path).convert_alpha()
        tile_images.append(tile_image)
    return tile_images

# Load level from a file
def load_level(level_path, cols, rows):
    level_data = [[0 for x in range(cols)] for y in range(rows)]
    tile_rects = []
    lavaRects = []
    with open(level_path, 'r') as f:
        for row, line in enumerate(f):
            tile_indices = line.strip().split(',')
            for col, tile_index in enumerate(tile_indices):
                tile_x = col * tile_size
                tile_y = row * tile_size
                if (int(tile_index) == 60):
                    lavaRect = pg.Rect(tile_x, tile_y, tile_size, tile_size)
                    lavaRects.append(lavaRect)
                elif int(tile_index) != 0:
                    tile_rect = pg.Rect(tile_x, tile_y, tile_size, tile_size)
                    tile_rects.append(tile_rect)
                level_data[row][col] = int(tile_index)
    return level_data, tile_rects, lavaRects

def WinZoneLoader(state):
    if state == 1:
        winZone = pg.Rect(425, -2450, 200, 20)
        return winZone
