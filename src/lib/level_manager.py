from src.game_levels import development_playground
from src.game_levels import test_level
from src.game_levels.levels import load_level
from src.const import GameConstants as const
from src.config import GAME_CONFIG as config

import sys

LEVEL_MAP = {
    "development_playground": development_playground,
}

GAME_LEVEL_KEY_CONFIG_MAP = {
    const.DEFAULT_LEVEL: LEVEL_MAP[config[const.DEFAULT_LEVEL]],
}

if test_level.get_level_config():
    LEVEL_MAP[sys.argv[-1]] = test_level
    GAME_LEVEL_KEY_CONFIG_MAP[sys.argv[-1]] = LEVEL_MAP[sys.argv[-1]]

def get_level(game_level_key=False):
    """Get level configuration for the provided level key"""
    if game_level_key in GAME_LEVEL_KEY_CONFIG_MAP:
        game_level_config = GAME_LEVEL_KEY_CONFIG_MAP.get(game_level_key)
    else:
        game_level_config = GAME_LEVEL_KEY_CONFIG_MAP.get(const.DEFAULT_LEVEL)

    if not game_level_config:
        raise ValueError('Target game level does not exist')

    return game_level_config.get_level_config()



    
