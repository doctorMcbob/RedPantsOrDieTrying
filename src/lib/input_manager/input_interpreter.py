from const import InputConstants as const

def parse_input_event_type(player_input, input_config):
    """Determine if an input was a button press or a button release"""
    player_input_type = player_input.type

    if player_input_type == input_config[const.BUTTON_PRESSED]:
        return const.BUTTON_PRESSED

    if player_input_type == input_config[const.BUTTON_RELEASED]:
        return const.BUTTON_RELEASED

    return False

def parse_input_event_key(player_input, input_config):
    """Get any valid command data from a button press"""
    player_input_key = player_input.key

    for i, input_key in enumerate(input_config.values()):
        if player_input_key == input_key:
            return list(input_config.keys())[i]

    return False

def parse_input(player_inputs, input_config):
    """Gather user inputs and check them against the input configuration"""
    parsed_inputs = []

    # Iterate through inputs and apply proper control behaviors if necessary
    for player_input in player_inputs:
        input_event_type = parse_input_event_type(player_input, input_config)

        if input_event_type:
            input_event_key = parse_input_event_key(player_input, input_config)

            if input_event_key:
                parsed_inputs.append({"type": input_event_type, "key": input_event_key})

    return parsed_inputs
