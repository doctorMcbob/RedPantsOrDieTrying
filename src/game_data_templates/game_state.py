"""Template for default game state dictionary"""
import sys

from src.const import GameConstants as const
from src.config import GAME_CONFIG as config

IS_DEBUG_MODE_ENABLED = "-d" in sys.argv

GAME_STATE_TEMPLATE = {
    const.WIDTH: config[const.WIDTH],
    const.HEIGHT: config[const.HEIGHT],
    const.IS_DEBUG_MODE_ACTIVE: IS_DEBUG_MODE_ENABLED and "-f" in sys.argv,
    const.IS_DEBUG_MODE_ENABLED: IS_DEBUG_MODE_ENABLED,
    const.FONTS: {},
    const.SHOULD_EXIT_FLAG: False,
    const.SHOULD_ADVANCE_FRAME: True,
}
