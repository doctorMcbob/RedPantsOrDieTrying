DEFAULT_SPRITE_CONFIG = {
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
        "DIVESTART": ((832, 0), (64, 64)),
        "DIVE": ((896, 0), (64, 64)),
        "DIVELAND": ((960, 0), (64, 64)),
        "DIVELANDJUMP": ((1024, 0), (64, 64)),
        "BONK": ((1088, 0), (64, 64)),
        "BONKLAND": ((1152, 0), (64, 64)),
    }
}

SPRITE_CONFIG = DEFAULT_SPRITE_CONFIG.copy()

def get_sprite():
    return SPRITE_CONFIG
