from src.const import GameConstants as const

# States that do not require special hitbox configurations (aka "default hitbox size config")
NORMAL_HITBOX_SIZE_CONFIG = ((16, 0), (32, 64))
NORMAL_HITBOX_SIZE_CONFIG_STATE_KEY_LIST = [
    const.IDLE, const.RUN, const.SLIDE,
    const.JUMPSQUAT, const.RISING, const.LAND,
    const.BONK, const.BONKLAND, const.FALLING,
    const.AIR, const.DIVESTART,
    const.KICKFLIP0, const.KICKFLIP1, const.KICKFLIP2,
]

# States that require special hitbox size configurations
SPECIAL_HITBOX_SIZE_CONFIG_STATE_KEY_MAP = {
    const.DIVE: ((0, 0), (64, 64)),
    const.DIVELAND: ((0, 32), (64, 32)),
    const.DIVELANDJUMP: ((0, 0), (64, 64))
}

DEFAULT_HITBOX_SIZE_CONFIG_STATE_KEY_MAP = SPECIAL_HITBOX_SIZE_CONFIG_STATE_KEY_MAP.copy()

for state_key in NORMAL_HITBOX_SIZE_CONFIG_STATE_KEY_LIST:
    DEFAULT_HITBOX_SIZE_CONFIG_STATE_KEY_MAP[state_key] = NORMAL_HITBOX_SIZE_CONFIG

GAME_PLAYER_HITBOX_CONFIG = DEFAULT_HITBOX_SIZE_CONFIG_STATE_KEY_MAP.copy()
