from src.config import GAME_CONFIG as config
from src.const import GameConstants as const

DEFAULT_LEVEL_CONFIG = {
    const.PLATFORMS: [
        (-config[const.WIDTH], 384, config[const.WIDTH] * 3, 96, 2),
        (-config[const.WIDTH], -256, 64, 640, 3),
        (config[const.WIDTH] * 2 - 64, -256, 64, 640, 3),
        (384, 320, 128, 64, 1),
        (612, 256, 64, 128, 1),
        (128, 192, 128, 192, 3),
        (-128, 256, 128, 128, 3),
        (0, 128, 128, 256, 3),
        (-config[const.WIDTH]+64, 64, 512, 64, 2),
        (256, 0, 128, 64, 1),
        (384, -64, 128*3, 64, 1),
        (512, -256, 128, 64, 1),
        (0, -256, 64*5, 64, 1),
    ],
    const.ENEMIES:[],
    const.SPIKES:[],
}

LEVEL_CONFIG = DEFAULT_LEVEL_CONFIG.copy()

def get_level_config():
    return LEVEL_CONFIG
