import pygame

from pygame.locals import *
from pygame import Surface

SPRITE_NAME_CONFIG_MAP = {
    "player": {
        "color_key": (1, 255, 1),
        "image_path": "img/player.png",
        "coordinate_data": {
            "IDLE": ((0, 0), (64, 64)),
            "RUN:0": ((64, 0), (64, 64)),
            "RUN:8": ((128, 0), (64, 64)),
            "RUN:15": ((192, 0), (64, 64)),
            "RUN:23": ((256, 0), (64, 64)),
            "SLIDE:0": ((320, 0), (64, 64)),
            "SLIDE:1": ((384, 0), (64, 64)),
            "JUMPSQUAT:0": ((448, 0), (64, 64)),
            "JUMPSQUAT:1": ((512, 0), (64, 64)),
            "RISING": ((576, 0), (64, 64)),
            "AIR": ((640, 0), (64, 64)),
            "FALLING": ((704, 0), (64, 64)),
            "LAND": ((768, 0), (64, 64)),
        }
    }
}

def load_spritesheet(sprite_name):
    sprite_config = SPRITE_NAME_CONFIG_MAP[sprite_name]
    """data should be dict with key: ((x, y), (w, h))"""
    surf = pygame.image.load(sprite_config["image_path"]).convert()
    sheet = {}

    for name in sprite_config["coordinate_data"]:
        sprite = Surface(sprite_config["coordinate_data"][name][1])
        x, y = 0 - sprite_config["coordinate_data"][name][0][0], 0 - sprite_config["coordinate_data"][name][0][1]
        sprite.blit(surf, (x, y))
        sprite.set_colorkey(sprite_config["color_key"])
        sheet[name] = sprite

    return sheet
