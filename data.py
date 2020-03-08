import pygame
from pygame.locals import *
from pygame import Surface

def load_spritesheet(filename, data, colorkey=None):
    """data should be dict with key: ((x, y), (w, h)), assumes w, h are 32, 32"""
    surf = pygame.image.load(filename).convert()
    sheet = {}
    for name in data:
        sprite = Surface(data[name][1])
        x, y = 0 - data[name][0][0], 0 - data[name][0][1]
        sprite.blit(surf, (x, y))
        sprite.set_colorkey(colorkey)
        sheet[name] = sprite
    return sheet

sheet_data = {
    "IDLE": ((0, 0), (64, 64)),
    "RUN:0": ((64, 0), (64, 64)),
    "RUN:1": ((128, 0), (64, 64)),
    "RUN:2": ((192, 0), (64, 64)),
    "RUN:3": ((256, 0), (64, 64)),
    "SLIDE:0": ((320, 0), (64, 64)),
    "SLIDE:1": ((384, 0), (64, 64)),
    "JUMPSQUAT:0": ((448, 0), (64, 64)),
    "JUMPSQUAT:1": ((512, 0), (64, 64)),
    "RISING": ((576, 0), (64, 64)),
    "AIR": ((640, 0), (64, 64)),
    "FALLING": ((704, 0), (64, 64)),
    "LAND": ((768, 0), (64, 64)),
}

sprites = load_spritesheet('img/player.png', sheet_data, colorkey=(1, 255, 1))
