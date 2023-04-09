import pygame as pg

tile_size = 32

class Lava(pg.sprite.Sprite):
    def __init__(self,x, y):
        pg.sprite.Sprite.__init__(self)
        waterImage = pg.image.load('MyAssets/lava.png')
        self.image = pg.transform.scale(waterImage, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y