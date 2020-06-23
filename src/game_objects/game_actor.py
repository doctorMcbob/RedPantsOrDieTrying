from pygame import Rect, Surface

from src.const import GameConstants as const

from src.game_objects.game_world_entity import GameWorldEntity

class GameActor(GameWorldEntity):
    def __init__(self, state_template, sprite_key, hitbox_config, triggers, update_function=False, collision_function=False):
        """
        trigger data:
         { ((x offset, y offset), (w, h)) : function... }
        """
        super(GameActor, self).__init__(
            state_template, sprite_key, hitbox_config)

        self.TRIGGERS = []
        self.TRIGGER_MAP = []
        for offset, dimensions in triggers.keys():
            self.TRIGGERS.append([Rect(self.state[const.X_COORD] + offset[0], self.state[const.Y_COORD] + offset[1])])
            self.TRIGGER_MAP.append(triggers[(offset, dimensions)])
        def off(*args): pass
        self.update_function = update_function or off
        self.collision_function = collision_function or off

    def check_triggers(self, player):
        triggers = list(self.TRIGGER_MAP.keys())
        i = Rect(self.state[const.HITBOX_CONFIG].get(self.state[const.STATE])).collidelist(triggers)
        if i != -1: TRIGGER_MAP[i](self)


        
