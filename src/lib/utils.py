from pygame import Rect
from src.const import GameConstants as const

def process_game_inputs(state, input_handler, game_inputs):
    for game_input in game_inputs:
        input_handler.process_input(state, game_input)

def print_state(state_dictionary):
    state_data = []

    for key in state_dictionary:
        state_data.append((key, key.value))

    state_data.sort(key=lambda x: x[1])
    print("-" * 20)

    for key_data in state_data:
        print(key_data[1], state_dictionary[key_data[0]])

def is_near(game_state, game_world, rect):
    X, Y = game_world.state[const.SCROLL]
    W, H = game_state[const.WIDTH], game_state[const.HEIGHT]
    return rect.colliderect(Rect((0-X, 0-Y), (W, H)))
