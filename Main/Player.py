import pygame
import sys

class Player:
    def __init__(self, relativePath): #relative path here refers to the path in your filesystem to the asset. For me and my repository, it's: Main\Assets\Pink_Monster.png
                                      #Keep in mind you don't have to type the FULL path. Relative path starts at your working folder instead of your drive.
                                      #for instance, the absolute (full) path for me is: H:\Projects\SWEN-Project\Main\Assets\Pink_Monster.png, but my 
                                      #working folder is SWEN-Project, so I can cut out everything before it.
        path = relativePath
        self.playerImage = pygame.image.load(path).convert()
        self.playerImage.set_colorkey((255, 255, 255))
        self.playerRect = pygame.Rect(50, 50, self.playerImage.get_width(), self.playerImage.get_height())
        self.movingRight = False
        self.movingLeft = False
        self.yMomentum = 0
