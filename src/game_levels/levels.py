from src.config import GAME_CONFIG as config
from src.const import GameConstants as const
from src.game_objects.game_actor import GameActor
from src.game_data_templates.actor_templates import ACTOR_FUNCTION_MAP
from pathlib import Path

import sys

path_to_levels = Path('.') / "src/game_levels/bin/"

def unpack_consts(d):
    new = {}
    for key in d.keys():
        if key in dir(const): new[const[key]] = d[key]
        else: new[key] = d[key]
    return new

def load_actor(actor_template):
    name = actor_template[const.NAME]
    triggers = {} if 'triggers' not in ACTOR_FUNCTION_MAP[name] else ACTOR_FUNCTION_MAP[name]['triggers']
    update = False if 'update' not in ACTOR_FUNCTION_MAP[name] else ACTOR_FUNCTION_MAP[name]['update']
    collision = False if 'collision' not in ACTOR_FUNCTION_MAP[name] else ACTOR_FUNCTION_MAP[name]['collision']
    return GameActor(actor_template, None, {}, triggers, update, collision)

def load_level(filename):
    with open(path_to_levels / filename, "r") as f:
        level_data = eval(f.read())
    
    for key in level_data.keys():
        if key is not 'SPAWN':
            for i, item in enumerate(level_data[key]):
                if type(item) == tuple:
                    level_data[key][i] = list(item)

    for i, actor in enumerate(level_data["ACTORS"]): 
        level_data["ACTORS"][i] = unpack_consts(actor)
        
    return {
        const.SPAWN: level_data["SPAWN"],
        const.PLATFORMS: level_data["PLATS"],
        const.ENEMIES: level_data["ENEMIES"],
        const.SPIKES: level_data["SPIKES"],
        const.ACTORS: level_data["ACTORS"],
    }
