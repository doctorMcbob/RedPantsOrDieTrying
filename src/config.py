"""Default game configuration"""
import os

from src.const import GameConstants as const

GAME_CONFIG = {
    const.WIDTH: int(os.getenv("WINDOW_WIDTH")),
    const.HEIGHT: int(os.getenv("WINDOW_HEIGHT")),
    const.DEFAULT_LEVEL: os.getenv("DEFAULT_LEVEL"),
    const.PLAYER_ONE_SPRITE_SHEET: os.getenv("PLAYER_ONE_SPRITE_SHEET_KEY")
}
