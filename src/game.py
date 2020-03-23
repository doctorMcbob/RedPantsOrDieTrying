import pygame

import src.lib.level_manager as level_manager

from src.lib.input_manager.input_handlers import (
    game as game_input_handler,
)

from src.lib import utils
from src.lib.input_manager import input_interpreter
from src.game_objects.game_player import GamePlayer
from src.game_objects.game_world import GameWorld
from src.game_data_templates.player_state import PLAYER_STATE_TEMPLATE
from src.game_data_templates.game_world_state import GAME_WORLD_STATE_TEMPLATE
from src.game_data_templates.game_player_hitbox_config import GAME_PLAYER_HITBOX_CONFIG

from src.game_data_templates.input_config import (
    INPUT_CONFIG_TEMPLATE,
)

from src.const import GameConstants as const
from src.config import GAME_CONFIG as config

GAME_PLAYER_ONE = GamePlayer(
    PLAYER_STATE_TEMPLATE,
    config[const.PLAYER_ONE_SPRITE_SHEET],
    GAME_PLAYER_HITBOX_CONFIG
)

GAME_WORLD = GameWorld(GAME_WORLD_STATE_TEMPLATE)
GAME_PLAYER_LIST = [GAME_PLAYER_ONE]
GAME_OBJECT_LIST = [GAME_WORLD, GAME_PLAYER_ONE]
GAME_SYSTEM_INPUT_CONFIG = INPUT_CONFIG_TEMPLATE.copy()

def init_game(game_state):
    # pylint: disable=no-member
    pygame.init()
    # pylint: enable=no-member

    game_state[const.SCREEN] = pygame.display.set_mode((
        game_state[const.WIDTH],
        game_state[const.HEIGHT]
    ))

    game_state[const.LEVEL] = level_manager.get_level()
    game_state[const.GAME_CLOCK] = pygame.time.Clock()

    # @TODO move to src.font_book.py
    game_state[const.FONTS][const.FONT_HELVETICA] = pygame.font.SysFont("Helvetica", 16)

    pygame.display.set_caption("lookin good")

    GAME_PLAYER_ONE.initialize()

    return game_state

def draw_screen(game_state, game_world_surface):
    game_state[const.SCREEN].blit(game_world_surface, (0, 0))
    pygame.display.update()

def update_player_states(game_state, game_world_state, raw_game_inputs):
    for player_obj in GAME_PLAYER_LIST:
        player_obj.update_state(game_state, game_world_state, raw_game_inputs)

def print_game_states(game_state):
    utils.print_state(game_state)
    for game_obj in GAME_OBJECT_LIST:
        game_obj.print_state()

def main_loop(game_state):
    while True:
        # Advance game clock at given framerate
        game_state[const.GAME_CLOCK].tick(30)

        # Get raw inputs and parse them into valid game inputs
        raw_game_inputs = pygame.event.get()

        # Get parsed, usable player inputs
        system_game_inputs = input_interpreter.parse_input(
            raw_game_inputs,
            GAME_SYSTEM_INPUT_CONFIG
        )

        # Apply game related input mutations to game state
        if system_game_inputs:
            utils.process_game_inputs(game_state, game_input_handler, system_game_inputs)

        # Exit the game if the player or system has requested
        if game_state[const.SHOULD_EXIT_FLAG]:
            return quit()

        if game_state[const.SHOULD_ADVANCE_FRAME]:
            # Advance to the next animation frame
            GAME_PLAYER_ONE.get_state()[const.FRAME] += 1

            update_player_states(game_state, GAME_WORLD.get_state(), raw_game_inputs)

            # Apply latest state to the game world
            GAME_WORLD.update_state(game_state, GAME_PLAYER_ONE)

            # Print game state every frame when in debug mode
            if game_state[const.IS_DEBUG_MODE_ACTIVE]:
                print_game_states(game_state)

            # Draw the screen with the most up to date game state
            game_world_surface = GAME_WORLD.get_surface(game_state, GAME_PLAYER_ONE)

            # Render game world on screen
            draw_screen(game_state, game_world_surface)

        # Stop next frame from advancing if in debug mode - allows "frame by frame" behavior
        if game_state[const.IS_DEBUG_MODE_ENABLED]:
            game_state[const.SHOULD_ADVANCE_FRAME] = not game_state[const.IS_DEBUG_MODE_ACTIVE]
