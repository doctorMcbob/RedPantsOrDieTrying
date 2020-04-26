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
        game_state_string = self.state[const.STATE].value
        sprites = self.state[const.SPRITE_SHEET]

        if game_state_string in sprites.keys():
            return sprites[game_state_string]

        game_frame = self.state[const.FRAME]

        while game_frame >= 0:
            current_frame = game_state_string + ":" + str(game_frame)

            if current_frame in sprites:
                return sprites[current_frame]

            game_frame -= 1

        draft = Surface((64, 64))

        draft.fill((0, 255, 0))

        font = game_state[const.FONTS][const.FONT_HELVETICA]

        draft.blit(font.render(game_state_string, 0, (0, 0, 0)), (0, 0))
        return draft

    def update_movement_velocity(self, game_state, game_world_state):
        self.state[const.X_COORD] += self.state[const.VELOCITY]
        self.state[const.Y_COORD] += self.state[const.VERTICAL_VELOCITY]
        self.state[const.VERTICAL_VELOCITY] += game_world_state[const.GRAVITY]

    def update_hitbox(self):
        self.state[const.HITBOX] = self.state[const.HITBOX_CONFIG][self.state[const.STATE]]


    def apply_platform_collision_detection(self, game_state):
        hitbox_pos, hitbox_size = self.state[const.HITBOX_CONFIG].get(self.state[const.STATE])
        self.state[const.HITBOX] = Rect((self.state[const.X_COORD] + hitbox_pos[0], self.state[const.Y_COORD] + hitbox_pos[1]), hitbox_size)

        plats = [Rect((x, y), (w, h)) for x, y, w, h, idx in game_state[const.LEVEL][const.PLATFORMS]]

        # this flag checks for a broken state where the player starts overlapped with a platform
        brokeflag = self.state[const.HITBOX].collidelist(plats) != -1
        xflag, yflag = False, False
        
        # X axis
        if self.state[const.VELOCITY]:
            direction = 1 if self.state[const.VELOCITY] < 0 else -1

            # as long as hitbox -> x velocity collides with a platform, decrement x velocity
            while self.state[const.HITBOX].move(self.state[const.VELOCITY], 0).collidelist(plats) != -1:
                xflag = True
                self.state[const.VELOCITY] += direction

            # if the player is overlapped with a platform then the last bit will have left the x velocity
            # leaving the player right outside the platform. so shift the player by that much and set x velocity to 0
            # then update hitbox
            if brokeflag:
                self.state[const.X_COORD] += self.state[const.VELOCITY]
                self.state[const.VELOCITY] = 0
                self.state[const.HITBOX] = Rect((self.state[const.X_COORD] + hitbox_pos[0], self.state[const.Y_COORD] + hitbox_pos[1]), hitbox_size)

        # Y axis
        if self.state[const.VERTICAL_VELOCITY]:
            direction = 1 if self.state[const.VERTICAL_VELOCITY] < 0 else -1

            # while hitbox -> y velocity collides with plat, decrement y velocity
            while self.state[const.HITBOX].move(0, self.state[const.VERTICAL_VELOCITY]).collidelist(plats) != -1:
                yflag = True
                self.state[const.VERTICAL_VELOCITY] += direction

            # same as above but for Y axis
            if brokeflag and self.state[const.VERTICAL_VELOCITY]:
                self.state[const.Y_COORD] += self.state[const.VERTICAL_VELOCITY]
                self.state[const.VERTICAL_VELOCITY] = 1
                self.state[const.HITBOX] = Rect((self.state[const.X_COORD] + hitbox_pos[0], self.state[const.Y_COORD] + hitbox_pos[1]), hitbox_size)
                

        # bug in the corner
        if self.state[const.VELOCITY] and self.state[const.VERTICAL_VELOCITY]:
            # while still moving in both axis decrement both velocities
            while self.state[const.HITBOX].move(self.state[const.VELOCITY], self.state[const.VERTICAL_VELOCITY]).collidelist(plats) != -1:
                self.state[const.VELOCITY] += 1 if self.state[const.VELOCITY] < 0 else -1
                self.state[const.VERTICAL_VELOCITY] += 1 if self.state[const.VERTICAL_VELOCITY] < 0 else -1

        if xflag:
            self.state[const.X_COORD] += self.state[const.VELOCITY]
            self.state[const.VELOCITY] = 0
            self.state[const.HITBOX] = Rect((self.state[const.X_COORD] + hitbox_pos[0], self.state[const.Y_COORD] + hitbox_pos[1]), hitbox_size)    
        if yflag:
            self.state[const.Y_COORD] += self.state[const.VERTICAL_VELOCITY]
            self.state[const.VERTICAL_VELOCITY] = 0
            self.state[const.HITBOX] = Rect((self.state[const.X_COORD] + hitbox_pos[0], self.state[const.Y_COORD] + hitbox_pos[1]), hitbox_size)


    def apply_hazard_collision_detection(self, game_state):
        hitbox_pos, hitbox_size = self.state[const.HITBOX_CONFIG].get(self.state[const.STATE])
        self.state[const.HITBOX] = Rect((self.state[const.X_COORD] + hitbox_pos[0], self.state[const.Y_COORD] + hitbox_pos[1]), hitbox_size)

        spikes = [Rect((x, y), (32, 32)) for x, y, d in game_state[const.LEVEL][const.SPIKES]]

        return self.state[const.HITBOX].collidelist(spikes) is not -1

        
