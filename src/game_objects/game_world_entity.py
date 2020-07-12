import pygame
from pygame import (
    Rect,
    Surface,
)

from src.const import GameConstants as const

from src.game_objects.game_object import GameObject
from src.lib.sprite_manager.sprite_sheet import load_sprite_sheet


# @TODO handle missing sprite key
class GameWorldEntity(GameObject):
    def __init__(self, state_template, sprite_key, hitbox_config):
        super(GameWorldEntity, self).__init__(state_template)

        self.state[const.SPRITE_SHEET_KEY] = sprite_key
        self.state[const.HITBOX_CONFIG] = hitbox_config
        self.state[const.HITBOX] = False

    def initialize(self):
        self.state[const.SPRITE_SHEET] = load_sprite_sheet(self.state[const.SPRITE_SHEET_KEY])

    def get_surface(self, game_state):
        if const.SPRITE_SHEET in self.state:
            game_state_string = self.state[const.STATE] if type(self.state[const.STATE]) is not const else self.state[const.STATE].value
            sprites = self.state[const.SPRITE_SHEET]

            if game_state_string in sprites.keys():
                return sprites[game_state_string]

            elif const.FRAME in self.state:
                game_frame = self.state[const.FRAME]

                while game_frame >= 0:
                    current_frame = game_state_string + ":" + str(game_frame)

                    if current_frame in sprites:
                        return sprites[current_frame]

                    game_frame -= 1
            
        game_state_string = self.state[const.NAME]
        
        draft = Surface((
            self.state[const.WIDTH],
            self.state[const.HEIGHT]))
        
        draft.fill((0, 255, 0))

        font = game_state[const.FONTS][const.FONT_HELVETICA]
        
        draft.blit(font.render(game_state_string, 0, (0, 0, 0)), (0, 0))
        return draft

    def update_movement_velocity(self, game_state, game_world_state):
        self.state[const.X_COORD] += self.state[const.VELOCITY]
        self.state[const.Y_COORD] += self.state[const.VERTICAL_VELOCITY]
        if const.TRAITS not in self.state or const.GRAVITY.value in self.state[const.TRAITS]:
            self.state[const.VERTICAL_VELOCITY] += game_world_state[const.GRAVITY]

    def update_hitbox(self):
        if self.state[const.STATE] in self.state[const.HITBOX_CONFIG]:
            hitbox_pos, hitbox_size = self.state[const.HITBOX_CONFIG].get(self.state[const.STATE])
        else:
            hitbox_pos = (0, 0)
            hitbox_size = (self.state[const.WIDTH], self.state[const.HEIGHT])
        self.state[const.HITBOX] = Rect((self.state[const.X_COORD] + hitbox_pos[0], self.state[const.Y_COORD] + hitbox_pos[1]), hitbox_size)


    def apply_platform_collision_detection(self, game_state):
        self.update_hitbox()

        # gather everything to check
        
        # platforms
        plats = [Rect((x, y), (w, h)) for x, y, w, h, idx in game_state[const.LEVEL][const.PLATFORMS]]

        # map for collision functions
        tang_map = list(filter(lambda actor: 'TANGIBLE' in actor.state[const.TRAITS], game_state[const.LOADED_ACTORS]))
        if self in tang_map: tang_map.remove(self)
        non_tang_map = list(filter(lambda actor: 'TANGIBLE' not in actor.state[const.TRAITS], game_state[const.LOADED_ACTORS]))
        if self in non_tang_map: non_tang_map.remove(self)

        # actors
        tangibles = [Rect((actor.state[const.X_COORD], actor.state[const.Y_COORD]),
                          (actor.state[const.WIDTH], actor.state[const.HEIGHT]))
                     for actor in tang_map]
        non_tangibles = [Rect((actor.state[const.X_COORD], actor.state[const.Y_COORD]),
                              (actor.state[const.WIDTH], actor.state[const.HEIGHT]))
                         for actor in non_tang_map]
        
        # check if we are currently colliding with an actor, if so, resolve collision function  
        hit = self.state[const.HITBOX].collidelist(tangibles)
        if hit != -1: tang_map[hit].collision_function(tang_map[hit], game_state, self)
        hit = self.state[const.HITBOX].collidelist(non_tangibles)
        if hit != -1: non_tang_map[hit].collision_function(non_tang_map[hit], game_state, self)

        hit = self.state[const.HITBOX].collidelist(plats + tangibles)
        if hit != -1 and self.state[const.STATE] != const.DMG:
            self.state[const.STATE] = const.DMG
            self.state[const.FRAME] = 0

        # X axis
        if self.state[const.VELOCITY]:
            direction = 1 if self.state[const.VELOCITY] < 0 else -1

            w = self.state[const.HITBOX].w
            for n in range(self.state[const.VELOCITY] // w):
                if self.state[const.HITBOX].move(w * n, 0).collidelist(plats + tangibles) != -1:
                    self.state[const.VELOCITY] = (w * n) + (self.state[const.VELOCITY] % w)
                    break
            
            i = self.state[const.HITBOX].move(self.state[const.VELOCITY], 0).collidelist(tangibles)
            if i != -1: tang_map[i].collision_function(tang_map[i], game_state, self)
            # as long as hitbox -> x velocity collides with a platform, decrement x velocity
            while self.state[const.HITBOX].move(self.state[const.VELOCITY], 0).collidelist(plats + tangibles) != -1:
                self.state[const.VELOCITY] += direction

        # Y axis
        if self.state[const.VERTICAL_VELOCITY]:
            direction = 1 if self.state[const.VERTICAL_VELOCITY] < 0 else -1

            h = self.state[const.HITBOX].h
            for n in range(self.state[const.VERTICAL_VELOCITY] // h):
                if self.state[const.HITBOX].move(0, h * n).collidelist(plats + tangibles) != -1:
                    self.state[const.VERTICAL_VELOCITY] = (h * n) + (self.state[const.VERTICAL_VELOCITY] % h)
                    break

            i = self.state[const.HITBOX].move(0, self.state[const.VERTICAL_VELOCITY]).collidelist(tangibles)
            # while hitbox -> y velocity collides with plat, decrement y velocity
            while self.state[const.HITBOX].move(0, self.state[const.VERTICAL_VELOCITY]).collidelist(plats + tangibles) != -1:
                self.state[const.VERTICAL_VELOCITY] += direction
            if i != -1: tang_map[i].collision_function(tang_map[i], game_state, self)


        if self.state[const.VERTICAL_VELOCITY] and self.state[const.VELOCITY]:
            while self.state[const.HITBOX].move(
                    self.state[const.VELOCITY], self.state[const.VERTICAL_VELOCITY]).collidelist(plats + tangibles) != -1:
                self.state[const.VELOCITY] += 1 if self.state[const.VELOCITY] < 0 else -1
                self.state[const.VERTICAL_VELOCITY] += 1 if self.state[const.VERTICAL_VELOCITY] < 0 else -1

            
        self.update_hitbox()
            
    def apply_hazard_collision_detection(self, game_state):
        hitbox_pos, hitbox_size = self.state[const.HITBOX_CONFIG].get(self.state[const.STATE])
        self.state[const.HITBOX] = Rect((self.state[const.X_COORD] + hitbox_pos[0], self.state[const.Y_COORD] + hitbox_pos[1]), hitbox_size)

        spikes = [Rect((x, y), (32, 32)) for x, y, d in game_state[const.LEVEL][const.SPIKES]]
        hazard_actors = list(filter(lambda actor: 'HAZARD' in actor.state[const.TRAITS], game_state[const.LOADED_ACTORS]))
        if self in hazard_actors: hazard_actors.remove(self)
        hazards = [Rect(
            (actor.state[const.X_COORD], actor.state[const.Y_COORD]),
            (actor.state[const.WIDTH], actor.state[const.HEIGHT])
        ) for actor in hazard_actors]
        
        return self.state[const.HITBOX].collidelist(spikes + hazards) is not -1

        
