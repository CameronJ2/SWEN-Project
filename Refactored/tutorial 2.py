import pygame, sys # import pygame and sys

clock = pygame.time.Clock() # set up the clock

from pygame.locals import * # import pygame modules
pygame.init() # initiate pygame

pygame.display.set_caption('My Pygame') # set the window name

WINDOW_SIZE = (800,600) # set up window size

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate screen

display = pygame.Surface((600, 400))

P2_moving_right = False
P2_moving_left = False
player2_y_momentum = 0
P2_gravity = 0



def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def playerCollisionTest(player1_rect, player2_rect):
    player_collision = False
    if player1_rect.colliderect(player2_rect):
        player_collision = True
        print('collision detected')
    return player_collision


def player1Move(player1_rect, movement, tiles, player2_rect):
    P1_collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    player1_rect.x += movement[0]
    hit_list = collision_test(player1_rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            player1_rect.right = tile.left
            P1_collision_types['right'] = True
        elif movement[0] < 0:
            player1_rect.left = tile.right
            P1_collision_types['left'] = True
    player1_rect.y += movement[1]
    hit_list = collision_test(player1_rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            player1_rect.bottom = tile.top
            P1_collision_types['bottom'] = True
        elif movement[1] < 0:
            player1_rect.top = tile.bottom
            P1_collision_types['top'] = True
    
    player_collision = playerCollisionTest(player1_rect, player2_rect)
    if player_collision == True:
        if movement[0] > 0:
            player1_rect.right = player2_rect.left
            P1_collision_types['right'] = True
        elif movement[0] < 0:
            player1_rect.left = player2_rect.right
            P1_collision_types['left'] = True

        if movement[1] > 0:
            player1_rect.bottom = player2_rect.top
            P1_collision_types['bottom'] = True
        elif movement[1] < 0:
            player1_rect.top = player2_rect.bottom
            P1_collision_types['top'] = True

    return player1_rect, P1_collision_types

def player2Move(player2_rect, movement, tiles, player1_rect):
    P2_collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    player2_rect.x += movement[0]
    hit_list = collision_test(player2_rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            player2_rect.right = tile.left
            P2_collision_types['right'] = True
        elif movement[0] < 0:
            player2_rect.left = tile.right
            P2_collision_types['left'] = True
    player2_rect.y += movement[1]
    hit_list = collision_test(player2_rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            player2_rect.bottom = tile.top
            P2_collision_types['bottom'] = True
        elif movement[1] < 0:
            player2_rect.top = tile.bottom
            P2_collision_types['top'] = True

    player_collision = playerCollisionTest(player1_rect, player2_rect)
    if player_collision == True:
        if movement[0] > 0:
            player2_rect.right = player1_rect.left
            P2_collision_types['right'] = True
        elif movement[0] < 0:
            player2_rect.left = player1_rect.right
            P2_collision_types['left'] = True

        if movement[1] > 0:
            player2_rect.bottom = player1_rect.top
            P2_collision_types['bottom'] = True
        elif movement[1] < 0:
            player2_rect.top = player1_rect.bottom
            P2_collision_types['top'] = True
    return player2_rect, P2_collision_types

player1_rect = pygame.Rect(50, 50, player1_image.get_width(), player1_image.get_height())
player2_rect = pygame.Rect(200, 50, player2_image.get_width(), player2_image.get_height())
test_rect = pygame.Rect(100,100,100,50)

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

    player1_movement = [0, 0]
    if P1_moving_right:
        player1_movement[0] += 2
    if P1_moving_left:
        player1_movement[0] -= 2
    player1_movement[1] += player1_y_momentum
    player1_y_momentum += 0.2
    if player1_y_momentum > 5:
        player1_y_momentum = 5

    player2_movement = [0, 0]
    if P2_moving_right:
        player2_movement[0] += 2
    if P2_moving_left:
        player2_movement[0] -= 2
    player2_movement[1] += player2_y_momentum
    player2_y_momentum += 0.2
    if player2_y_momentum > 5:
        player2_y_momentum = 5

    player1_rect, P1_collisions = player1Move(player1_rect, player1_movement, tile_rects, player2_rect)
    player2_rect, P2_collisions = player2Move(player2_rect, player2_movement, tile_rects, player1_rect)

    if P1_collisions['bottom']:
        player1_y_momentum = 0
        P1_gravity = 0
    else:
        P1_gravity += 1

    if P1_collisions['top']:
        player1_y_momentum = 1
        P1_gravity += 0
    else:
        P1_gravity += 1



    if P2_collisions['bottom']:
        player2_y_momentum = 0
        P2_gravity = 0
    else:
        P2_gravity += 1

    if P2_collisions['top']:
        player2_y_momentum = 1
        P2_gravity += 0
    else:
        P2_gravity += 1

    display.blit(player1_image, (player1_rect.x, player1_rect.y))
    display.blit(player2_image, (player2_rect.x, player2_rect.y))
    

    for event in pygame.event.get(): # event loop
        if event.type == QUIT: # check for window quit
            pygame.quit() # stop pygame
            sys.exit() # stop script
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                P1_moving_right = True
            if event.key == K_LEFT:
                P1_moving_left = True
            if event.key == K_UP:
                if P1_gravity < 20:
                    player1_y_momentum = -6
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                P1_moving_right = False
            if event.key == K_LEFT:
                P1_moving_left = False


        if event.type == KEYDOWN:
            if event.key == K_d:
                P2_moving_right = True
            if event.key == K_a:
                P2_moving_left = True
            if event.key == K_w:
                if P2_gravity < 20:
                    player2_y_momentum = -6
        if event.type == KEYUP:
            if event.key == K_d:
                P2_moving_right = False
            if event.key == K_a:
                P2_moving_left = False
    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update() # update display
    clock.tick(60) # maintain 60 fps