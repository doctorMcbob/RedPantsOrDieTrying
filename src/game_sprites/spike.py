SPIKE_SPRITE_CONFIG = {
    "color_key": (1, 255, 1),
    "image_path": "img/spike.png",
    "coordinate_data": {
        "spike": ((0, 0), (32, 32)),
    }
}

SPRITE_CONFIG = SPIKE_SPRITE_CONFIG.copy()

def get_sprite():
    return SPRITE_CONFIG
