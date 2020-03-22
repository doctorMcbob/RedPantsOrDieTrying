"""Template for default game state dictionary"""
import sys

from const import GameConstants as const
from config import GAME_CONFIG as config

IS_DEBUG_MODE_ENABLED = "-d" in sys.argv

GAME_STATE_TEMPLATE = {
    const.WIDTH: config[const.WIDTH],
    const.HEIGHT: config[const.HEIGHT],
    const.X_COORD: 0,
    const.Y_COORD: 0,
    const.SCROLL: [0, 0],
    const.VELOCITY: 0,
    const.VERTICAL_VELOCITY: 0,
    const.STATE: const.IDLE,
    const.DIRECTION: 1,
    const.MOVE: 0,
    const.JUMP: 0,
    const.DIVE: 0,
    const.FRAME: 0,
    const.LANDING_FRAME: 2,
    const.JUMP_SQUAT_FRAME: 2,
    const.BONKLF: 5,
    const.DSTARTF: 3,
    const.DIVESTR: 20,
    const.DIVELJSTR: -12,
    const.SPEED: 10,
    const.TRACTION: 2,
    const.DRIFT: 2,
    const.JUMP_SPEED: -24,
    const.GRAVITY: 2,
    const.AIR: 12,
    const.IS_DEBUG_MODE_ACTIVE: IS_DEBUG_MODE_ENABLED and "-f" in sys.argv,
    const.IS_DEBUG_MODE_ENABLED: IS_DEBUG_MODE_ENABLED,
    const.FONTS: {},
    const.SHOULD_EXIT_FLAG: False,
    const.SHOULD_ADVANCE_FRAME: True,
    const.KICKFLIPSTR: -35,
    const.KICKFLIPLIMIT: -18,
    const.HITBOX: ((16, 0), (32, 64)),
}
