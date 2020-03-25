"""Apply player related game state mutations based off of player input"""
from src.const import (
    InputConstants,
    GameConstants,
)

from src.lib.input_manager.input_handlers.utils import process_button_event

def move_player_right(state):
    """Move character to the right"""
    state[GameConstants.MOVE] = min(state[GameConstants.MOVE] + 1, 1)

def move_player_left(state):
    """Move character to the left"""
    state[GameConstants.MOVE] = max(state[GameConstants.MOVE] - 1, -1)

def move_player_jump(state):
    """Make character jump"""
    state[GameConstants.JUMP] += 1

def move_player_dive(state):
    """Make character dive"""
    state[GameConstants.DIVE] += 1

def move_player_right_stop(state):
    """Stop moving to the right when in motion"""
    state[GameConstants.MOVE] -= 1

def move_player_left_stop(state):
    """Stop moving to the left when in motion"""
    state[GameConstants.MOVE] += 1

BUTTON_PRESS_INPUT_KEY_HANDLER_MAP = {
    InputConstants.BUTTON_RIGHT: move_player_right,
    InputConstants.BUTTON_LEFT: move_player_left,
    InputConstants.BUTTON_ONE: move_player_jump,
    InputConstants.BUTTON_TWO: move_player_dive,
}

BUTTON_RELEASE_INPUT_KEY_HANDLER_MAP = {
    InputConstants.BUTTON_RIGHT: move_player_right_stop,
    InputConstants.BUTTON_LEFT: move_player_left_stop,
}

def process_input(state, player_input_data):
    """Process player input and apply game state mutations if necessary"""
    if player_input_data["type"] == InputConstants.BUTTON_PRESSED:
        return process_button_event(state, player_input_data, BUTTON_PRESS_INPUT_KEY_HANDLER_MAP)

    return process_button_event(state, player_input_data, BUTTON_RELEASE_INPUT_KEY_HANDLER_MAP)
