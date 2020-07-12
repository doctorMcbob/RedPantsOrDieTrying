import pygame

from pygame import Surface
from src.game_sprites import player_one as player_one_sprite
from src.game_sprites import (
    platform_sprites, spike, trampoline, door,
    collectable, movingplatform, leaper
)

# Enabled sprites
SPRITE_SHEET_KEY_CONFIG_MAP = {
    "player": player_one_sprite.get_sprite(),
    "spike": spike.get_sprite(),
    "Trampoline": trampoline.get_sprite(),
    "Door": door.get_sprite(),
    "Collectable": collectable.get_sprite(),
    "Moving Platform": movingplatform.get_sprite(),
    "Leaper": leaper.get_sprite(),
}
for n in range(platform_sprites.plat_num):
    SPRITE_SHEET_KEY_CONFIG_MAP["platform" + str(n)] = platform_sprites.get_sprite(n)

def load_sprite_sheet(sprite_sheet_key):
    sprite_sheet_config = SPRITE_SHEET_KEY_CONFIG_MAP.get(sprite_sheet_key)
    sprite_sheet_data = {}

    if not sprite_sheet_config:
        return sprite_sheet_data

    # data should be dict with key: ((x, y), (w, h))
    sprite_sheet_surface = pygame.image.load(sprite_sheet_config["image_path"]).convert()

    for sheet_key in sprite_sheet_config["coordinate_data"]:
        coordinate_data = sprite_sheet_config["coordinate_data"][sheet_key]
        sprite_sheet = Surface(coordinate_data[1])
        x_coord = 0 - coordinate_data[0][0]
        y_coord = 0 - coordinate_data[0][1]

        sprite_sheet.blit(sprite_sheet_surface, (x_coord, y_coord))
        sprite_sheet.set_colorkey(sprite_sheet_config["color_key"])

        sprite_sheet_data[sheet_key] = sprite_sheet

    return sprite_sheet_data
