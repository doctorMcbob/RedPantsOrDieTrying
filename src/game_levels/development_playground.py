from src.config import GAME_CONFIG as config
from src.const import GameConstants as const

DEFAULT_LEVEL_CONFIG = {
    const.PLATFORMS: [
        (-config[const.WIDTH], 400, config[const.WIDTH] * 3, 96, 2),
        (-config[const.WIDTH], -200, 64, 600, 3),
        (config[const.WIDTH]*2-64, -200, 64, 600, 3),
        (420, 336, 126, 64, 1),
        (612, 400-126, 64, 126, 1),
        (420-(64*4), 336-126, 126, 64, 1),
        (420-(64*6), 336-126-64, 126, 64, 1),
        (-config[const.WIDTH]+64, 336-256, 256*2, 64, 2),
        (420-(64*2), 0, 126, 64, 1),
        (420, -64, 126*3, 64, 1),
        (420+(64*2), -256, 126, 64, 1),
        (420-(64*6), -256, 64*5, 64, 1),
    ],
    const.ENEMIES:[],
    const.SPIKES:[],
}

LEVEL_CONFIG = DEFAULT_LEVEL_CONFIG.copy()

def get_level_config():
    return LEVEL_CONFIG
