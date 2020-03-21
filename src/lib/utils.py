def process_game_inputs(state, input_handler, game_inputs):
    for game_input in game_inputs:
        input_handler.process_input(state, game_input)
