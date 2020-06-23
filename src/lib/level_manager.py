from src.game_levels import development_playground
from src.game_levels import test_level
from src.game_levels.levels import load_level, load_actor
from src.const import GameConstants as const
from src.config import GAME_CONFIG as config

import sys

levels_to_load = ['home', 'hallway', 'kitchen', 'livingroom', 'pantry']
LEVEL_MAP = {}
for level in levels_to_load:
    LEVEL_MAP[level] = load_level(level)
    LEVEL_MAP[const.DEFAULT_LEVEL] = load_level('default')

LEVEL_ACTOR_MAP = {}
for level in LEVEL_MAP.keys():
    LEVEL_ACTOR_MAP[level] = [load_actor(a) for a in LEVEL_MAP[level][const.ACTORS]]

def get_level(game_state, game_level_key=False):
    """Get level configuration for the provided level key"""
    if game_level_key in LEVEL_MAP:
        game_level_config = LEVEL_MAP.get(game_level_key)
    else:
        game_level_config = LEVEL_MAP.get(const.DEFAULT_LEVEL)

    if not game_level_config:
        raise ValueError('Target game level does not exist')

    game_state[const.LEVEL] = game_level_config
    game_state[const.LOADED_ACTORS] = LEVEL_ACTOR_MAP[game_level_key]


    
