LEAPER_SPRITE_CONFIG = {
    "color_key": (1, 255, 1),
    "image_path": "img/leaper.png",
    "coordinate_data": {
        "idle": ((0, 0), (64, 32)),
        "leapstart": ((64, 0), (64, 32)),
        "leaping": ((128, 0), (64, 32)),
    }
}

SPRITE_CONFIG = LEAPER_SPRITE_CONFIG.copy()

def get_sprite():
    return SPRITE_CONFIG
