import pygame
from pygame.rect import Rect

from src.const import GameConstants as const

from math import sqrt

MOVING_PLATFORM_TEMPLATE = {
    const.STATE: "platform",
    const.NAME: "Moving Platform",
    const.X_COORD: 0,
    const.Y_COORD: 0,
    const.WIDTH: 0,
    const.HEIGHT: 0,
    const.VELOCITY: 0,
    const.VERTICAL_VELOCITY: 0,
    const.COUNTER: 0,
    const.SPEED: 1,
    const.TRAITS: ["TANGIBLE"],
    
    const.PATH: [(const.X_COORD, const.Y_COORD)], # evaluated in level editor, when placing initially
}

def moving_platform_update_function(self, game_state, game_world_state):
    X, Y = round(self.state[const.X_COORD]), round(self.state[const.Y_COORD])
    X_, Y_ = self.state[const.PATH][self.state[const.COUNTER]]
    if (X, Y) == (X_, Y_): self.state[const.COUNTER] = (self.state[const.COUNTER] + 1) % len(self.state[const.PATH])
    if X < X_: self.state[const.VELOCITY] = min(self.state[const.SPEED], abs(X_ - X))
    if X > X_: self.state[const.VELOCITY] = min(-self.state[const.SPEED], abs(X_ - X))
    if X == X_: self.state[const.VELOCITY] = 0
    if Y < Y_: self.state[const.VERTICAL_VELOCITY] = min(self.state[const.SPEED], abs(Y_ - Y))
    if Y > Y_: self.state[const.VERTICAL_VELOCITY] = min(-self.state[const.SPEED], abs(Y_ - Y))
    if Y == Y_: self.state[const.VERTICAL_VELOCITY] = 0
    self.update_movement_velocity(game_state, game_world_state)
    
def responsive_collision(self, game_state, collider):
    hbox = Rect((self.state[const.X_COORD], self.state[const.Y_COORD]), (self.state[const.WIDTH], self.state[const.HEIGHT]))
    cbox = collider.state[const.HITBOX]
    if cbox.colliderect(hbox):
        val = None
        idx = 0
        for i, value in enumerate([abs(cbox.top - hbox.bottom),
                                   abs(cbox.bottom - hbox.top),
                                   abs(cbox.left - hbox.right),
                                   abs(cbox.right - hbox.left)]):
            if val is None or val > value:
                val = value
                idx = i
        if idx == 0: collider.state[const.Y_COORD] = hbox.bottom
        if idx == 1: collider.state[const.Y_COORD] = hbox.top - cbox.height
        if idx == 2: collider.state[const.X_COORD] = hbox.right
        if idx == 3: collider.state[const.X_COORD] = hbox.left - cbox.width
    else:
        collider.state[const.X_COORD] += self.state[const.VELOCITY]
        collider.state[const.Y_COORD] += self.state[const.VERTICAL_VELOCITY]
    collider.update_hitbox()


ACTOR_FUNCTION_MAP = {
    "Moving Platform": {
        'template': MOVING_PLATFORM_TEMPLATE,
        'update': moving_platform_update_function,
        'collision': responsive_collision,
    }
}
