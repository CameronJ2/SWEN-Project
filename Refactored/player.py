import pygame as pg
import math
from levelLoader import load_level, load_tiles
from levelLoader import tile_folder

gameOver = 0

lavaGroup = pg.sprite.Group()

class Player:
    def __init__(self, upkey, leftkey, rightkey, x, y, width, height, scale=2):
        self.x = x
        self.y = y
        self.width = int(width * scale)
        self.height = int(height * scale)
        self.velocity_x = 0
        self.velocity_y = 0
        self.max_velocity = 10
        self.gravity = 0.5
        self.jump_power = 20
        self.jump_angle = math.radians(30) # set jump angle to 45 degrees
        self.upkey = upkey
        self.leftkey = leftkey
        self.rightkey = rightkey

        # Load sprite sheets
        self.idle_sheet = pg.image.load('Refactored/img/Owl_Mon/Idle_4.png').convert_alpha()
        self.running_sheet = pg.image.load('Refactored/img/Owl_Mon/Run_6.png').convert_alpha()
        self.jumping_sheet = pg.image.load('Refactored/img/Owl_Mon/Jump_8.png').convert_alpha()

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
    
    #This sets up the controls for the character
    def update(self, gameOver):
        self.velocity_x = 0
        self.y = 0
        
        if gameOver == 0:
            
            keys = pg.key.get_pressed()

            if keys[self.leftkey] and self.x > self.velocity_x:
                self.velocity_x = 6
                self.x -= self.velocity_x
                self.state = 'running'
            elif keys[self.rightkey] and self.x < 960 - self.width - self.velocity_x:
                self.velocity_x = 6
                self.x += self.velocity_x
                self.state = 'running'
            else:
                self.velocity_x = 0
                if self.velocity_y == 0:
                    self.state = 'idle'
                
            for tile in tile_folder:
                if tile.colliderect(self.x, self.velocity_x, self.y, self.width, self.height):
                    self.velocity_x = 0
                if tile.colliderect(self.x, self.velocity_x, self.y, self.width, self.height):
                    if self.velocity_y >= 0:
                        self.y = tile[61].top - self.rect.bottom
                        self.velocity_y = 0
                    
            #check collision with lava        
            if pg.sprite.spritecollide(self, lavaGroup, False):
                gameOver = -1
                
        elif gameOver == -1:
            self.image = 'idle'
            if self.y > 200:
                self.y -= 5
                
                
        # Apply gravity
        self.velocity_y = min(self.velocity_y + self.gravity, self.max_velocity)
        self.y += self.velocity_y

        # Check for collisions with the bottom of the screen
        if self.y > 640 - self.height:
            self.y = 640 - self.height
            self.velocity_y = 0

        if keys[self.upkey] and self.velocity_y == 0:
            # calculate x and y velocities for jump
            self.velocity_y = -self.jump_power * math.sin(self.jump_angle)
            self.velocity_x = self.jump_power * math.cos(self.jump_angle)
            if self.velocity_x != 0: # check if the player is also running
                self.state = 'running_and_jumping'
            else:
                self.state = 'jumping'
                
        return gameOver


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
        if keys[self.leftkey]:
            self.image = pg.transform.flip(self.image, True, False)

        # Scale rect to match scaled image
        rect = self.image.get_rect()
        rect.x = int(self.x * scale)
        rect.y = int(self.y * scale)
        rect.width = int(rect.width * scale)
        rect.height = int(rect.height * scale)

        surface.blit(self.image, rect)