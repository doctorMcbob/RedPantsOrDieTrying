from pygame import Surface
from const import GameConstants as const

def update_movement_velocity(state):
    state[const.X_COORD] += state[const.VELOCITY]
    state[const.Y_COORD] += state[const.VERTICAL_VELOCITY]
    state[const.VERTICAL_VELOCITY] += state[const.GRAVITY]

def apply_slide_state(state):
    if state[const.VELOCITY] == 0:
        state[const.STATE] = const.IDLE
        state[const.FRAME] = 0
    elif state[const.VELOCITY] < 5:
        state[const.FRAME] = 1
    else:
        state[const.FRAME] = 0

def apply_land_state(state):
    if state[const.FRAME] == state[const.LANDING_FRAME]:
        state[const.STATE] = const.IDLE if state[const.MOVE] * state[const.VELOCITY] >= 0 else const.SLIDE
        state[const.FRAME] = 0

def apply_idle_state(state):
    if state[const.MOVE]:
        state[const.DIRECTION] = state[const.MOVE]
        state[const.STATE] = const.RUN
        state[const.FRAME] = 0
    elif state[const.VELOCITY]:
        state[const.STATE] = const.SLIDE

def apply_run_state(state):
    state[const.FRAME] = state[const.FRAME] % 30
    state[const.VELOCITY] = state[const.SPEED] * state[const.DIRECTION]

    if state[const.MOVE] != state[const.DIRECTION]:
        state[const.STATE] = const.SLIDE
        state[const.FRAME] = 0

def apply_traction_state(state):
    if state[const.VELOCITY] > 0:
        state[const.VELOCITY] = max(state[const.VELOCITY] - state[const.TRACTION], 0)
    else:
        state[const.VELOCITY] = min(state[const.VELOCITY] + state[const.TRACTION], 0)

MOTION_STATE_HANDLER_MAP = {
    const.SLIDE: apply_slide_state,
    const.IDLE: apply_idle_state,
    const.RUN: apply_run_state,
    const.LAND: apply_land_state,
}

def update_motion_state(state):
    player_motion_state = state[const.STATE]
    motion_state_handler = MOTION_STATE_HANDLER_MAP.get(player_motion_state)

    if motion_state_handler:
        motion_state_handler(state)

TRACTION_STATE_BLACKLIST = [const.RISING, const.AIR, const.FALLING, const.FASTFALLING,
                            const.DIVE, const.DIVELANDJUMP, const.KICKFLIP0,
                            const.KICKFLIP1, const.KICKFLIP2]

def update_traction_state(state):
    player_motion_state = state[const.STATE]

    if player_motion_state not in TRACTION_STATE_BLACKLIST:
        apply_traction_state(state)

JUMPSQUAT_BLACKLIST = [
    const.RISING, const.AIR, const.FALLING,
    const.FASTFALLING, const.DIVE, const.DIVESTART,
    const.DIVELAND, const.DIVELANDJUMP, const.BONK,
    const.KICKFLIP0, const.KICKFLIP1, const.KICKFLIP2,
]

JUMP_START_MOTION_STATE_BLACKLIST = [const.DIVE, const.DIVELANDJUMP, const.BONK,
                                     const.KICKFLIP0, const.KICKFLIP1, const.KICKFLIP2]

def update_kickflip_state(state):
    if state[const.STATE] == const.SLIDE and state[const.JUMP] and state[const.MOVE] != state[const.DIRECTION]:
        state[const.STATE] = const.KICKFLIP0
        state[const.FRAME] = 0

        state[const.VERTICAL_VELOCITY] = state[const.KICKFLIPSTR]
        state[const.DIRECTION] *= -1
        state[const.VELOCITY] = state[const.DIRECTION] * 5

    if state[const.STATE] == const.KICKFLIP0 and state[const.VERTICAL_VELOCITY] >= state[const.KICKFLIPLIMIT]:
        state[const.STATE] = const.KICKFLIP1
        state[const.FRAME] = 0

    if state[const.STATE] in [const.KICKFLIP0, const.KICKFLIP1] and state[const.VERTICAL_VELOCITY] > 0:
        state[const.STATE] = const.KICKFLIP2
        state[const.FRAME] = 0

def update_jump_state(state):
    is_starting_squat = state[const.JUMP] and state[const.STATE] not in JUMPSQUAT_BLACKLIST

    if is_starting_squat:
        state[const.STATE] = const.JUMPSQUAT
        state[const.FRAME] = 0

    is_starting_jump = state[const.STATE] == const.JUMPSQUAT and state[const.FRAME] >= state[const.JUMP_SQUAT_FRAME]

    if is_starting_jump:
        state[const.VERTICAL_VELOCITY] += state[const.JUMP_SPEED]

    is_jumping = state[const.STATE] not in JUMP_START_MOTION_STATE_BLACKLIST
    
    if is_jumping:
        if abs(state[const.VERTICAL_VELOCITY]) > state[const.GRAVITY]:
            state[const.STATE] = const.AIR
            state[const.FRAME] = 0

        if state[const.VERTICAL_VELOCITY] < -state[const.AIR]:
            state[const.STATE] = const.RISING
            state[const.FRAME] = 0

        if state[const.VERTICAL_VELOCITY] > state[const.AIR]:
            state[const.STATE] = const.FALLING
            state[const.FRAME] = 0

def update_falling_state(state):
    is_falling = state[const.STATE] == const.AIR and state[const.MOVE]

    if is_falling:
        if abs(state[const.VELOCITY] + state[const.DRIFT] * state[const.MOVE]) <= state[const.SPEED]:
            state[const.VELOCITY] += state[const.DRIFT] * state[const.MOVE]
        if state[const.VELOCITY]:
            state[const.DIRECTION] = state[const.MOVE] if state[const.MOVE] else state[const.DIRECTION]

    is_flipping = state[const.STATE] in [const.KICKFLIP1, const.KICKFLIP2]

    if is_flipping:
        if state[const.MOVE] == state[const.DIRECTION]:
            if abs(state[const.VELOCITY] + state[const.DRIFT] * state[const.MOVE]) <= state[const.SPEED]:
                state[const.VELOCITY] += state[const.DRIFT] * state[const.MOVE]
            
def update_dive_state(state):
    is_starting_dive = state[const.STATE] == const.AIR and state[const.DIVE]

    if is_starting_dive:
        state[const.STATE] = const.DIVESTART
        state[const.FRAME] = 0

    is_diving = state[const.STATE] == const.DIVESTART

    if is_diving:
        state[const.VERTICAL_VELOCITY] = 0
        if state[const.FRAME] > state[const.DSTARTF]:
            state[const.STATE] = const.DIVE
            state[const.FRAME] = 0
            state[const.VELOCITY] = state[const.DIVESTR] * state[const.DIRECTION]

    is_landing = state[const.STATE] == const.DIVELAND

    if is_landing:
        if state[const.VELOCITY] == 0:
            state[const.STATE] = const.IDLE
            state[const.FRAME] = 0

        if state[const.JUMP]:
            state[const.VERTICAL_VELOCITY] = state[const.DIVELJSTR]
            state[const.STATE] = const.DIVELANDJUMP
            state[const.FRAME] = 0

def update_bonk_state(state):
    is_bonking = state[const.STATE] == const.BONK and state[const.FRAME] <= 1
        
    if is_bonking:
        state[const.VELOCITY] = -10 * state[const.DIRECTION]

    has_bonked = state[const.STATE] == const.BONKLAND and state[const.FRAME] >= state[const.BONKLF]

    if has_bonked:
        state[const.STATE] = const.IDLE
        state[const.FRAME] = 0

def reset_jump_and_dive_flags(state):
    state[const.DIVE] = 0
    state[const.JUMP] = 0

HITBOX_STATE_DATA = {const.DIVELAND: ((0, 32), (64, 32))}

for s in [const.DIVE, const.DIVELANDJUMP,
          const.KICKFLIP0, const.KICKFLIP1, const.KICKFLIP2]:
    HITBOX_STATE_DATA[s] = ((0, 0), (64, 64))

for s in [const.IDLE, const.RUN, const.SLIDE, const.JUMPSQUAT,
          const.RISING, const.LAND, const.BONK, const.BONKLAND,
          const.FALLING, const.AIR, const.DIVESTART]:
    HITBOX_STATE_DATA[s] = ((16, 0), (32, 64))


def update_hitbox(state):
    state[const.HITBOX] = HITBOX_STATE_DATA[state[const.STATE]]

def apply_state(state):
    update_hitbox(state)
    update_movement_velocity(state)
    update_motion_state(state)
    update_traction_state(state)

    update_kickflip_state(state)
    update_jump_state(state)
    update_falling_state(state)
    update_dive_state(state)
    update_bonk_state(state)

    reset_jump_and_dive_flags(state)

def get_surface(state):
    game_state_string = state[const.STATE].value
    sprites = state[const.SPRITE_SHEET]

    if game_state_string in sprites.keys():
        return sprites[game_state_string]

    game_frame = state[const.FRAME]

    while game_frame >= 0:
        current_frame = game_state_string + ":" + str(game_frame)

        if current_frame in sprites:
            return sprites[current_frame]

        game_frame -= 1

    draft = Surface((64, 64))

    draft.fill((0, 255, 0))

    font = state[const.FONTS][const.FONT_HELVETICA]

    draft.blit(font.render(game_state_string, 0, (0, 0, 0)), (0, 0))

    return draft
    #raise IndexError("no sprite found for player "+state[STATE])
