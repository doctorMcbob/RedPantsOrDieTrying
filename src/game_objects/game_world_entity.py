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
        #raise IndexError("no sprite found for player "+self.state[STATE])

    def update_movement_velocity(self, game_state, game_world_state):
        self.state[const.X_COORD] += self.state[const.VELOCITY]
        self.state[const.Y_COORD] += self.state[const.VERTICAL_VELOCITY]
        self.state[const.VERTICAL_VELOCITY] += game_world_state[const.GRAVITY]

    def update_hitbox(self):
        self.state[const.HITBOX] = self.state[const.HITBOX_CONFIG][self.state[const.STATE]]


    def apply_collision_detection(self, game_state):
        hitbox_pos, hitbox_size = self.state[const.HITBOX_CONFIG].get(self.state[const.STATE])
        self.state[const.HITBOX] = Rect((self.state[const.X_COORD] + hitbox_pos[0], self.state[const.Y_COORD] + hitbox_pos[1]), hitbox_size)

        plats = [Rect((x, y), (w, h)) for x, y, w, h, idx in game_state[const.LEVEL][const.PLATFORMS]]
        # this flag checks for a broken state where the player starts overlapped with a platform
        brokeflag = self.state[const.HITBOX].collidelist(plats) != -1

        # X axis
        if self.state[const.VELOCITY]:
            # xflag checks if we are moving
            xflag = abs(self.state[const.VELOCITY]) > 0
            direction = 1 if self.state[const.VELOCITY] < 0 else -1

            # as long as hitbox -> x velocity collides with a platform, decrement x velocity
            while self.state[const.HITBOX].move(self.state[const.VELOCITY], 0).collidelist(plats) != -1:
                self.state[const.VELOCITY] += direction

            # if the player is overlapped with a platform then the last bit will have left the x velocity
            # leaving the player right outside the platform. so shift the player by that much and set x velocity to 0
            # then update hitbox
            if brokeflag:
                self.state[const.X_COORD] += self.state[const.VELOCITY]
                self.state[const.VELOCITY] = 0
                self.state[const.HITBOX] = Rect((self.state[const.X_COORD] + hitbox_pos[0], self.state[const.Y_COORD] + hitbox_pos[1]), hitbox_size)
            # if we were moving and are no longer moving, change state to bonk
            # this logic should ideally be in the player state machine
            # but i havent thought of a good way to handle hit detection logic there
            if xflag and not self.state[const.VELOCITY]:
                if self.state[const.STATE] in [const.DIVE, const.DIVELANDJUMP]:
                    self.state[const.STATE] = const.BONK
                    self.state[const.FRAME] = 0

        # Y axis -- more or less the same
        if self.state[const.VERTICAL_VELOCITY]:
            # checks if moving vertically DOWNWARD specifically
            yflag = self.state[const.VERTICAL_VELOCITY] > 0
            direction = 1 if self.state[const.VERTICAL_VELOCITY] < 0 else -1

            # while hitbox -> y velocity collides with plat, decrement y velocity
            while self.state[const.HITBOX].move(0, self.state[const.VERTICAL_VELOCITY]).collidelist(plats) != -1:
                self.state[const.VERTICAL_VELOCITY] += direction

            # same as above but for Y axis
            if brokeflag and self.state[const.VERTICAL_VELOCITY]:
                self.state[const.Y_COORD] += self.state[const.VERTICAL_VELOCITY]
                self.state[const.VERTICAL_VELOCITY] = 1
                self.state[const.HITBOX] = Rect((self.state[const.X_COORD] + hitbox_pos[0], self.state[const.Y_COORD] + hitbox_pos[1]), hitbox_size)
                
            # this time this line will trigger if the player was moving downward and has stopped
            if yflag and not self.state[const.VERTICAL_VELOCITY]:
                # switch from most airborn states to LAND animation
                if self.state[const.STATE] in [const.FALLING, const.AIR, const.DIVELANDJUMP,
                                               const.KICKFLIP0, const.KICKFLIP1, const.KICKFLIP2]:
                    self.state[const.STATE] = const.LAND
                    self.state[const.FRAME] = 0

                # DIVE -> DIVELAND  BONK -> BONKLAND
                if self.state[const.STATE] in [const.DIVE, const.BONK]:
                    # this line is a little hacky but whatever
                    self.state[const.STATE] = const[self.state[const.STATE].value + const.LAND.value]
                    self.state[const.FRAME] = 0


        # bug in the corner
        if self.state[const.VELOCITY] and self.state[const.VERTICAL_VELOCITY]:
            # while still moving in both axis decrement both velocities
            while self.state[const.HITBOX].move(self.state[const.VELOCITY], self.state[const.VERTICAL_VELOCITY]).collidelist(plats) != -1:
                self.state[const.VELOCITY] += 1 if self.state[const.VELOCITY] < 0 else -1
                self.state[const.VERTICAL_VELOCITY] += 1 if self.state[const.VERTICAL_VELOCITY] < 0 else -1
