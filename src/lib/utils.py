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
