import pygame as pg
from player import Player as gPlayer
from pygame.locals import *
from levelLoader import load_level, load_tiles
from lava import Lava

clock = pg.time.Clock()

pg.init()

#sets screen resolution
screen_width = 960
screen_height = 640

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Summit Sprint')

#define game variables REMEMBER TO UPSCALE TILES IN FOLDER BY FOR 32x32 TO 64x64 2!!!
tile_size= 32
rows = 100
cols = 30
gameOver = 0
Width = 32
Height = 32
lavaGroup = pg.sprite.Group()

# create an instance of the Player class
player1 = gPlayer('Refactored\img\Owl_Mon', K_UP, K_LEFT, K_RIGHT, screen_width//2, screen_height//2, Width, Height)
player2 = gPlayer('Refactored\img\Pink_Mon', K_w, K_a, K_d, screen_width//2, screen_height//2, Width, Height)

lavaGroup = pg.sprite.Group()

#background image
BG3 = pg.image.load('Refactored/Free/BG_3/BG_3.png').convert_alpha()
BG2 = pg.image.load('Refactored/Free/BG_2/BG_2.png').convert_alpha()
BG1 = pg.image.load('Refactored/Free/BG_1/BG_1.png').convert_alpha()

#resizes BG
Bimg3 = pg.transform.scale(BG3, (1929 * 4, 400 * 4))
Bimg2 = pg.transform.scale(BG2, (1929 * 4, 400 * 4))
Bimg1 = pg.transform.scale(BG1, (1929 * 4, 400 * 4))

# load the tiles from the tile folder
tile_images = load_tiles('Refactored/level_editor/Tiles/1_Tiles')
tile_rects = []

# create an empty level
level = []

# load the level data from file
level = load_level('Refactored/level_editor/level.txt', cols, rows)

# replace the tile indices with tile images in the level data
for row in range(len(level)):
    for col in range(len(level[row])):
        tile_index = level[row][col]
        if tile_index != 0:
            level[row][col] = tile_images[tile_index]
        if tile_index == 61:
                lava = Lava(col * tile_size, row * tile_size + (tile_size // 2))
                lavaGroup.add(lava)
run = True
while run:

    clock.tick(60) # Delay to cap the framerate at 60 fps

    #loads images to screen
    screen.blit(Bimg3, (-3000,0))
    screen.blit(Bimg2, (-3000,0))
    screen.blit(Bimg1, (-3000,0))

    # draw the level tiles
    for row in range(len(level)):
        for col in range(len(level[row])):
            tile = level[row][col]
            if tile != 0:
                screen.blit(tile, (col * tile_size, row * tile_size))

    # move and draw the player
    player1.update(gameOver)
    player1.draw(screen)
    player2.update(gameOver)
    player2.draw(screen)
    
    if gameOver == 0:
        lavaGroup.update()
        
        gameOver = gPlayer.update(gameOver)


    #event handler to close game
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    
    pg.display.update()

pg.quit()
