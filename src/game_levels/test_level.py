from src.config import GAME_CONFIG as config
from src.const import GameConstants as const

from src.game_levels.levels import load_level

import sys

try: test_level = load_level(sys.argv[-1])
except IOError: test_level = False

ORIGINAL_LEVEL_CONFIG = test_level

LEVEL_CONFIG = ORIGINAL_LEVEL_CONFIG.copy() if test_level else False

def get_level_config():
    return LEVEL_CONFIG

