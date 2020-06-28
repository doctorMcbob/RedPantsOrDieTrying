"""
-- working on --
[x] collectables
[x] timer "rings"
[x] doors
... after doors, think about making a playable demo
[/] Enemies
\   [x] Leaper


-- Known bugs --
[] Moving Platforms
\   [x] 'warp' glitch
    ... was caused because the hitbox is not aligned with X_COORD
        changed to accomidate
    [x] phase through platforms on x axis
    [x] 'stutter' when colliding with platform
    [x] stuck in platform when platform moves up
    ... these two were fixed in game_world_entity
    []  'warp' when moving platform pushes into platform
    []  'stutter'? when in the air and a moving platform is moving twords the player
    ... causes walljump to behave differently
[] Trampolines
\   [x] entering trampoline perpendicular to bounce direction
    [x] 'multli bounce' when inside trampoline 'bouncing' every frame
    ... this fixed the perpendicular problem as well :)
    []  jump lock [GAME BREAKING]
    ... sometimes when you jump into a trampoline you get stuck in jump
        pretty rare, problably frame perfect. maybe happens when
        you get into a trampoline on the first frame out of jumpsquat
    [x]  skipping past trampoline with high velocity
    ... should be fixed in GameWorldEntity, same
        bug appears with platforms. need to rework
        hit detection.

"""
import pygame
from pygame.rect import Rect

import src.lib as lib

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
    const.TRAITS: ["TANGIBLE", "RELOAD"],
    
    const.PATH: [(const.X_COORD, const.Y_COORD)], # evaluated in level editor, when placing initially
}

TRAMPOLINE_TEMPLATE = {
    const.STATE: "trampoline",
    const.NAME: "Trampoline",
    const.X_COORD: 0,
    const.Y_COORD: 0,
    const.WIDTH: 0,
    const.HEIGHT: 0,
    const.FLAG: [],
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

DOOR_TEMPLATE = {
    const.STATE: "door",
    const.NAME: "Door",
    const.X_COORD: 0,
    const.Y_COORD: 0,
    const.WIDTH: 64,
    const.HEIGHT: 64,
    const.LEVEL: "",
    const.DROP: (0, 0),
    const.TRAITS: []
}

LEAPER_TEMPLATE = {
    const.STATE: "idle",
    const.NAME: "Leaper",
    const.X_COORD: 0,
    const.Y_COORD: 0,
    const.WIDTH: 64,
    const.HEIGHT: 32,
    const.VELOCITY: 0,
    const.VERTICAL_VELOCITY:0,
    const.COUNTER: 0,
    const.DIRECTION: 1,
    const.DISTANCE: 128,
    const.TRAITS: ["HAZARD", "GRAV", "RELOAD"],
    const.HITBOX_CONFIG: [], # TODO
    const.HITBOX: None,
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
        elif idx == 1: collider.state[const.Y_COORD] = hbox.top - cbox.height
        elif idx == 2: collider.state[const.X_COORD] = hbox.right - (cbox.width * 0.5)
        elif idx == 3: collider.state[const.X_COORD] = hbox.left - (cbox.width * 1.5)
        if idx in [0, 1]: collider.state[const.VERTICAL_VELOCITY] = 0
        if idx in [2, 3]: collider.state[const.VELOCITY] = 0

    collider.state[const.X_COORD] += self.state[const.VELOCITY]
    collider.state[const.Y_COORD] += self.state[const.VERTICAL_VELOCITY]
    collider.update_hitbox()


TRAMPOLINE_BLACKLIST = [const.IDLE, const.RUN, const.DIVELAND, const.SLIDE, const.JUMPSQUAT]

def trampoline_collision_function(self, game_state, collider):
    if collider in self.state[const.FLAG]: return
    else: self.state[const.FLAG].append(collider)
    if collider.state[const.STATE] in TRAMPOLINE_BLACKLIST: return
    if self.state[const.DIRECTION]: collider.state[const.VELOCITY] *= -1
    else: collider.state[const.VERTICAL_VELOCITY] *= -1

def trampoline_update_function(self, game_state, game_world_state):
    if self.state[const.FLAG]:
        hbox = Rect((self.state[const.X_COORD], self.state[const.Y_COORD]), (self.state[const.WIDTH], self.state[const.HEIGHT]))
        removelist = []
        for p in self.state[const.FLAG]:
            if not hbox.colliderect(p.state[const.HITBOX]):
                removelist.append(p)
        for p in removelist:
            self.state[const.FLAG].remove(p)


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
    if collider not in game_state[const.PLAYERS]: return
    self.state[const.COUNTER] = self.state[const.TIMER]
    self.state[const.IDX] += 1

def door_collision_function(self, game_state, collider):
    if collider not in game_state[const.PLAYERS]: return
    if collider.state[const.DOOR]:
        lib.level_manager.get_level(game_state, self.state[const.LEVEL])
        collider.state[const.X_COORD], collider.state[const.Y_COORD] = self.state[const.DROP]
        collider.state[const.SPAWN] = self.state[const.DROP]

def leaper_update_function(self, game_state, game_world_state):
    self.state[const.COUNTER] += 1
    if self.state[const.STATE] == "idle":
        for player in game_state[const.PLAYERS]:
            if self.state[const.X_COORD] - self.state[const.DISTANCE] <= player.state[const.X_COORD] <= self.state[const.X_COORD] + self.state[const.WIDTH] + self.state[const.DISTANCE] and self.state[const.Y_COORD] - self.state[const.DISTANCE] <= player.state[const.Y_COORD] <= self.state[const.Y_COORD] + self.state[const.HEIGHT] + self.state[const.DISTANCE]:
                self.state[const.DIRECTION] = 1 if player.state[const.X_COORD] > self.state[const.X_COORD] else -1
                self.state[const.STATE] = "leapstart"
                self.state[const.COUNTER] = 0
    if self.state[const.STATE] == "leapstart":
        if self.state[const.COUNTER] >= 5:
            self.state[const.VELOCITY] = self.state[const.DIRECTION] * 10
            self.state[const.VERTICAL_VELOCITY] = -10
            self.state[const.STATE] = "leaping"
            self.state[const.COUNTER] = 0

    flag = bool(self.state[const.VERTICAL_VELOCITY])
    self.apply_platform_collision_detection(game_state)
    if self.state[const.STATE] == "leaping" and flag and not bool(self.state[const.VERTICAL_VELOCITY]):
        self.state[const.STATE] = "idle"
        self.state[const.VELOCITY] = 0
        self.state[const.COUNTER] = 0

    self.update_movement_velocity(game_state, game_world_state)


ACTOR_FUNCTION_MAP = {
    "Moving Platform": {
        'template': MOVING_PLATFORM_TEMPLATE,
        'update': moving_platform_update_function,
        'collision': responsive_collision,
    },
    "Trampoline": {
        'template': TRAMPOLINE_TEMPLATE,
        'collision': trampoline_collision_function,
        'update': trampoline_update_function,
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
    "Door": {
        'template': DOOR_TEMPLATE,
        'collision': door_collision_function,
    },
    "Leaper": {
        'template': LEAPER_TEMPLATE,
        'update': leaper_update_function,
    },
}
