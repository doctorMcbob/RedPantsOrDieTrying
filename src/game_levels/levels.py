from src.config import GAME_CONFIG as config
from src.const import GameConstants as const

from pathlib import Path

LEVELS = Path('.') / "src/game_levels/bin/"
def load_level(filename):
    with open(LEVELS / filename, "r") as f:
        level_data = eval(f.read())
    return {
        const.PLATFORMS: level_data["PLATS"],
        const.ENEMIES: level_data["ENEMIES"],
        const.SPIKES: level_data["SPIKES"],
    }

