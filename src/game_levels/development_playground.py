from src.config import GAME_CONFIG as config
from src.const import GameConstants as const

from src.game_levels.levels import load_level

DEFAULT_LEVEL_CONFIG = load_level("default")

LEVEL_CONFIG = DEFAULT_LEVEL_CONFIG.copy()

def get_level_config():
    return LEVEL_CONFIG
