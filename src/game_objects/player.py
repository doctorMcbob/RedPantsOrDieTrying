from pygame import (
    Rect,
    Surface,
)

from const import GameConstants as const
from src.game_objects.game_object import GameObject
from src.lib import utils

from src.lib.sprite_manager.sprite_sheet import load_sprite_sheet
from src.lib.input_manager.input_handlers import player as input_handler
from src.game_data_templates.input_config import (
    INPUT_CONFIG_TEMPLATE,
)

MID_AIR_MOTION_STATE_WHITELIST = [
    const.RISING, const.AIR, const.FALLING,
    const.FASTFALLING, const.DIVE, const.DIVESTART,
    const.DIVELAND, const.DIVELANDJUMP, const.BONK,
]

JUMP_START_MOTION_STATE_BLACKLIST = [const.DIVE, const.DIVELANDJUMP, const.BONK]
TRACTION_STATE_BLACKLIST = [const.RISING, const.AIR, const.FALLING, const.FASTFALLING, const.DIVE]

class Player(GameObject):
    def __init__(self, player_state_template):
        super(Player, self).__init__(player_state_template)

        self.state["input_config"] = INPUT_CONFIG_TEMPLATE.copy()
        self.motion_state_handlers = {
            const.SLIDE: self.apply_slide_state,
            const.IDLE: self.apply_idle_state,
            const.RUN: self.apply_run_state,
            const.LAND: self.apply_land_state,
        }

    def initialize(self):
        self.state[const.SPRITE_SHEET] = load_sprite_sheet("player")

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state

        return self.get_state()

    def update_movement_velocity(self, game_state, game_world_state):
        self.state[const.X_COORD] += self.state[const.VELOCITY]
        self.state[const.Y_COORD] += self.state[const.VERTICAL_VELOCITY]
        self.state[const.VERTICAL_VELOCITY] += game_world_state[const.GRAVITY]

    def apply_slide_state(self):
        if self.state[const.VELOCITY] == 0:
            self.state[const.STATE] = const.IDLE
            self.state[const.FRAME] = 0
        elif self.state[const.VELOCITY] < 5:
            self.state[const.FRAME] = 1
        else:
            self.state[const.FRAME] = 0

    def apply_land_state(self):
        if self.state[const.FRAME] == self.state[const.LANDING_FRAME]:
            self.state[const.STATE] = const.IDLE
            self.state[const.FRAME] = 0

    def apply_idle_state(self):
        if self.state[const.MOVE]:
            self.state[const.DIRECTION] = self.state[const.MOVE]
            self.state[const.STATE] = const.RUN
            self.state[const.FRAME] = 0
        elif self.state[const.VELOCITY]:
            self.state[const.STATE] = const.SLIDE

    def apply_run_state(self):
        self.state[const.FRAME] = self.state[const.FRAME] % 30
        self.state[const.VELOCITY] = self.state[const.SPEED] * self.state[const.DIRECTION]

        if self.state[const.MOVE] != self.state[const.DIRECTION]:
            self.state[const.STATE] = const.SLIDE
            self.state[const.FRAME] = 0

    def apply_traction_state(self):
        if self.state[const.VELOCITY] > 0:
            self.state[const.VELOCITY] = max(self.state[const.VELOCITY] - self.state[const.TRACTION], 0)
        else:
            self.state[const.VELOCITY] = min(self.state[const.VELOCITY] + self.state[const.TRACTION], 0)

    def update_motion_state(self):
        player_motion_state = self.state[const.STATE]
        motion_state_handlers = self.motion_state_handlers.get(player_motion_state)

        if motion_state_handlers:
            motion_state_handlers()

    def update_traction_state(self):
        player_motion_state = self.state[const.STATE]

        if player_motion_state not in TRACTION_STATE_BLACKLIST:
            self.apply_traction_state()

    def update_jump_state(self, game_state, game_world_state):
        is_starting_squat = self.state[const.JUMP] and self.state[const.STATE] not in MID_AIR_MOTION_STATE_WHITELIST

        if is_starting_squat:
            self.state[const.STATE] = const.JUMPSQUAT
            self.state[const.FRAME] = 0

        is_starting_jump = self.state[const.STATE] == const.JUMPSQUAT and self.state[const.FRAME] >= self.state[const.JUMP_SQUAT_FRAME]

        if is_starting_jump:
            self.state[const.VERTICAL_VELOCITY] += self.state[const.JUMP_SPEED]

        is_jumping = self.state[const.STATE] not in JUMP_START_MOTION_STATE_BLACKLIST

        if is_jumping:
            if abs(self.state[const.VERTICAL_VELOCITY]) > game_world_state[const.GRAVITY]:
                self.state[const.STATE] = const.AIR
                self.state[const.FRAME] = 0

            if self.state[const.VERTICAL_VELOCITY] < -self.state[const.AIR]:
                self.state[const.STATE] = const.RISING
                self.state[const.FRAME] = 0

            if self.state[const.VERTICAL_VELOCITY] > self.state[const.AIR]:
                self.state[const.STATE] = const.FALLING
                self.state[const.FRAME] = 0

    def update_falling_state(self):
        is_falling = self.state[const.STATE] == const.AIR and self.state[const.MOVE] or self.state[const.MOVE] == const.DIVELANDJUMP

        if is_falling:
            if abs(self.state[const.VELOCITY] + self.state[const.DRIFT] * self.state[const.MOVE]) <= self.state[const.SPEED]:
                self.state[const.VELOCITY] += self.state[const.DRIFT] * self.state[const.MOVE]
            if self.state[const.VELOCITY]:
                self.state[const.DIRECTION] = self.state[const.MOVE] if self.state[const.MOVE] else self.state[const.DIRECTION]

    def update_dive_state(self):
        is_starting_dive = self.state[const.STATE] == const.AIR and self.state[const.DIVE]

        if is_starting_dive:
            self.state[const.STATE] = const.DIVESTART
            self.state[const.FRAME] = 0

        is_diving = self.state[const.STATE] == const.DIVESTART

        if is_diving:
            self.state[const.VERTICAL_VELOCITY] = 0
            if self.state[const.FRAME] > self.state[const.DSTARTF]:
                self.state[const.STATE] = const.DIVE
                self.state[const.FRAME] = 0
                self.state[const.VELOCITY] = self.state[const.DIVESTR] * self.state[const.DIRECTION]

        is_landing = self.state[const.STATE] == const.DIVELAND

        if is_landing:
            if self.state[const.VELOCITY] == 0:
                self.state[const.STATE] = const.IDLE
                self.state[const.FRAME] = 0

            if self.state[const.JUMP]:
                self.state[const.VERTICAL_VELOCITY] = self.state[const.DIVELJSTR]
                self.state[const.STATE] = const.DIVELANDJUMP
                self.state[const.FRAME] = 0

    def update_bonk_state(self):
        is_bonking = self.state[const.STATE] == const.BONK and self.state[const.FRAME] == 1

        if is_bonking:
            self.state[const.VELOCITY] = -10 * self.state[const.DIRECTION]

        has_bonked = self.state[const.STATE] == const.BONKLAND and self.state[const.FRAME] >= self.state[const.BONKLF]

        if has_bonked:
            self.state[const.STATE] = const.IDLE
            self.state[const.FRAME] = 0

    def reset_jump_and_dive_flags(self):
        self.state[const.DIVE] = 0
        self.state[const.JUMP] = 0

    def update_controls(self, new_input_config):
        self.state["input_config"] = new_input_config

    def update_state(self, game_state, game_world_state, game_inputs):
        if game_inputs:
            utils.process_game_inputs(self.state, input_handler, game_inputs)

        self.update_movement_velocity(game_state, game_world_state)
        self.update_motion_state()
        self.update_traction_state()
        self.update_jump_state(game_state, game_world_state)
        self.update_falling_state()
        self.update_dive_state()
        self.update_bonk_state()
        self.reset_jump_and_dive_flags()
        self.apply_collision_detection(game_state)

    def apply_collision_detection(self, game_state):
        self.state[const.HITBOX] = Rect((self.state[const.X_COORD]+16, self.state[const.Y_COORD]), (32, 64))

        plats = [Rect((x, y), (w, h)) for x, y, w, h, idx in game_state[const.LEVEL][const.PLATFORMS]]

        if self.state[const.VELOCITY]:
            xflag = abs(self.state[const.VELOCITY]) > 0
            while self.state[const.HITBOX].move(self.state[const.VELOCITY], 0).collidelist(plats) != -1:
                self.state[const.VELOCITY] += 1 if self.state[const.VELOCITY] < 0 else -1
            if xflag and not self.state[const.VELOCITY]:
                if self.state[const.STATE] in [const.DIVE, const.DIVELANDJUMP]:
                    self.state[const.STATE] = const.BONK
                    self.state[const.FRAME] = 0

        if self.state[const.VERTICAL_VELOCITY]:
            yflag = self.state[const.VERTICAL_VELOCITY] > 0
            while self.state[const.HITBOX].move(0, self.state[const.VERTICAL_VELOCITY]).collidelist(plats) != -1:
                self.state[const.VERTICAL_VELOCITY] += 1 if self.state[const.VERTICAL_VELOCITY] < 0 else -1
            if yflag and not self.state[const.VERTICAL_VELOCITY]:
                # i dont love changing the state here but it seems fine
                if self.state[const.STATE] in [const.FALLING, const.AIR, const.DIVELANDJUMP]:
                    self.state[const.STATE] = const.LAND
                    self.state[const.FRAME] = 0
                if self.state[const.STATE] in [const.DIVE, const.BONK]:
                    self.state[const.STATE] = const[self.state[const.STATE].value + const.LAND.value]
                    self.state[const.FRAME] = 0

        if self.state[const.VELOCITY] and self.state[const.VERTICAL_VELOCITY]:
            while self.state[const.HITBOX].move(self.state[const.VELOCITY], self.state[const.VERTICAL_VELOCITY]).collidelist(plats) != -1:
                self.state[const.VELOCITY] += 1 if self.state[const.VELOCITY] < 0 else -1
                self.state[const.VERTICAL_VELOCITY] += 1 if self.state[const.VERTICAL_VELOCITY] < 0 else -1

    def get_surface(self, game_state): #placeholder untill i have pixel art
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
