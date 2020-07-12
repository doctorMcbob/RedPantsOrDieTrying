DOOR_SPRITE_CONFIG = {
    "color_key": (1, 255, 1),
    "image_path": "img/door.png",
    "coordinate_data": {
        "door": ((0, 0), (64, 64)),
    }
}

SPRITE_CONFIG = DOOR_SPRITE_CONFIG.copy()

def get_sprite():
    return SPRITE_CONFIG
