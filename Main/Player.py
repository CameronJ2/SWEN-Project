import pygame as pg
from pygame.locals import *
import sys
#from pygame.locals import * # import pygame modules

class Player:
    def __init__(self, spritePath, upKey, leftKey, downkey, rightKey, x, y): #relative path here refers to the path in your filesystem to the asset. For me and my repository, it's: Main\Assets\Pink_Monster.png
                                      #Keep in mind you don't have to type the FULL path. Relative path starts at your working folder instead of your drive.
                                      #for instance, the absolute (full) path for me is: H:\Projects\SWEN-Project\Main\Assets\Pink_Monster.png, but my 
                                      #working folder is SWEN-Project, so I can cut out everything before it.
        self.x = x
        self.y = y
        self.playerRect = pg.Rect(x, y, 36, 55)
        self.movingRight = False
        self.movingLeft = False
        self.yMomentum = 0
        self.playerRect.center
        self.upKey = upKey
        self.leftKey = leftKey
        self.downkey = downkey
        self.rightKey = rightKey
        
        # The 32 is the tile size and the 2 is the scale
        self.width = 32 * 2
        self.height = 32 * 2

        # Load sprite sheets
        self.idle_sheet = pg.image.load(spritePath + '/Idle_4.png').convert_alpha()
        self.running_sheet = pg.image.load(spritePath + '/Run_6.png').convert_alpha()
        self.jumping_sheet = pg.image.load(spritePath + '/Jump_8.png').convert_alpha()

        # Scale sprite sheets
        self.idle_sheet = pg.transform.scale(self.idle_sheet, (self.width * 4, self.height))
        self.running_sheet = pg.transform.scale(self.running_sheet, (self.width * 6, self.height))
        self.jumping_sheet = pg.transform.scale(self.jumping_sheet, (self.width * 8, self.height))

        self.sprites = {
            'idle': self.idle_sheet,
            'running': self.running_sheet,
            'jumping': self.jumping_sheet,
            'running_and_jumping': self.jumping_sheet
        }

        # Set initial sprite to idle
        self.state = 'idle'
        self.sprite_sheet = self.sprites[self.state]
        self.image = self.get_frame(0)
        self.rect = self.image.get_rect()

    def movementEvents(self, collisions, event, otherPlayer):
        if event.type == KEYDOWN:
            if event.key == self.rightKey:
                self.movingRight = True
                self.state = 'running'
            if event.key == self.leftKey:
                self.movingLeft = True
                self.state = 'running'
            if event.key == self.upKey:
                if collisions['bottom']:
                    self.yMomentum = -18
                    self.state = 'jumping'        
            if event.key == self.downkey:
                otherPlayer.yMomentum = -10
                if collisions['right']:
                    otherPlayer.movingRight = True
                if collisions['left']:
                    otherPlayer.movingLeft = True

        if event.type == KEYUP:
            if event.key == self.rightKey:
                self.movingRight = False
                self.state = 'idle'
            if event.key == self.leftKey:
                self.movingLeft = False
                self.state = 'idle'

    def getMovement(self):
        playerMovement = [0,0]
        if self.movingRight:
            playerMovement[0] += 5
        elif self.movingLeft:
            playerMovement[0] -= 5
        self.yMomentum += 1
        if self.yMomentum > 10:
            self.yMomentum = 10
        playerMovement[1] += self.yMomentum
        return playerMovement
    
    def get_frame(self, frame, scale=1):
        # Calculate position of current frame in sprite sheet
        x = frame * self.width
        y = 0
        rect = pg.Rect(x, y, self.width, self.height)
        image = pg.Surface(rect.size, pg.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), rect)

        # Scale image
        width = int(self.width * scale)
        height = int(self.height * scale)
        image = pg.transform.scale(image, (width, height))

        return image
    
    def draw(self, surface, scale=1):
        keys = pg.key.get_pressed()
        # Update sprite image based on current state
        if self.state == 'idle':
            self.sprite_sheet = self.idle_sheet
            frame = (pg.time.get_ticks() // 100) % 4 # animate by cycling through frames every 100ms
        elif self.state == 'running':
            self.sprite_sheet = self.running_sheet
            frame = (pg.time.get_ticks() // 100) % 6 # animate by cycling through frames every 100ms
        elif self.state == 'jumping' or self.state == 'running_and_jumping':
            self.sprite_sheet = self.jumping_sheet
            frame = (pg.time.get_ticks() // 70) % 8 # animate by cycling through frames every 100ms

        self.image = self.get_frame(frame, scale)

        # Flip image if player is facing left
        if keys[self.leftKey]:
            self.image = pg.transform.flip(self.image, True, False)

        # Scale rect to match scaled image
        rect = self.image.get_rect()
        rect.x = int(self.x * scale)
        rect.y = int(self.y * scale)
        rect.width = int(rect.width * scale)
        rect.height = int(rect.height * scale)
        
        # Set the x and y attributes of the Player class to the position of the player rectangle
        self.x = self.playerRect.x
        self.y = self.playerRect.y

        # Blit the sprite to the screen using the x and y attributes of the Player class
        surface.blit(self.image, (self.x-11, self.y-10))
