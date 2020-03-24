"""
Red Pants of Die Trying
this time, its personal

the next big blockbuster red pants game, this time no deadlines
STILL NOT WORRYING ABOUT IT
hopefully I can stay motivated

similar to the last one in achitecture but thinking a little more ahead of time,
taking it slow

platforms [(x, y, w, h, idx)]

---- Notes
Edgecancel dive baby
"""
import sys

from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path('.')
ENV_FILE_PATH = ROOT_DIR / '.env'

# Load environment variables from .env file
load_dotenv(dotenv_path=ENV_FILE_PATH)

# Add root game directory to system path for module loading
sys.path.append(ROOT_DIR.as_posix())

# pylint:disable=wrong-import-position
from src.game import (
    init_game,
    main_loop,
)

from src.game_data_templates.game_state import GAME_STATE_TEMPLATE

UNINITIALIZED_GAME_STATE = GAME_STATE_TEMPLATE.copy()

# Initialize game components and game state
GAME_STATE = init_game(UNINITIALIZED_GAME_STATE)

# Start main game loop
main_loop(GAME_STATE)
