from src.config import GAME_CONFIG as config
from src.const import GameConstants as const

DEFAULT_LEVEL_CONFIG = {
    const.PLATFORMS: [
        (-config[const.WIDTH], 400, config[const.WIDTH] * 3, 96, 2),
        (420, 336, 126, 64, 1),
        (612, 400-126, 64, 126, 1),
        (420-(64*3), 336-126, 64, 64, 1),
        (420-(64*6), 336-126-64, 126, 64, 1)
    ],
    const.ENEMIES:[],
    const.SPIKES:[],
}

LEVEL_CONFIG = DEFAULT_LEVEL_CONFIG.copy()

def get_level_config():
    return LEVEL_CONFIG
