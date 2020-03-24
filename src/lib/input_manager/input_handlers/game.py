"""Apply system related game state mutations based off of player input"""

from src.const import (
    GameConstants,
    InputConstants,
)

from src.lib.input_manager.input_handlers.utils import process_button_event

def toggle_debug_mode(state):
    """Enable/disable debug mode"""
    if state[GameConstants.IS_DEBUG_MODE_ENABLED]:
        state[GameConstants.IS_DEBUG_MODE_ACTIVE] = not state[GameConstants.IS_DEBUG_MODE_ACTIVE]

        return True

    return False

def toggle_freeze_frame(state):
    if state[GameConstants.IS_DEBUG_MODE_ACTIVE]:
        # Manually advance to the next frame
        state[GameConstants.SHOULD_ADVANCE_FRAME] = not state[GameConstants.SHOULD_ADVANCE_FRAME]

    return True

def flag_game_for_exit(state):
    """Flag the game for shutdown"""
    state[GameConstants.SHOULD_EXIT_FLAG] = True

    return True

# @TODO pull these from .env
DEBUG_KEY = InputConstants.BUTTON_D_KEY
FREEZE_FRAME_KEY = InputConstants.BUTTON_N_KEY

BUTTON_PRESS_INPUT_KEY_HANDLER_MAP = {
    DEBUG_KEY: toggle_debug_mode,
    FREEZE_FRAME_KEY: toggle_freeze_frame,
}

BUTTON_RELEASE_INPUT_KEY_HANDLER_MAP = {
    InputConstants.BUTTON_QUIT: flag_game_for_exit,
    InputConstants.BUTTON_ESCAPE: flag_game_for_exit,
}

def process_input(state, player_input_data):
    """Process player input and apply game state mutations if necessary"""
    if player_input_data["type"] == InputConstants.BUTTON_RELEASED:
        return process_button_event(state, player_input_data, BUTTON_RELEASE_INPUT_KEY_HANDLER_MAP)

    return process_button_event(state, player_input_data, BUTTON_PRESS_INPUT_KEY_HANDLER_MAP)
