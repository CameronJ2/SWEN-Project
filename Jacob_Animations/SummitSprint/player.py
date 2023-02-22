import pygame as pg
import math

class Player:
    def __init__(self, x, y, width, height, scale=2):
        self.x = x
        self.y = y
        self.width = int(width * scale)
        self.height = int(height * scale)
        self.velocity_x = 0
        self.velocity_y = 0
        self.max_velocity = 10
        self.gravity = 0.5
        self.jump_power = 20
        self.jump_angle = math.radians(45) # set jump angle to 45 degrees

        # Load sprite sheets
        self.idle_sheet = pg.image.load('img/Owl_Mon/Owlet_Monster_Idle_4.png').convert_alpha()
        self.running_sheet = pg.image.load('img/Owl_Mon/Owlet_Monster_Run_6.png').convert_alpha()
        self.jumping_sheet = pg.image.load('img/Owl_Mon/Owlet_Monster_Jump_8.png').convert_alpha()

        # Scale sprite sheets
        self.idle_sheet = pg.transform.scale(self.idle_sheet, (self.width * 4, self.height))
        self.running_sheet = pg.transform.scale(self.running_sheet, (self.width * 6, self.height))
        self.jumping_sheet = pg.transform.scale(self.jumping_sheet, (self.width * 8, self.height))

        # Create dictionary of sprite sheets
        self.sprites = {
            'idle': self.idle_sheet,
            'running': self.running_sheet,
            'jumping': self.jumping_sheet
        }

        # Set initial sprite to idle
        self.state = 'idle'
        self.sprite_sheet = self.sprites[self.state]
        self.image = self.get_frame(0)
        self.rect = self.image.get_rect()
    
    #This sets up the controls for the character
    def move(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_a] and self.x > self.velocity_x:
            self.velocity_x = 6
            self.x -= self.velocity_x
            self.state = 'running'
        elif keys[pg.K_d] and self.x < 640 - self.width - self.velocity_x:
            self.velocity_x = 6
            self.x += self.velocity_x
            self.state = 'running'
        else:
            self.velocity_x = 0
            self.state = 'idle'

        # Apply gravity
        self.velocity_y = min(self.velocity_y + self.gravity, self.max_velocity)
        self.y += self.velocity_y

        # Check for collisions with the bottom of the screen
        if self.y > 640 - self.height:
            self.y = 640 - self.height
            self.velocity_y = 0

        # Check for jumping
        if keys[pg.K_w] and self.velocity_y == 0:
            # calculate x and y velocities for jump
            self.velocity_y = -self.jump_power * math.sin(self.jump_angle)
            self.velocity_x = self.jump_power * math.cos(self.jump_angle)
            self.state = 'jumping'

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
        else:
            self.sprite_sheet = self.jumping_sheet
            frame = (pg.time.get_ticks() // 100) % 8 # animate by cycling through frames every 100ms

        self.image = self.get_frame(frame, scale)

        # Flip image if player is facing left
        if keys[pg.K_a]:
            self.image = pg.transform.flip(self.image, True, False)

        # Scale rect to match scaled image
        rect = self.image.get_rect()
        rect.x = int(self.x * scale)
        rect.y = int(self.y * scale)
        rect.width = int(rect.width * scale)
        rect.height = int(rect.height * scale)

        surface.blit(self.image, rect)