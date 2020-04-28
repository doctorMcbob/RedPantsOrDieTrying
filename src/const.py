"""Game constants"""

# pylint: disable=too-few-public-methods
from enum import Enum

class InputConstants(Enum):
    """Enum used to store controller/input related constants"""
    # Generic game control buttons
    BUTTON_ONE = "USER_INPUT_BUTTON_ONE"
    BUTTON_TWO = "USER_INPUT_BUTTON_TWO"
    BUTTON_UP = "USER_INPUT_BUTTON_UP"
    BUTTON_DOWN = "USER_INPUT_BUTTON_DOWN"
    BUTTON_LEFT = "USER_INPUT_BUTTON_LEFT"
    BUTTON_RIGHT = "USER_INPUT_BUTTON_RIGHT"
    BUTTON_EXIT = "USER_INPUT_BUTTON_EXIT"
    BUTTON_QUIT = "USER_INPUT_BUTTON_QUIT"

    # Generic button events
    BUTTON_PRESSED = "USER_INPUT_EVENT_BUTTON_PRESSED"
    BUTTON_RELEASED = "USER_INPUT_EVENT_BUTTON_RELEASED"

    # Keyboard specific keybindings
    BUTTON_ESCAPE = "USER_INPUT_KEYBOARD_KEY_ESCAPE"
    BUTTON_D_KEY = "USER_INPUT_KEYBOARD_KEY_D"
    BUTTON_N_KEY = "USER_INPUT_KEYBOARD_KEY_N"


class GameConstants(Enum):
    """Enum used to store main game system related constants"""
    WIDTH = "W"
    HEIGHT = "H"
    X_COORD = "X"
    Y_COORD = "Y"
    STATE = "STATE"
    MOVE = "MOV"
    JUMP = "JMP"
    SPEED = "SPEED"
    DIRECTION = "DIR"
    TRACTION = "TRACTION"
    VELOCITY = "X_VEL"
    VERTICAL_VELOCITY = "Y_VEL"
    JUMP_SPEED = "JMPSPEED"
    GRAVITY = "GRAV"
    PLATFORMS = "PLATS"
    ENEMIES = "ENEMIES"
    SPIKES = "SPIKES"
    LEVEL = "LVL"
    DRIFT = "DRIFT"
    FRAME = "FRAME"
    LANDING_FRAME = "LANDF"
    JUMP_SQUAT_FRAME = "JSQUATF"
    SCROLL = "SCROLL"
    DIVESTR = "DIVESTR"
    DSTARTF = "DSTARTF"
    DIVELJSTR = "DIVELJSTR"
    BONKLF = "BONKLF"
    FA = "FA"
    KICKFLIPSTR = "KICKFLIPSTR"
    KICKFLIPLIMIT = "KICKFLIPLIMIT"
    SCREEN = "SCREEN"
    FONTS = "FONT_BOOK"
    FONT_HELVETICA = "HEL16"
    SPRITE_SHEET = "SPRITE_SHEET"
    GAME_CLOCK = "GAME_CLOCK"
    SHOULD_EXIT_FLAG = "SHOULD_EXIT_GAME"
    SHOULD_ADVANCE_FRAME = "SHOULD_FRAME_BE_ADVANCED"
    IS_DEBUG_MODE_ACTIVE = "IS_DEBUG_MODE_ACTIVE"
    IS_DEBUG_MODE_ENABLED = "IS_DEBUG_MODE_ENABLED"
    DEFAULT_LEVEL = "DEFAULT_GAME_LEVEL_CONFIG"
    HITBOX = "HITBOX"
    HITBOX_CONFIG = "HITBOX_SIZE_CONFIG"
    INPUT_HANDLER = "INPUT_HANDLER"
    INPUT_CONFIG = "INPUT_CONFIG"
    SPRITE_SHEET_KEY = "GAME_ENTITY_SPRITE_SHEET_KEY"
    PLAYER_ONE_SPRITE_SHEET = "PLAYER_ONE_SPRITE_SHEET_KEY"
    WALLJUMPSTR = "WALLJUMPSTR"
    WALLJUMPFRM = "WALLJUMPFRM"
    ACTORS = "ACTORS"
    COUNTER = "COUNTER"
    PATH = "PATH"
    SPAWN = "SPAWN"
    DMGFR = "DMGFR"
    NAME = "NAME"
    LOADED_ACTORS = "LOADED_ACTORS"
    TRAITS = "TRAITS"
    TANGIBLE = "TANGIBLE"
    # ----- states -----
    AIR = "AIR"
    SLIDE = "SLIDE"
    IDLE = "IDLE"
    RUN = "RUN"
    LAND = "LAND"
    RISING = "RISING"
    FALLING = "FALLING"
    FASTFALLING = "FASTFALLING"
    DIVESTART = "DIVESTART"
    DIVE = "DIVE"
    DIVELAND = "DIVELAND"
    DIVELANDJUMP = "DIVELANDJUMP"
    BONK = "BONK"
    JUMPSQUAT = "JUMPSQUAT"
    BONKLAND = "BONKLAND"
    KICKFLIP0 = "KICKFLIP0"
    KICKFLIP1 = "KICKFLIP1"
    KICKFLIP2 = "KICKFLIP2"
    WALL = "WALL"
    WALLJUMPSTART = "WALLJUMPSTART"
    DMG = "DMG"
