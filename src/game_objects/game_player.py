from src.const import GameConstants as const

from src.game_objects.game_world_entity import GameWorldEntity
from src.game_data_templates.input_config import (
    INPUT_CONFIG_TEMPLATE,
)

from src.lib import utils
from src.lib.input_manager import input_interpreter
from src.lib.input_manager.input_handlers import player as input_handler

MID_AIR_MOTION_STATE_WHITELIST = [
    const.RISING, const.AIR, const.FALLING,
    const.FASTFALLING, const.DIVE, const.DIVESTART,
    const.DIVELAND, const.DIVELANDJUMP, const.BONK,
    const.KICKFLIP0, const.KICKFLIP1, const.KICKFLIP2,
    const.WALL, const.WALLJUMPSTART,
]

JUMP_START_MOTION_STATE_BLACKLIST = [
    const.DIVE, const.DIVELANDJUMP, const.BONK,
    const.KICKFLIP0, const.KICKFLIP1, const.KICKFLIP2,
]
TRACTION_STATE_BLACKLIST = [
    const.RISING, const.AIR, const.FALLING,
    const.FASTFALLING, const.DIVE, const.DIVELANDJUMP,
    const.KICKFLIP0, const.KICKFLIP1, const.KICKFLIP2,
]

class GamePlayer(GameWorldEntity):
    def __init__(self, player_state_template, player_sprite_sheet_key, player_hitbox_config):
        super(GamePlayer, self).__init__(
            player_state_template,
            player_sprite_sheet_key,
            player_hitbox_config
        )

        self.state[const.INPUT_CONFIG] = INPUT_CONFIG_TEMPLATE.copy()
        # decided not to put this in the template
        # because i dont want it to reset on death
        self.inventory = {
            "coin": 0,
            "cheese": 0,
            # ...
        }
        
        self.motion_state_handlers = {
            const.SLIDE: self.__apply_slide_state,
            const.IDLE: self.__apply_idle_state,
            const.RUN: self.__apply_run_state,
            const.LAND: self.__apply_land_state,
        }
        
    def apply_platform_collision_detection(self, game_state):
        # checks if we are moving
        xflag = abs(self.state[const.VELOCITY]) > 0
        yflag = self.state[const.VERTICAL_VELOCITY] > 0

        super(GamePlayer, self).apply_platform_collision_detection(game_state)

        # if we were moving and are no longer moving
        if xflag and not self.state[const.VELOCITY]:
            # set up for wall jump if in the air
            if self.state[const.STATE] in [const.AIR, const.KICKFLIP2]:
                self.state[const.STATE] = const.WALL
                self.state[const.FRAME] = 0

            # bonk out of dive or divelandjump
            if self.state[const.STATE] in [const.DIVE, const.DIVELANDJUMP]:
                self.state[const.STATE] = const.BONK
                self.state[const.FRAME] = 0
        
        # if the player was moving downward and has stopped
        if yflag and not self.state[const.VERTICAL_VELOCITY]:
                # switch from most airborn states to LAND animation
                if self.state[const.STATE] in [const.FALLING, const.AIR, const.DIVELANDJUMP,
                                               const.KICKFLIP0, const.KICKFLIP1, const.KICKFLIP2,
                                               const.WALL]:
                    self.state[const.STATE] = const.LAND
                    self.state[const.FRAME] = 0

                # DIVE -> DIVELAND  BONK -> BONKLAND
                if self.state[const.STATE] in [const.DIVE, const.BONK]:
                    # this line is a little hacky but whatever
                    self.state[const.STATE] = const[self.state[const.STATE].value + const.LAND.value]
                    self.state[const.FRAME] = 0


    def apply_hazard_collision_detection(self, game_state):
        if self.state[const.STATE] == const.DMG: return
        if super(GamePlayer, self).apply_hazard_collision_detection(game_state):
            self.state[const.STATE] = const.DMG
            self.state[const.FRAME] = 0
            self.state[const.VELOCITY] = 0
            self.state[const.VERTICAL_VELOCITY] = 0
                    
    def update_state(self, game_state, game_world_state, raw_game_inputs):
        player_inputs = self.__parse_inputs(raw_game_inputs)

        if player_inputs:
            utils.process_game_inputs(self.state, input_handler, player_inputs)

        self.update_hitbox()
        self.update_movement_velocity(game_state, game_world_state)
        self.__update_motion_state()
        self.__update_traction_state()

        self.__update_kickflip_state()
        self.__update_walljump_state()
        self.__update_jump_state()
        self.__update_air_state(game_world_state)
        self.__update_falling_state()
        self.__update_dive_state()
        self.__update_bonk_state()
        self.__update_damage_state()
        self.__reset_jump_and_dive_flags()

        self.apply_platform_collision_detection(game_state)
        self.apply_hazard_collision_detection(game_state)

    def update_controls(self, new_input_config):
        self.state[const.INPUT_CONFIG] = new_input_config

    def __apply_slide_state(self):
        if self.state[const.VELOCITY] == 0:
            self.state[const.STATE] = const.IDLE
            self.state[const.FRAME] = 0
        elif self.state[const.VELOCITY] < 5:
            self.state[const.FRAME] = 1
        else:
            self.state[const.FRAME] = 0

    def __apply_land_state(self):
        if self.state[const.FRAME] == self.state[const.LANDING_FRAME]:
            self.state[const.STATE] = const.IDLE if self.state[const.MOVE] * self.state[const.VELOCITY] >= 0 else const.SLIDE
            self.state[const.FRAME] = 0

    def __apply_idle_state(self):
        if self.state[const.MOVE]:
            self.state[const.DIRECTION] = self.state[const.MOVE]
            self.state[const.STATE] = const.RUN
            self.state[const.FRAME] = 0
        elif self.state[const.VELOCITY]:
            self.state[const.STATE] = const.SLIDE

    def __apply_run_state(self):
        self.state[const.FRAME] = self.state[const.FRAME] % 30
        self.state[const.VELOCITY] = self.state[const.SPEED] * self.state[const.DIRECTION]

        if self.state[const.MOVE] != self.state[const.DIRECTION]:
            self.state[const.STATE] = const.SLIDE
            self.state[const.FRAME] = 0

    def __apply_traction_state(self):
        if self.state[const.VELOCITY] > 0:
            self.state[const.VELOCITY] = max(
                self.state[const.VELOCITY] - self.state[const.TRACTION],
                0
            )

        else:
            self.state[const.VELOCITY] = min(
                self.state[const.VELOCITY] + self.state[const.TRACTION],
                0
            )

    def __update_damage_state(self):
        if self.state[const.STATE] == const.DMG:
            self.state[const.VELOCITY] = 0
            self.state[const.VERTICAL_VELOCITY] = 0
            if self.state[const.FRAME] >= self.state[const.DMGFR]:
                self.state[const.X_COORD], self.state[const.Y_COORD] = self.state[const.SPAWN]
                self.state[const.STATE] = const.IDLE
                self.state[const.FRAME] = 0

    
    def __update_motion_state(self):
        player_motion_state = self.state[const.STATE]
        motion_state_handlers = self.motion_state_handlers.get(player_motion_state)

        if motion_state_handlers:
            motion_state_handlers()

    def __update_traction_state(self):
        player_motion_state = self.state[const.STATE]

        if player_motion_state not in TRACTION_STATE_BLACKLIST:
            self.__apply_traction_state()


    def __update_kickflip_state(self):
        if self.state[const.STATE] == const.SLIDE and self.state[const.JUMP] and self.state[const.MOVE] == -1 * self.state[const.DIRECTION]:
            self.state[const.STATE] = const.KICKFLIP0
            self.state[const.FRAME] = 0

            self.state[const.VERTICAL_VELOCITY] = self.state[const.KICKFLIPSTR]
            self.state[const.DIRECTION] *= -1
            self.state[const.VELOCITY] = self.state[const.DIRECTION] * 5

        if self.state[const.STATE] == const.KICKFLIP0 and self.state[const.VERTICAL_VELOCITY] >= self.state[const.KICKFLIPLIMIT]:
            self.state[const.STATE] = const.KICKFLIP1
            self.state[const.FRAME] = 0

        if self.state[const.STATE] in [const.KICKFLIP0, const.KICKFLIP1] and self.state[const.VERTICAL_VELOCITY] > 0:
            self.state[const.STATE] = const.KICKFLIP2
            self.state[const.FRAME] = 0

    def __update_walljump_state(self):
        is_starting_walljump = self.state[const.JUMP] and self.state[const.STATE] == const.WALL

        if is_starting_walljump:
            self.state[const.STATE] = const.WALLJUMPSTART
            self.state[const.FRAME] = 0

        if self.state[const.STATE] == const.WALLJUMPSTART:
            self.state[const.VERTICAL_VELOCITY] = 0

        is_walljumping = self.state[const.STATE] == const.WALLJUMPSTART and self.state[const.FRAME] >= self.state[const.WALLJUMPFRM]

        if is_walljumping:
            self.state[const.VELOCITY] = self.state[const.DIRECTION] * -1 * self.state[const.WALLJUMPSTR]
            self.state[const.DIRECTION] *= -1
            self.state[const.VERTICAL_VELOCITY] = self.state[const.JUMP_SPEED]
        
    def __update_jump_state(self):
        is_starting_squat = self.state[const.JUMP] and self.state[const.STATE] not in MID_AIR_MOTION_STATE_WHITELIST
        
        if is_starting_squat:
            self.state[const.STATE] = const.JUMPSQUAT
            self.state[const.FRAME] = 0
    
        is_starting_jump = self.state[const.STATE] == const.JUMPSQUAT and self.state[const.FRAME] >= self.state[const.JUMP_SQUAT_FRAME]

        if is_starting_jump:
            self.state[const.VERTICAL_VELOCITY] = self.state[const.JUMP_SPEED]

    def __update_air_state(self, game_world_state):
        # seperated from jump states because it should still trigger when walking off a platform
        is_airborn = self.state[const.STATE] not in JUMP_START_MOTION_STATE_BLACKLIST

        if is_airborn:
            if abs(self.state[const.VERTICAL_VELOCITY]) > game_world_state[const.GRAVITY]:
                self.state[const.STATE] = const.AIR
                self.state[const.FRAME] = 0

            if self.state[const.VERTICAL_VELOCITY] < -self.state[const.AIR]:
                self.state[const.STATE] = const.RISING
                self.state[const.FRAME] = 0

            if self.state[const.VERTICAL_VELOCITY] > self.state[const.AIR]:
                self.state[const.STATE] = const.FALLING
                self.state[const.FRAME] = 0

    def __update_falling_state(self):
        is_falling = self.state[const.STATE] == const.AIR and self.state[const.MOVE]

        if is_falling:
            if abs(self.state[const.VELOCITY] + self.state[const.DRIFT] * self.state[const.MOVE]) <= self.state[const.SPEED]:
                self.state[const.VELOCITY] += self.state[const.DRIFT] * self.state[const.MOVE]
            if self.state[const.VELOCITY]:
                self.state[const.DIRECTION] = self.state[const.MOVE] if self.state[const.MOVE] else self.state[const.DIRECTION]

        is_flipping = self.state[const.STATE] in [const.KICKFLIP1, const.KICKFLIP2]

        if is_flipping:
            if self.state[const.MOVE] == self.state[const.DIRECTION]:
                if abs(self.state[const.VELOCITY] + self.state[const.DRIFT] * self.state[const.MOVE]) <= self.state[const.SPEED]:
                    self.state[const.VELOCITY] += self.state[const.DRIFT] * self.state[const.MOVE]
        
    def __update_dive_state(self):
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

    def __update_bonk_state(self):
        is_bonking = self.state[const.STATE] == const.BONK and self.state[const.FRAME] <= 1

        if is_bonking:
            self.state[const.VELOCITY] = -10 * self.state[const.DIRECTION]
        elif self.state[const.STATE] == const.BONK:
            self.state[const.VELOCITY] = -2 * self.state[const.DIRECTION]
        
        has_bonked = self.state[const.STATE] == const.BONKLAND and self.state[const.FRAME] >= self.state[const.BONKLF]

        if has_bonked:
            self.state[const.STATE] = const.IDLE
            self.state[const.FRAME] = 0

    def __reset_jump_and_dive_flags(self):
        self.state[const.DIVE] = 0
        self.state[const.JUMP] = 0

    def __parse_inputs(self, raw_game_inputs):
        player_input_config = self.get_state()[const.INPUT_CONFIG]
        player_inputs = input_interpreter.parse_input(raw_game_inputs, player_input_config)

        return player_inputs
