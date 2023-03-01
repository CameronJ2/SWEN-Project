import pygame
from pygame import *
import sys
from Player import Player
import TerrainMap

clock = pygame.time.Clock() # set up the clock
pygame.init() # initiate pygame
pygame.display.set_caption('Summit Sprint') # set the window name
WINDOW_SIZE = (800,600) # set up window size
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate screen
display = pygame.Surface((600, 400))
player1 = Player('Main\Assets\Pink_Monster.png', K_UP, K_LEFT, K_RIGHT)
player2 = Player('Main\Assets\Pink_Monster.png', K_w, K_a, K_d)
game_map = TerrainMap.game_map

def collision_test(playerRect, tiles, otherPlayerRect):
    hit_list = []
    for tile in tiles:
        if playerRect.colliderect(tile):
            hit_list.append(tile)
    if playerRect.colliderect(otherPlayerRect):
        hit_list.append(otherPlayerRect)
    
    return hit_list

def movePlayer(playerRect, movement, tiles, otherPlayerRect):
    collisionTypes = {'bottom': False}
    playerRect.x += movement[0]
    hit_list = collision_test(playerRect, tiles, otherPlayerRect)
    for rect in hit_list:
        if movement[0] > 0:
            playerRect.right = rect.left
        elif movement[0] < 0:
            playerRect.left = rect.right
    
    playerRect.y += movement[1]
    hit_list = collision_test(playerRect, tiles, otherPlayerRect)
    for rect in hit_list:
        if movement[1] > 0:
            playerRect.bottom = rect.top
        elif movement[1] < 0: 
            playerRect.top = rect.bottom
            
    #lower sensor definition: box a pixel below feet to check if player is standing on something
    #Note: uses player1 dimensions, so try to keep all playermodels the same dimensions or come back and change this later to be more general
    lowerSensor = pygame.Rect(playerRect.x, playerRect.bottom, player1.playerImage.get_width(), 1) 
    lowerSensorHitList = collision_test(lowerSensor, tiles, otherPlayerRect)
    if len(lowerSensorHitList) > 0:
        collisionTypes['bottom'] = True

    return collisionTypes

while True: # game loop
    display.fill((146,244,255))
    tile_rects = TerrainMap.mapDisplay(display)
    
    player1_movement = player1.getMovement()
    player2_movement = player2.getMovement()

    # removed player1_rect variable, pointer to player1.playerRect is passed in and updated, redundant variable.
    P1_collisions = movePlayer(player1.playerRect, player1_movement, tile_rects, player2.playerRect) 
    P2_collisions = movePlayer(player2.playerRect, player2_movement, tile_rects, player1.playerRect)
    
    if P1_collisions['bottom']:
        player1.yMomentum = 0

    if P2_collisions['bottom']:
        player2.yMomentum = 0

    display.blit(player1.playerImage, (player1.playerRect.x, player1.playerRect.y))
    display.blit(player2.playerImage, (player2.playerRect.x, player2.playerRect.y))
    
    for event in pygame.event.get(): # event loop
        if event.type == QUIT: # check for window quit
            pygame.quit() # stop pygame
            sys.exit() # stop script

        if event.type == KEYDOWN or event.type == KEYUP:
            player1.movementEvents(P1_collisions, event)
            player2.movementEvents(P2_collisions, event)

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update() # update display
    clock.tick(60) # maintain 60 fps