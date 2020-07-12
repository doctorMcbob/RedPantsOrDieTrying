DOOR_SPRITE_CONFIG = {
    "color_key": (1, 255, 1),
    "image_path": "img/collectable.png",
    "coordinate_data": {
        "coin": ((0, 0), (32, 32)),
        "banana": ((0, 32), (32, 32)),
    }
}

SPRITE_CONFIG = DOOR_SPRITE_CONFIG.copy()

def get_sprite():
    return SPRITE_CONFIG
