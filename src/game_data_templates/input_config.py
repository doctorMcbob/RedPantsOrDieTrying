"""User input configuration - manages keybindings and supplies input config for session"""

# pylint: disable=no-name-in-module
"""
This prevents pylint from blowing up when using imported locals globally
@TODO find a better way to fix this
"""
from pygame.locals import (
    K_z,
    K_x,
    K_LEFT,
    K_UP,
    K_RIGHT,
    K_DOWN,
    QUIT,
    KEYDOWN,
    K_ESCAPE,
    K_d,
    K_n,
    KEYUP,
)
# pylint: enable=no-name-in-module

from const import InputConstants as const

INPUT_CONFIG_TEMPLATE = {
    # Basic Controls
    const.BUTTON_ONE: K_z,
    const.BUTTON_TWO: K_x,
    const.BUTTON_LEFT: K_LEFT,
    const.BUTTON_UP: K_UP,
    const.BUTTON_RIGHT: K_RIGHT,
    const.BUTTON_DOWN: K_DOWN,
    # Utility/State related keys (button press, button release, etc)
    const.BUTTON_PRESSED: KEYDOWN,
    const.BUTTON_RELEASED: KEYUP,
    const.BUTTON_QUIT: QUIT,
    const.BUTTON_ESCAPE: K_ESCAPE,
    # Character specific keybindings
    const.BUTTON_D_KEY: K_d,
    const.BUTTON_N_KEY: K_n,
}
