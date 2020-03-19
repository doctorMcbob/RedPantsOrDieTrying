def get_handler_from_map(input_key, handler_map):
    for valid_input_key in handler_map:
        if input_key == valid_input_key:
            return handler_map[valid_input_key]

    return False

def process_button_event(state, player_input_data, input_handler_map):
    """Handle player button press"""
    input_key = player_input_data["key"]
    input_handler = get_handler_from_map(input_key, input_handler_map)

    if input_handler:
        return input_handler(state)

    return False
