import pygame

from pygame.locals import *
from pygame import Surface
from src.game_sprites import player_one as player_one_sprite

SPRITE_NAME_CONFIG_MAP = {
    "player": player_one_sprite.get_sprite(),
}

def load_sprite_sheet(sprite_name):
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
