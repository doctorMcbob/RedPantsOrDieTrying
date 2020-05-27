"""
-- working on --
[x] collectables
[] timer "rings"
[] doors

-- Known bugs --
[] Moving Platforms
\   [] 'warp' glitch
    ... happens when walking into a moving platform,
        causes X axis collision with platform below player
        warping the player to the end of the platform
    [] 'stutter' when colliding with platform
    ... not sure about solving this one
[] Trampolines
\   [] entering trampoline perpendicular to bounce direction
    [] skipping past trampoline with high velocity
    ... should be fixed in GameWorldEntity, same
        bug appears with platforms

"""
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

TRAMPOLINE_TEMPLATE = {
    const.STATE: "trampoline",
    const.NAME: "Trampoline",
    const.X_COORD: 0,
    const.Y_COORD: 0,
    const.WIDTH: 0,
    const.HEIGHT: 0,
    const.DIRECTION: 0, # vertical if true else horizontal
    const.TRAITS: [],
}

COLLECTABLE_TEMPLATE = {
    # can be set to 'banana' or 'cheese' or whatever biome
    const.STATE: "coin",
    const.NAME: "Collectable",
    const.X_COORD: 0,
    const.Y_COORD: 0,
    const.WIDTH: 32,
    const.HEIGHT: 32,
    const.TRAITS: [],
}

TIMER_RINGS_TEMPLATE = {
    const.STATE: "ring",
    const.NAME: "Ring",
    const.COUNTER: 0,
    const.TIMER: 100,
    const.IDX: 0,
    const.X_COORD: 0,
    const.Y_COORD: 0,
    const.WIDTH: 32,
    const.HEIGHT: 128,
    const.PATH: [(const.X_COORD, const.Y_COORD)],
    const.TRAITS: [],
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
        if idx == 1: collider.state[const.Y_COORD] = hbox.top - cbox.height - 5 # HACKY AF
        if idx == 2: collider.state[const.X_COORD] = hbox.right
        if idx == 3: collider.state[const.X_COORD] = hbox.left - cbox.width
    else:
        collider.state[const.X_COORD] += self.state[const.VELOCITY]
        collider.state[const.Y_COORD] += self.state[const.VERTICAL_VELOCITY]
    collider.update_hitbox()
    print(collider.state[const.X_COORD], collider.state[const.Y_COORD])


def trampoline_collision_function(self, game_state, collider):
    if self.state[const.DIRECTION]: collider.state[const.VELOCITY] *= -1
    else: collider.state[const.VERTICAL_VELOCITY] *= -1

def collectable_collision_function(self, game_state, collider):
    if self.state[const.STATE] in collider.inventory:
        collider.inventory[self.state[const.STATE]] += 1
    else:
        collider.inventory[self.state[const.STATE]] = 1
    game_state[const.LOADED_ACTORS].remove(self)

def timer_rings_update_function(self, game_state, game_world_state):
    
    if self.state[const.IDX] >= len(self.state[const.PATH]):
        # Figure out what to put here
        print("ZOINKS SCOOB")
        game_state[const.LOADED_ACTORS].remove(self)
        return

    self.state[const.X_COORD], self.state[const.Y_COORD] = self.state[const.PATH][self.state[const.IDX]]
    if self.state[const.IDX] != 0:
        self.state[const.COUNTER] -= 1
    if self.state[const.COUNTER] <= 0:
        self.state[const.IDX] = 0
        self.state[const.COUNTER] = self.state[const.TIMER]

def timer_rings_collision_function(self, game_state, collider):
    self.state[const.COUNTER] = self.state[const.TIMER]
    self.state[const.IDX] += 1

ACTOR_FUNCTION_MAP = {
    "Moving Platform": {
        'template': MOVING_PLATFORM_TEMPLATE,
        'update': moving_platform_update_function,
        'collision': responsive_collision,
    },
    "Trampoline": {
        'template': TRAMPOLINE_TEMPLATE,
        'collision': trampoline_collision_function,
    },
    "Collectable": {
        'template': COLLECTABLE_TEMPLATE,
        'collision': collectable_collision_function,
    },
    "Timer Rings": {
        'template': TIMER_RINGS_TEMPLATE,
        'update': timer_rings_update_function,
        'collision': timer_rings_collision_function,
    },
}
