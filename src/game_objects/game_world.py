"""
Main game board logic
"""

import pygame

from pygame import (
    Rect,
    Surface,
)

from const import GameConstants as const

def get_board_position(state, x_pos, y_pos):
    """Get new position coordinats based off of current position coordinates and board state"""
    scroll_state = state[const.SCROLL]

    return (x_pos + scroll_state[0], y_pos + scroll_state[1])

def get_platform_surface(state, plat):
    font = state[const.FONTS][const.FONT_HELVETICA]
    surface = Surface((plat[2], plat[3]))

    surface.fill([(100, 100, 100), (200, 100, 100), (100, 200, 100), (100, 100, 200)][plat[4]])
    surface.blit(font.render("Platform", 0, (0, 0, 0)), (0, 0))

    return surface

def get_surface(state, player_one_surface):
    game_width = state[const.WIDTH]
    game_height = state[const.HEIGHT]
    player_direction = state[const.DIRECTION]
    player_x_pos = state[const.X_COORD]
    player_y_pos = state[const.Y_COORD]
    surface = Surface((game_width, game_height))

    surface.fill((255, 255, 255)) #draw background -- later

    for plat in state[const.LEVEL][const.PLATFORMS]:
        surface.blit(get_platform_surface(state, plat), get_board_position(state, plat[0], plat[1]))

    surface.blit(
        pygame.transform.flip(player_one_surface, player_direction > 0, 0),
        get_board_position(state, player_x_pos, player_y_pos)
    )

    return surface

def apply_collision_detection(state):
    #platform hit detection

    # gather hitboxes
    plats = [Rect((x, y), (w, h)) for x, y, w, h, idx in state[const.LEVEL][const.PLATFORMS]]
    pos, box = state[const.HITBOX]
    hitbox = Rect((state[const.X_COORD]+pos[0], state[const.Y_COORD]+pos[1]), box)

    brokeflag = hitbox.collidelist(plats) != -1
    
    # X axis
    if state[const.VELOCITY]:
        xflag = abs(state[const.VELOCITY]) > 0
        direction = 1 if state[const.VELOCITY] < 0 else -1
        while hitbox.move(state[const.VELOCITY], 0).collidelist(plats) != -1:
            state[const.VELOCITY] += direction

        if brokeflag:
            state[const.X_COORD] += state[const.VELOCITY]
            state[const.VELOCITY] = 0
            hitbox = Rect((state[const.X_COORD]+pos[0], state[const.Y_COORD]+pos[1]), box)
        
        if xflag and not state[const.VELOCITY]:
            if state[const.STATE] in [const.DIVE, const.DIVELANDJUMP]:
                state[const.STATE] = const.BONK
                state[const.FRAME] = 0

    
    # Y axis
    if state[const.VERTICAL_VELOCITY]:
        yflag = state[const.VERTICAL_VELOCITY] > 0
        direction = 1 if state[const.VERTICAL_VELOCITY] < 0 else -1
        while hitbox.move(0, state[const.VERTICAL_VELOCITY]).collidelist(plats) != -1:
            state[const.VERTICAL_VELOCITY] += direction

        if brokeflag:
            state[const.Y_COORD] += state[const.VERTICAL_VELOCITY]
            state[const.VERTICAL_VELOCITY] = 0
            hitbox = Rect((state[const.X_COORD]+pos[0], state[const.Y_COORD]+pos[1]), box)

        if yflag and not state[const.VERTICAL_VELOCITY]:
            if state[const.STATE] in [const.FALLING, const.AIR, const.DIVELANDJUMP]:
                state[const.STATE] = const.LAND
                state[const.FRAME] = 0

            if state[const.STATE] in [const.DIVE, const.BONK]:
                state[const.STATE] = const[state[const.STATE].value + const.LAND.value]
                state[const.FRAME] = 0

    # corner
    if state[const.VELOCITY] and state[const.VERTICAL_VELOCITY]:
        while hitbox.move(state[const.VELOCITY], state[const.VERTICAL_VELOCITY]).collidelist(plats) != -1:
            state[const.VELOCITY] += 1 if state[const.VELOCITY] < 0 else -1
            state[const.VERTICAL_VELOCITY] += 1 if state[const.VERTICAL_VELOCITY] < 0 else -1

        
def apply_state(state):
    """Update scroll state of game board to simulate movement"""
    apply_collision_detection(state)

    scroll_state = state[const.SCROLL]
    game_x_pos = state[const.X_COORD]
    game_y_pos = state[const.Y_COORD]
    board_width = state[const.WIDTH]
    board_height = state[const.HEIGHT]

    scroll_state[0] = 0 - game_x_pos + board_width / 2 - 16
    scroll_state[1] = 0 - game_y_pos + board_height / 2 - 32
