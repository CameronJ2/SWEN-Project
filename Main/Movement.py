import pygame
from Player import Player
import Main


def movementEvents(pygame.event): #to be used in the game loop
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                player1.movingRight = True
            if event.key == K_LEFT:
                player1.movingLeft = True
            if event.key == K_UP:
                if P1_gravity < 20:
                    player1.yMomentum = -6
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                player1.movingRight = False
            if event.key == K_LEFT:
                player1.movingLeft = False
