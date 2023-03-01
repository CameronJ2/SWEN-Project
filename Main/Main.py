import pygame
from pygame import *
import sys
from Player import Player
import TerrainMap

clock = pygame.time.Clock() # set up the clock

#from pygame.locals import * # import pygame modules
pygame.init() # initiate pygame

pygame.display.set_caption('Summit Sprint') # set the window name

WINDOW_SIZE = (800,600) # set up window size

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate screen

display = pygame.Surface((600, 400))

#P1_moving_right = False
#P1_moving_left = False
#player1_y_momentum = 0
P1_gravity = 0

#P2_moving_right = False
#P2_moving_left = False
#player2_y_momentum = 0
P2_gravity = 0

#player1_image = pygame.image.load('Main\Assets\Pink_Monster.png').convert()
#player1_image.set_colorkey((255, 255, 255))
#player2_image = pygame.image.load('Main\Assets\Pink_Monster.png').convert()
#player2_image.set_colorkey((255, 255, 255))

player1 = Player('Main\Assets\Pink_Monster.png', K_UP, K_LEFT, K_RIGHT)
player2 = Player('Main\Assets\Pink_Monster.png', K_w, K_a, K_d)

grass_image = pygame.image.load('Main\Assets\grass.png')
TILE_SIZE = grass_image.get_width()

dirt_image = pygame.image.load('Main\Assets\dirt.png')

game_map = TerrainMap.game_map

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def movePlayer(playerRect, movement, tiles, otherPlayerRect):
    collisionTypes = {'bottom': False}
    playerRect.x += movement[0]
    hit_list = collision_test(playerRect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            playerRect.right = tile.left
        elif movement[0] < 0:
            playerRect.left = tile.right
    
    playerRect.y += movement[1]
    hit_list = collision_test(playerRect, tiles)
    for tile in hit_list:
        if playerRect.center[1] < tile.center[1]:
            playerRect.bottom = tile.top
        elif movement[1] < 0:
            playerRect.top = tile.bottom
    
    #lower sensor definition: box a pixel below feet to check if player is standing on something
    #Note: uses player1 dimensions, so try to keep all playermodels the same dimensions or come back and change this later to be more general
    lowerSensor = pygame.Rect(playerRect.x, playerRect.bottom, player1.playerImage.get_width(), 1) 
    lowerSensorHitList = collision_test(lowerSensor, tiles)
    if len(lowerSensorHitList) > 0:
        collisionTypes['bottom'] = True

    #fix player collision and add it here!

    

    return collisionTypes


while True: # game loop
    display.fill((146,244,255))

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '2':
                display.blit(grass_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1
    TerrainMap.mapDisplay(display)

    player1_movement = [0, 0]
    if player1.movingRight:
        player1_movement[0] += 2
    if player1.movingLeft:
        player1_movement[0] -= 2
    player1_movement[1] += player1.yMomentum
    player1.yMomentum += 0.2
    if player1.yMomentum > 5:
        player1.yMomentum = 5

    player2_movement = [0, 0]
    if player2.movingRight:
        player2_movement[0] += 2
    if player2.movingLeft:
        player2_movement[0] -= 2
    player2_movement[1] += player2.yMomentum
    player2.yMomentum += 0.2
    if player2.yMomentum > 5:
        player2.yMomentum = 5

    # removed player1_rect variable, pointer to player1.playerRect is passed in and updated, redundant variable.
    P1_collisions = movePlayer(player1.playerRect, player1_movement, tile_rects, player2.playerRect) 
    P2_collisions = movePlayer(player2.playerRect, player2_movement, tile_rects, player1.playerRect)
    
    print("collisions")
    print(P1_collisions)

    if P1_collisions['bottom']:
        player1.yMomentum = 0
        P1_gravity = 0
    else:
        P1_gravity += 1

    '''if P1_collisions['top']:
        player1.yMomentum = 1
    else:
        P1_gravity += 1'''



    if P2_collisions['bottom']:
        player2.yMomentum = 0
        P2_gravity = 0
    else:
        P2_gravity += 1

    '''if P2_collisions['top']:
        player2.yMomentum = 1
        P2_gravity += 0
    else:
        P2_gravity += 1'''

    display.blit(player1.playerImage, (player1.playerRect.x, player1.playerRect.y))
    display.blit(player2.playerImage, (player2.playerRect.x, player2.playerRect.y))
    

    for event in pygame.event.get(): # event loop
        if event.type == QUIT: # check for window quit
            pygame.quit() # stop pygame
            sys.exit() # stop script

        if event.type == KEYDOWN or event.type == KEYUP:
            player1.movementEvents(P1_collisions, event)
            player2.movementEvents(P2_collisions, event)
        '''if event.type == KEYDOWN:
            player1.movementEvents(player1, P1_collisions, event.key)
            player2.movementEvents(player2, P2_collisions, event.key)

            if event.key == K_RIGHT:
                player1.movingRight = True
            if event.key == K_LEFT:
                player1.movingLeft = True
            if event.key == K_UP:
                #if P1_gravity < 20:
                print("jump input")
                if P1_collisions['bottom']:
                    player1.yMomentum = -6
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                player1.movingRight = False
            if event.key == K_LEFT:
                player1.movingLeft = False


        if event.type == KEYDOWN:
            if event.key == K_d:
                player2.movingRight = True
            if event.key == K_a:
                player2.movingLeft = True
            if event.key == K_w:
                if P2_gravity < 20:
                    player2.yMomentum = -6
        if event.type == KEYUP:
            if event.key == K_d:
                player2.movingRight = False
            if event.key == K_a:
                player2.movingLeft = False'''
    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update() # update display
    clock.tick(60) # maintain 60 fps