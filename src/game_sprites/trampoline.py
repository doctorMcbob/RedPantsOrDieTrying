TRAMP_SPRITE_CONFIG = {
    "color_key": (1, 255, 1),
    "image_path": "img/trampoline.png",
    "coordinate_data": {
        "couch": ((0, 0), (128, 64)),
        "smallbed": ((0, 64), (128, 32)),
        "bigbed": ((0, 96), (160, 64))
    }
}

SPRITE_CONFIG = TRAMP_SPRITE_CONFIG.copy()

def get_sprite():
    return SPRITE_CONFIG
