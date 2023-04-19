import pygame as pg
import time
from pygame import *
import sys
from Player import Player
from Level import load_level, load_tiles

clock = pg.time.Clock() # set up the clock
pg.init() # initiate pygame
pg.display.set_caption('Summit Sprint') # set the window name
WINDOW_SIZE = (960,640) # set up window size
screen = pg.display.set_mode(WINDOW_SIZE,0,32) # initiate screen
display = pg.Surface((960, 640))
player1 = Player('Main\img\Owl_Mon', K_UP, K_LEFT, K_DOWN, K_RIGHT, 150, 500)
player2 = Player('Main\img\Pink_Mon', K_w, K_a, K_s, K_d, 100, 500)
rows = 100
cols = 30
screen_width = 960
screen_height = 640
textFont = pg.font.SysFont("Arial", 30)
#rectangle at the bottom of the screen for killing the player
killZone = pg.Rect(0, 630, 960, 10)
winZone = pg.Rect(425, -2450, 200, 20)

P1Score = 'P1 Score: %d' % player1.score
p2Score = 'P2 Score: %d' % player2.score

def StringToScreen(text, font, color, x, y):
    image = font.render(text, True, color)
    screen.blit(image, (x,y))

def BasicCollisionTest(playerRect, tiles, otherPlayerRect):
    hit_list = []
    for tile in tiles:
        if playerRect.colliderect(tile):
            hit_list.append(tile)
    if playerRect.colliderect(otherPlayerRect):
        hit_list.append(otherPlayerRect)
    
    return hit_list


""" 
added this method for the pushing mechanic. Had to jump through hoops a bit because collisions were already being handled in MovePlayer, so I couldn't use the colliderect function, so instead, I had to basically give a range of rect.x and rect.y values that would require the players to be touching.
 """
def PlayerCollisionTest(playerRect, otherPlayerRect):
    playerCollisionTypes = {'bottom': False, 'left': False, 'right': False, 'top': False}
    if playerRect.bottom == otherPlayerRect.top and (playerRect.x -36 <= otherPlayerRect.x <= playerRect.x + 36):
        playerCollisionTypes['bottom'] = True
    elif playerRect.top == otherPlayerRect.bottom and (playerRect.x -36 <= otherPlayerRect.x <= playerRect.x + 36):
        playerCollisionTypes['top'] = True
    if (otherPlayerRect.left <= playerRect.right <= otherPlayerRect.left + 36) and (playerRect.y -55 <= otherPlayerRect.y <= playerRect.y + 55):
        playerCollisionTypes['right'] = True
    if (otherPlayerRect.right - 36 <= playerRect.left <= otherPlayerRect.right) and (playerRect.y -55 <= otherPlayerRect.y <= playerRect.y + 55):
        playerCollisionTypes['left'] = True
    return playerCollisionTypes


#logic for what should happen when a player wins
def WinFunction(winner, loser):
    if winner == player1:
        print("Player 1 Wins!")
    else:
        print("Player 2 Wins!")
    winner.score += 1
    winner.hasWon = True
    loser.hasWon = False

def MovePlayer(P1, movement, tiles, P2):
    collisionTypes = {'bottom': False, 'left': False, 'right': False}
    P1.playerRect.x += movement[0]
    
    # check for collisions with the left and right side of the screen
    if P1.playerRect.left < 0:
        P1.playerRect.left = 0
    elif P1.playerRect.right > screen_width:
        P1.playerRect.right = screen_width

    # win conditions:
    if P2.playerRect.top >= killZone.bottom or P1.playerRect.colliderect(winZone):
        WinFunction(P1, P2)    
    if P1.playerRect.top >= killZone.bottom or P2.playerRect.colliderect(winZone):
        WinFunction(P2, P1)
        

    hit_list = BasicCollisionTest(P1.playerRect, tiles, P2.playerRect)
    for rect in hit_list:
        if movement[0] > 0:
            P1.playerRect.right = rect.left
            #collisionTypes['right'] = True
        elif movement[0] < 0:
            #collisionTypes['left'] = True
            P1.playerRect.left = rect.right
    
    P1.playerRect.y += movement[1]
    hit_list = BasicCollisionTest(P1.playerRect, tiles, P2.playerRect)
    for rect in hit_list:
        if movement[1] > 0:
            P1.playerRect.bottom = rect.top
        elif movement[1] < 0: 
            P1.playerRect.top = rect.bottom
            
    #lower sensor definition: box a pixel below feet to check if player is standing on something
    #Note: uses player1 dimensions, so try to keep all playermodels the same dimensions or come back and change this later to be more general
    lowerSensor = pg.Rect(P1.playerRect.x, P1.playerRect.bottom, 32, 1) 
    lowerSensorHitList = BasicCollisionTest(lowerSensor, tiles, P2.playerRect)
    if len(lowerSensorHitList) > 0:
        collisionTypes['bottom'] = True

    return collisionTypes

#background image
BG3 = pg.image.load('Main/Free/BG_3/BG_3.png').convert_alpha()
BG2 = pg.image.load('Main/Free/BG_2/BG_2.png').convert_alpha()
BG1 = pg.image.load('Main/Free/BG_1/BG_1.png').convert_alpha()

#resizes BG
Bimg3 = pg.transform.scale(BG3, (1929 * 4, 400 * 4))
Bimg2 = pg.transform.scale(BG2, (1929 * 4, 400 * 4))
Bimg1 = pg.transform.scale(BG1, (1929 * 4, 400 * 4))

# load the tiles from the tile folder
tile_images = load_tiles('Main/level_editor/Tiles/1_Tiles')

# create an empty level
level = []
tile_rects = []

# load the level data from file
level, tile_rects = load_level('Main/level.txt', cols, rows)

# replace the tile indices with tile images in the level data
for row in range(len(level)):
    for col in range(len(level[row])):
        tile_index = level[row][col]
        if tile_index != 0:
            level[row][col] = tile_images[tile_index]

camera_y = 2560
old_camera_y = 2560
target_camera_y = 2560
    
while True: # game loop
    tile_rects = []  # Clear tile_rects

    #loads images to screen
    screen.blit(Bimg3, (-3000,0))
    screen.blit(Bimg2, (-3000,0))
    screen.blit(Bimg1, (-3000,0))
    StringToScreen(P1Score, textFont, (0,0,0), 220, 150)
    
    ##### Delete this or comment this out to get rid of the player rectangles
    # pg.draw.rect(screen, (0, 0, 255), player1.playerRect)
    # pg.draw.rect(screen, (0, 0, 255), player2.playerRect)
    pg.draw.rect(screen, (0, 0, 255), killZone)
    pg.draw.rect(screen, (0,0,255), winZone)
     
    if player1.playerRect.top < 50 or player2.playerRect.top < 50:
        if camera_y > 100:  # only move camera if it hasn't reached the top of the level
            target_camera_y -= 250
            winZone.update

    # move the camera towards the target position
    # Cameron: Made this a high value to stop the weird collision issues on camera move. The code instantly tries to update the playerrect on the screen, but the screen was slowly moving up, creating the weird collision issues
    camera_y += (target_camera_y - camera_y) * 1  # adjust the 0.1 to control the speed of the camera movement
    
    # update player positions based on camera movement
    player1.playerRect.y -= (camera_y - old_camera_y)
    player2.playerRect.y -= (camera_y - old_camera_y)
    winZone.y -= (camera_y - old_camera_y)
    old_camera_y = camera_y

    # draw the level tiles and update tile_rects
    for row in range(len(level)):
        for col in range(len(level[row])):
            tile = level[row][col]
            if tile != 0:
                tile_rects.append(pg.Rect(col * 32, row * 32 - camera_y, 32, 32))
                screen.blit(tile, (col * 32, row * 32 - camera_y))
                                
    player1_movement = player1.getMovement()
    player2_movement = player2.getMovement()

    # removed player1_rect variable, pointer to player1.playerRect is passed in and updated, redundant variable.
    P1Collisions = MovePlayer(player1, player1_movement, tile_rects, player2) 
    P1PlayerCollision = PlayerCollisionTest(player1.playerRect, player2.playerRect)
    P2Collisions = MovePlayer(player2, player2_movement, tile_rects, player1)
    P2PlayerCollision = PlayerCollisionTest(player2.playerRect, player1.playerRect)
    
    if P1Collisions['bottom']:
        player1.yMomentum = 0

    if P2Collisions['bottom']:
        player2.yMomentum = 0

    #draw the player
    player1.draw(screen)
    player2.draw(screen)    
    
    for event in pg.event.get(): # event loop
        if event.type == QUIT: # check for window quit
            pg.quit() # stop pygame
            sys.exit() # stop script

        if event.type == KEYDOWN or event.type == KEYUP:
            player1.movementEvents(P1Collisions, event, P1PlayerCollision, player2)
            player2.movementEvents(P2Collisions, event, P2PlayerCollision, player1)

    pg.display.update() # update display  
    clock.tick(60) # maintain 60 fps
