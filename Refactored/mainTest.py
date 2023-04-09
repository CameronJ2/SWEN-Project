import pygame as pg
from pygame import *
import sys
from playerTest import Player
from levelLoaderTest import load_level, load_tiles
from lava import Lava

clock = pg.time.Clock() # set up the clock
pg.init() # initiate pygame
pg.display.set_caption('Summit Sprint') # set the window name
WINDOW_SIZE = (960,640) # set up window size
screen = pg.display.set_mode(WINDOW_SIZE,0,32) # initiate screen
display = pg.Surface((960, 640))
player1 = Player('Refactored/img/Owl_Mon', K_UP, K_LEFT, K_RIGHT, 900, 500)
player2 = Player('Refactored/img/Pink_Mon', K_w, K_a, K_d, 300, 300)
rows = 100
cols = 30
screen_width = 960
screen_height = 640
gameOver = 0

def collision_test(playerRect, tiles, otherPlayerRect, lava):
    hit_list = []
    for tile in tiles:
        if playerRect.colliderect(tile):
            hit_list.append(tile)
    if playerRect.colliderect(otherPlayerRect):
        hit_list.append(otherPlayerRect)
    if playerRect.colliderect(lava):
        hit_list.append(lava)
    
    return hit_list


def movePlayer(playerRect, movement, tiles, otherPlayerRect, lava):
    collisionTypes = {'bottom': False}
    playerRect.x += movement[0]
    hit_list = collision_test(playerRect, tiles, otherPlayerRect, lava)
    for rect in hit_list:
        if movement[0] > 0:
            playerRect.right = rect.left
        elif movement[0] < 0:
            playerRect.left = rect.right
    
    playerRect.y += movement[1]
    hit_list = collision_test(playerRect, tiles, otherPlayerRect, lava)
    for rect in hit_list:
        if movement[1] > 0:
            playerRect.bottom = rect.top
        elif movement[1] < 0: 
            playerRect.top = rect.bottom
            
    #lower sensor definition: box a pixel below feet to check if player is standing on something
    #Note: uses player1 dimensions, so try to keep all playermodels the same dimensions or come back and change this later to be more general
    lowerSensor = pg.Rect(playerRect.x, playerRect.bottom, 32, 1) 
    lowerSensorHitList = collision_test(lowerSensor, tiles, otherPlayerRect)
    if len(lowerSensorHitList) > 0:
        collisionTypes['bottom'] = True

    return collisionTypes

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

# create an empty level
level = []
tile_rects = []

# load the level data from file
level, tile_rects = load_level('Refactored/level_editor/level.txt', cols, rows)



# replace the tile indices with tile images in the level data
for row in range(len(level)):
    for col in range(len(level[row])):
        tile_index = level[row][col]
        if tile_index != 0:
            level[row][col] = tile_images[tile_index]
        if tile_index == 61:
            level[row][col] = tile_images[Lava]


while True: # game loop
    #loads images to screen
    screen.blit(Bimg3, (-3000,0))
    screen.blit(Bimg2, (-3000,0))
    screen.blit(Bimg1, (-3000,0))
    
    ##### Delete this or comment this out to get rid of the player rectangles
    pg.draw.rect(screen, (0, 0, 255), player1.playerRect)
    pg.draw.rect(screen, (0, 0, 255), player2.playerRect)


    # draw the level tiles
    for row in range(len(level)):
        for col in range(len(level[row])):
            tile = level[row][col]
            if tile != 0:
                screen.blit(tile, (col * 32, row * 32))
                
    player1_movement = player1.getMovement()
    player2_movement = player2.getMovement()

    # removed player1_rect variable, pointer to player1.playerRect is passed in and updated, redundant variable.
    P1_collisions = movePlayer(player1.playerRect, player1_movement, tile_rects, player2.playerRect, Lava) 
    P2_collisions = movePlayer(player2.playerRect, player2_movement, tile_rects, player1.playerRect, Lava)
    
    if P1_collisions['bottom']:
        player1.yMomentum = 0

    if P2_collisions['bottom']:
        player2.yMomentum = 0

    #draw the player
    player1.draw(screen)
    player2.draw(screen)    
    
    for event in pg.event.get(): # event loop
        if event.type == QUIT: # check for window quit
            pg.quit() # stop pygame
            sys.exit() # stop script

        if event.type == KEYDOWN or event.type == KEYUP:
            player1.movementEvents(P1_collisions, event)
            player2.movementEvents(P2_collisions, event)

    pg.display.update() # update display
    clock.tick(60) # maintain 60 fps
