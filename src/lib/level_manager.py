from src.game_levels import development_playground
from const import GameConstants as const
from config import GAME_CONFIG as config

LEVEL_MAP = {
    "development_playground": development_playground,
}

GAME_LEVEL_KEY_CONFIG_MAP = {
    const.DEFAULT_LEVEL: LEVEL_MAP[config[const.DEFAULT_LEVEL]],
}

def get_level(game_level_key=False):
    """Get level configuration for the provided level key"""
    game_level_config = GAME_LEVEL_KEY_CONFIG_MAP.get(game_level_key or const.DEFAULT_LEVEL)

    if not game_level_config:
        raise ValueError('Target game level does not exist')

    return game_level_config.get_level_config()
