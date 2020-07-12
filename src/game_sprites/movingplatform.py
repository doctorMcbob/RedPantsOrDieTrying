DOOR_SPRITE_CONFIG = {
    "color_key": (1, 255, 1),
    "image_path": "img/movingplatform.png",
    "coordinate_data": {
        "wood": ((0, 0), (160, 64)),
    }
}

SPRITE_CONFIG = DOOR_SPRITE_CONFIG.copy()

def get_sprite():
    return SPRITE_CONFIG
