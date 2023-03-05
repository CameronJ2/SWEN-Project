import pygame as pg
from player import Player

pg.init()

#sets screen resolution
screen_width = 960
screen_height = 640

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Summit Sprint')

#define game variables REMEMBER TO UPSCALE TILES IN FOLDER BY FOR 32x32 TO 64x64 2!!!
tile_size= 32

# create an instance of the Player class
player = Player(x=screen_width//2, y=screen_height//2, width=32, height=32)


#background image
BG3 = pg.image.load('Refactored\Free\BG_3\BG_3.png').convert_alpha()
BG2 = pg.image.load('Refactored\Free\BG_2\BG_2.png').convert_alpha()
BG1 = pg.image.load('Refactored\Free\BG_1\BG_1.png').convert_alpha()

#resizes BG
Bimg3 = pg.transform.scale(BG3, (1929 * 4, 400 * 4))
Bimg2 = pg.transform.scale(BG2, (1929 * 4, 400 * 4))
Bimg1 = pg.transform.scale(BG1, (1929 * 4, 400 * 4))

clock = pg.time.Clock()

run = True
while run:

    clock.tick(60) # Delay to cap the framerate at 60 fps

    #loads images to screen
    screen.blit(Bimg3, (-3000,-900))
    screen.blit(Bimg2, (-3000,-900))
    screen.blit(Bimg1, (-3000,-900))

    # move and draw the player
    player.move()
    player.draw(screen)

    #event handler to close game
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    
    pg.display.update()

pg.quit()