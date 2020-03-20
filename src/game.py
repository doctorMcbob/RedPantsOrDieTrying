import pygame
import src.lib.level_manager as level_manager

from src.game_objects import (
    game_world,
    player_one,
)

from src.lib.input_manager.input_handlers import (
    player_one as player_one_input_handler,
    game as game_input_handler,
)

from src.lib.sprite_manager.sprite_sheet import load_sprite_sheet
from src.lib.input_manager import input_interpreter
from const import GameConstants as const

def init_game(state):
    # pylint: disable=no-member
    pygame.init()
    # pylint: enable=no-member

    state[const.SCREEN] = pygame.display.set_mode((state[const.WIDTH], state[const.HEIGHT]))
    state[const.LEVEL] = level_manager.get_level()
    state[const.SPRITE_SHEET] = load_sprite_sheet("player")
    state[const.GAME_CLOCK] = pygame.time.Clock()

    # @TODO move to src.font_book.py
    state[const.FONTS][const.FONT_HELVETICA] = pygame.font.SysFont("Helvetica", 16)

    pygame.display.set_caption("lookin good")

    return state

# @TODO move to src.lib.utils and refactor
def print_game_state(state):
    state_data = []

    for key in state:
        state_data.append((key, key.value))

    state_data.sort(key=lambda x: x[1])
    print("-" * 20)

    for key_data in state_data:
        print(key_data[1], state[key_data[0]])

def draw_screen(state, game_world_surface):
    state[const.SCREEN].blit(game_world_surface, (0, 0))
    pygame.display.update()

def get_player_inputs():
    # Get raw inputs and parse them into valid game inputs
    raw_game_inputs = pygame.event.get()

    # @TODO split this out into controller and game system specific commands
    parsed_game_inputs = input_interpreter.parse_input(raw_game_inputs)

    return parsed_game_inputs

def process_player_inputs(state, input_handler, player_inputs):
    for player_input in player_inputs:
        input_handler.process_input(state, player_input)

def main_loop(state):
    while True:
        # Advance game clock at given framerate
        state[const.GAME_CLOCK].tick(30)

        # Get parsed, usable player inputs
        player_inputs = get_player_inputs()

        # Apply game related input mutations to game state
        if player_inputs:
            process_player_inputs(state, game_input_handler, player_inputs)

        # Exit the game if the player or system has requested
        if state[const.SHOULD_EXIT_FLAG]:
            return quit()

        # Apply player related input mutations to game state
        if player_inputs:
            process_player_inputs(state, player_one_input_handler, player_inputs)

        if state[const.SHOULD_ADVANCE_FRAME]:
            # Advance to the next animation frame
            state[const.FRAME] += 1

            # Apply latest state to player one
            player_one.apply_state(state)

            # Apply latest state to the game world
            game_world.apply_state(state)

            # Print game state every frame when in debug mode
            if state[const.IS_DEBUG_MODE_ACTIVE]:
                print_game_state(state)

            # Get player one character surface to put into game world
            player_one_surface = player_one.get_surface(state)

            # Draw the screen with the most up to date game state
            game_world_surface = game_world.get_surface(state, player_one_surface)

            # Render game world on screen
            draw_screen(state, game_world_surface)

        # Stop next frame from advancing if in debug mode - allows "frame by frame" behavior
        if state[const.IS_DEBUG_MODE_ENABLED]:
            state[const.SHOULD_ADVANCE_FRAME] = not state[const.IS_DEBUG_MODE_ACTIVE]
