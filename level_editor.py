"""
Level editor

right now im just going for platforms
check out the redpantsadventure repo to see what im going for [spaghetti warning]
https://github.com/doctorMcbob/RedPantsAdventure/blob/master/leveleditor.py

platforms:
    (x, y, w, h, idx)
"""
import pygame
from pygame.locals import *
from pygame import Surface

import sys

from pathlib import Path
from dotenv import load_dotenv

# okay im copy pasting a lot from boot here
# just trying to get wheels on

ROOT_DIR = Path('.')
ENV_FILE_PATH = ROOT_DIR / '.env'

# Load environment variables from .env file
load_dotenv(dotenv_path=ENV_FILE_PATH)

# Add root game directory to system path for module loading
sys.path.append(ROOT_DIR.as_posix())

path_to_levels = Path('.') / "src/game_levels/bin/"

from src.game import *
from src.game_levels.levels import load_level
from src.const import GameConstants as const
from src.config import GAME_CONFIG as config
from src.game_data_templates.game_world_state import GAME_WORLD_STATE_TEMPLATE
from src.game_data_templates.game_state import GAME_STATE_TEMPLATE
from src.game_objects.game_world import GameWorld
from src.lib.input_manager.input_handlers import (
    game as game_input_handler,
)

from src.lib import utils
from src.lib.input_manager import input_interpreter
from src.game_objects.game_player import GamePlayer
from src.game_objects.game_world import GameWorld
from src.game_objects.game_actor import GameActor
from src.game_data_templates.player_state import PLAYER_STATE_TEMPLATE
from src.game_data_templates.game_world_state import GAME_WORLD_STATE_TEMPLATE
from src.game_data_templates.game_player_hitbox_config import GAME_PLAYER_HITBOX_CONFIG
from src.game_data_templates.actor_templates import ACTOR_FUNCTION_MAP
from src.game_data_templates.input_config import (
    INPUT_CONFIG_TEMPLATE,
)

STATIC_OBJ_NAMES = {
    const.PLATFORMS: ["X", "Y", "W", "H", "Image idx"],
    const.SPIKES: ["X", "Y", "Direction"]
}

pygame.init()
HEL32 = pygame.font.SysFont("Helvetica", 32)
HEL16 = pygame.font.SysFont("Helvetica", 16)

STATIC_OBJ_TEXT_KEY = {
    const.PLATFORMS: ["X", "Y", "Width", "Height", "image idx"],
    const.SPIKES: ["X", "Y", "direction"],
}

# try to load level from command line
try:
    LEVEL = load_level(sys.argv[-1])
except IOError:
    print("Could not load level, starting fresh")
    
    LEVEL = {
        const.SPAWN: (0, 0),
        const.PLATFORMS: [],
        const.ENEMIES: [],
        const.SPIKES: [],
        const.ACTORS: [],
    }


def savable(d):
    new = {}
    for key in d.keys():
        if type(key) == const: new[key.name] = d[key]
        else: new[key] = d[key]
    return new
        
    
def save():
    filename = input("Save as (blank for NO SAVE)\n> ")
    if not filename: return
    actors = []
    for i in range(len(LEVEL[const.ACTORS])):
        actors.append(savable(LEVEL[const.ACTORS][i]))

    level = {
        "SPAWN": LEVEL[const.SPAWN],
        "PLATS": LEVEL[const.PLATFORMS],
        "ENEMIES": LEVEL[const.ENEMIES],
        "SPIKES": LEVEL[const.SPIKES],
        "ACTORS": actors,
    }
    with open(path_to_levels / filename, "w") as f:
        f.write(repr(level))


def reset_game_state():
    GAME_STATE = GAME_STATE_TEMPLATE.copy()
    GAME_STATE[const.SCREEN] = pygame.display.set_mode((
        GAME_STATE[const.WIDTH],
        GAME_STATE[const.HEIGHT]
    ))
    GAME_STATE[const.LEVEL] = LEVEL
    GAME_STATE[const.LOADED_ACTORS] = []
    for actor in GAME_STATE[const.LEVEL][const.ACTORS]: load_actor(GAME_STATE, actor)

    GAME_STATE[const.GAME_CLOCK] = pygame.time.Clock()
    GAME_STATE[const.FONTS][const.FONT_HELVETICA] = pygame.font.SysFont("Helvetica", 16)

    pygame.display.set_caption("lookin good")

    return GAME_STATE


GAME_STATE = reset_game_state()
font = GAME_STATE[const.FONTS][const.FONT_HELVETICA] = pygame.font.SysFont("Helvetica", 16)

CURSOR = [GAME_STATE[const.WIDTH] / 2, GAME_STATE[const.HEIGHT] / 2]
CORNER = None


def get_surface(level):
    xscroll = CURSOR[0] - GAME_STATE[const.WIDTH] // 2
    yscroll = CURSOR[1] - GAME_STATE[const.HEIGHT] // 2
    surf = Surface((
        GAME_STATE[const.WIDTH],
        GAME_STATE[const.HEIGHT]
    ))
    surf.fill((255, 255, 255))
    for plat in level[const.PLATFORMS]:
        surface = Surface((plat[2], plat[3]))
        surface.fill([(100, 100, 100), (200, 100, 100), (100, 200, 100), (100, 100, 200)][plat[4]])
        surface.blit(font.render("Platform", 0, (0, 0, 0)), (0, 0))
        surf.blit(surface, (plat[0] - xscroll , plat[1] - yscroll))
    for spike in level[const.SPIKES]:
        surface = Surface((32, 32))
        surface.fill((255, 100, 100))
        surface.blit(font.render("Spike", 0, (0, 0, 0)
        ), (0, 0))
        surf.blit(surface, (spike[0] - xscroll , spike[1] - yscroll))
    for actor in level[const.ACTORS]:
        surface = Surface((actor[const.WIDTH], actor[const.HEIGHT]))
        surface.fill((150, 255, 150))
        surface.blit(font.render(actor[const.NAME], 0, (0, 0, 0)
        ), (0, 0))
        surf.blit(surface, (actor[const.X_COORD] - xscroll , actor[const.Y_COORD] - yscroll))
    if CORNER is not None: surf.blit(font.render("C", 0, (0, 0, 0)), (CORNER[0]-xscroll, CORNER[1]-yscroll))

    spwn = Surface((64, 64))
    spwn.fill((0, 255, 0))
    surf.blit(spwn, (LEVEL[const.SPAWN][0] - xscroll , LEVEL[const.SPAWN][1] - yscroll))
    
    return surf

def draw_cursor():
    pygame.draw.line(GAME_STATE[const.SCREEN], (255, 0, 0), 
        (GAME_STATE[const.WIDTH] // 2, GAME_STATE[const.HEIGHT] // 2),
        (GAME_STATE[const.WIDTH] // 2 + 32, GAME_STATE[const.HEIGHT] // 2 + 32), 2)
    pygame.draw.line(GAME_STATE[const.SCREEN], (255, 0, 0),
        (GAME_STATE[const.WIDTH] // 2, GAME_STATE[const.HEIGHT] // 2 + 32),
        (GAME_STATE[const.WIDTH] // 2 + 32, GAME_STATE[const.HEIGHT] // 2), 2)


def make_spike(level):
    level[const.SPIKES].append([CURSOR[0], CURSOR[1], 0])
    
def make_platform(level):
    global CORNER
    if CORNER is None:
        CORNER = CURSOR.copy()
        return
    x = min(CURSOR[0], CORNER[0])
    y = min(CURSOR[1], CORNER[1])
    w = abs(CURSOR[0] - CORNER[0]) + 32
    h = abs(CURSOR[1] - CORNER[1]) + 32
    
    level[const.PLATFORMS].append([x, y, w, h, 1])

    CORNER = None

def select_from_list(l, pos, dim):
    selected = 0
    while True:
        surf = Surface(dim)
        surf.fill((150, 150, 150))
        for i, data in enumerate(l):
            col = (0, 0, 0) if i != selected else (200, 100, 100)
            surf.blit(HEL16.render(str(data), 0, col), (0, i * 16))
        GAME_STATE[const.SCREEN].blit(surf, pos)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == QUIT: quit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE: return False
                if e.key == K_UP: selected = (selected - 1) % len(l)
                if e.key == K_DOWN: selected = (selected + 1) % len(l)
                if e.key in [K_RETURN, K_SPACE]:
                    return l[selected]

def get_numeric_input(pos):
    num = ''
    while True:
        for e in pygame.event.get():
            if e.type == QUIT: quit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE: return False
                if e.key == K_BACKSPACE: num = num[:-1]
                
                if e.key == K_0: num += '0'
                if e.key == K_1: num += '1'
                if e.key == K_2: num += '2'
                if e.key == K_3: num += '3'
                if e.key == K_4: num += '4'
                if e.key == K_5: num += '5'
                if e.key == K_6: num += '6'
                if e.key == K_7: num += '7'
                if e.key == K_8: num += '8'
                if e.key == K_9: num += '9'

                if e.key in [K_SPACE, K_RETURN]: return bool(num) and int(num)
        surf = Surface((64, 16))
        surf.fill((230, 230, 230))
        surf.blit(HEL16.render(num, 0, (0, 0, 0)), (0, 0))
        GAME_STATE[const.SCREEN].blit(surf, pos)
        pygame.display.update()

def choose_position():
    while True:
        for e in pygame.event.get():
            if e.type == QUIT: quit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    return False
                if e.key in [K_SPACE, K_RETURN]:
                    return tuple(CURSOR)
                if e.key == K_RIGHT:
                    CURSOR[0] += 32
                if e.key == K_LEFT:
                    CURSOR[0] -= 32
                if e.key == K_DOWN:
                    CURSOR[1] += 32
                if e.key == K_UP:
                    CURSOR[1] -= 32
    
        GAME_STATE[const.SCREEN].blit(get_surface(LEVEL), (0, 0))
        draw_cursor()
        GAME_STATE[const.SCREEN].blit(HEL32.render(str(CURSOR), 0, (0 ,0, 0)), (0, 0))
        pygame.display.update()
    
def make_menu(name):
    if name in STATIC_OBJ_NAMES:
        surf = Surface((256, 64))
        obj = []
        for text in STATIC_OBJ_NAMES[name]:
            surf.fill((150, 150, 150))
            surf.blit(HEL16.render(text, 0, (0, 0, 0)), (32, 16))
            GAME_STATE[const.SCREEN].blit(surf, (256, 256))
            obj.append(get_numeric_input((256 + 32, 256 + 32)))
            if False in obj: return
        LEVEL[name].append(obj)
    if name == const.ACTORS:
        keys = list(ACTOR_FUNCTION_MAP.keys())
        actor = select_from_list(keys, (256, 256), (126, 256))
        if actor in ACTOR_FUNCTION_MAP:
            temp = ACTOR_FUNCTION_MAP[actor]['template'].copy()
            surf = Surface((256, 64))
            for key in temp.keys():
                surf.fill((150, 150, 150))
                surf.blit(HEL16.render(str(key), 0, (0, 0, 0)), (32, 16))
                GAME_STATE[const.SCREEN].blit(surf, (256, 256))
                if type(temp[key]) == int:
                    temp[key] = get_numeric_input((256 + 32, 256 + 32))
                if type(temp[key]) == list and type(temp[key][0]) == tuple:
                    if len(temp[key]):
                        temp[key] = [tuple([n if n not in temp else temp[n] for n in tup]) for tup in temp[key]]
                    pos = choose_position()
                    while pos:
                        temp[key].append(pos)
                        pos = choose_position()
            temp[const.NAME] = actor
            LEVEL[const.ACTORS].append(temp)


def submenu(game_state, name):
    inmenu = True
    selected = 0
    while inmenu:
        submenu = Surface((640, 480))
        submenu.fill((100, 100, 100))
        submenu.blit(HEL32.render(str(name), 0, (0, 0, 0)), (16, 16))
        itemlist = Surface((640 - 32, max((len(LEVEL[name]) + 1) * 16, 400)))
        itemlist.fill((200, 200, 200))
        for i, item in enumerate(LEVEL[name]):
            col = (0, 0, 0) if i != selected else (200, 0, 0)
            itemlist.blit(HEL16.render(repr(item), 0, col), (0, i * 16))
        col = (0, 0, 0) if len(LEVEL[name]) != selected else (200, 0, 0)
        itemlist.blit(HEL16.render("New...", 0, col), (0, len(LEVEL[name]) * 16))
        submenu.blit(itemlist, (16, 64))
        game_state[const.SCREEN].blit(submenu, ((game_state[const.WIDTH] / 2) - 320, (game_state[const.HEIGHT] / 2) - 240))
        pygame.display.update()

        objmenu = False
        for e in pygame.event.get():
            if e.type == QUIT: quit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE: inmenu = False
                if e.key == K_DOWN: selected = (selected + 1) % (len(LEVEL[name]) + 1)
                if e.key == K_UP: selected = (selected - 1) % (len(LEVEL[name]) + 1)

                if e.key == K_SPACE:
                    if selected != len(LEVEL[name]): objmenu = True
                    else:
                        make_menu(name)
        selected2 = 0
        while objmenu:
            menu = Surface((640 - 32, max(len(LEVEL[name][selected]) * 16, 400)))
            menu.fill((200, 200, 200))
            if type(LEVEL[name][selected]) != dict:
                CURSOR[0] = LEVEL[name][selected][0]
                CURSOR[1] = LEVEL[name][selected][1]
                for i, data in enumerate(list(LEVEL[name][selected]) + ["move", "delete"]):
                    col = (0, 0, 0) if i != selected2 else (200, 0, 0)
                    if i < len(STATIC_OBJ_NAMES[name]):
                        menu.blit(font.render(STATIC_OBJ_NAMES[name][i], 0, col), (0, i * 16))
                    menu.blit(font.render(str(data), 0, col), (128, i * 16))
            else:
                keys = list(LEVEL[name][selected].keys())
                CURSOR[0] = LEVEL[name][selected][const.X_COORD]
                CURSOR[1] = LEVEL[name][selected][const.Y_COORD]
                for i, key in enumerate(keys + ["move", "delete"]):
                    col = (0, 0, 0) if i != selected2 else (200, 0, 0)
                    menu.blit(font.render(str(key), 0, col), (0, i * 16))
                    if key in LEVEL[name][selected]:
                        menu.blit(font.render(str(LEVEL[name][selected][key]), 0, col), (256, i * 16))
            submenu.blit(menu, (16, 64))
            game_state[const.SCREEN].blit(submenu, ((game_state[const.WIDTH] / 2) - 320, (game_state[const.HEIGHT] / 2) - 240))
            pygame.display.update()
            for e in pygame.event.get():
                if e.type == QUIT: quit()
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE: objmenu = False
                    if e.key == K_DOWN: selected2 = (selected2 + 1) % (len(LEVEL[name][selected].keys()) + 2)
                    if e.key == K_UP: selected2 = (selected2 - 1) % (len(LEVEL[name][selected].keys()) + 2)

                    if e.key == K_LEFT:
                        try:
                            if type(LEVEL[name][selected]) != dict:
                                LEVEL[name][selected][selected2] = int(LEVEL[name][selected][selected2]) - 16
                            else:
                                LEVEL[name][selected][keys[selected2]] = int(LEVEL[name][selected][keys[selected2]]) - 16
                        except TypeError: pass
                        except ValueError: pass
                    if e.key == K_RIGHT:
                        try:
                            if type(LEVEL[name][selected]) != dict:
                                LEVEL[name][selected][selected2] = int(LEVEL[name][selected][selected2]) + 16
                            else:
                                LEVEL[name][selected][keys[selected2]] = int(LEVEL[name][selected][keys[selected2]]) + 16
                        except TypeError: pass
                        except ValueError: pass
                    
                    if e.key in [K_SPACE, K_RETURN]:
                        if selected2 == len(LEVEL[name][selected]): # moving
                            moving = True
                            while moving:
                                for e in pygame.event.get():
                                    if e.type == QUIT: quit()
                                    if e.type == KEYDOWN:
                                        if e.key in [K_SPACE, K_RETURN, K_ESCAPE]:
                                            moving = False
                                        if e.key == K_RIGHT:
                                            CURSOR[0] += 32
                                            if type(LEVEL[name][selected]) == dict:
                                                LEVEL[name][selected][const.X_COORD] += 32
                                            else: LEVEL[name][selected][0] += 32
                                        if e.key == K_LEFT:
                                            CURSOR[0] -= 32
                                            if type(LEVEL[name][selected]) == dict:
                                                LEVEL[name][selected][const.X_COORD] -= 32
                                            else: LEVEL[name][selected][0] -= 32
                                        if e.key == K_DOWN:
                                            CURSOR[1] += 32
                                            if type(LEVEL[name][selected]) == dict:
                                                LEVEL[name][selected][const.Y_COORD] += 32
                                            else: LEVEL[name][selected][1] += 32
                                        if e.key == K_UP:
                                            CURSOR[1] -= 32
                                            if type(LEVEL[name][selected]) == dict:
                                                LEVEL[name][selected][const.Y_COORD] -= 32
                                            else: LEVEL[name][selected][1] -= 32
                                        
                                GAME_STATE[const.SCREEN].blit(get_surface(LEVEL), (0, 0))
                                pygame.display.update()

                        if selected2 == len(LEVEL[name][selected]) + 1: # deleting
                            LEVEL[name].pop(selected)
                            objmenu = False


# changed from the main loop in game.py to not quit on game exit
def alt_main_loop(game_state):
    GAME_PLAYER_ONE = GamePlayer(
        PLAYER_STATE_TEMPLATE,
        config[const.PLAYER_ONE_SPRITE_SHEET],
        GAME_PLAYER_HITBOX_CONFIG
    )
    GAME_WORLD = GameWorld(GAME_WORLD_STATE_TEMPLATE)
    GAME_SYSTEM_INPUT_CONFIG = INPUT_CONFIG_TEMPLATE.copy()
    GAME_PLAYER_ONE.initialize()
    GAME_PLAYER_ONE.state[const.SPAWN] = game_state[const.LEVEL][const.SPAWN]
    GAME_PLAYER_ONE.state[const.X_COORD], GAME_PLAYER_ONE.state[const.Y_COORD] = GAME_PLAYER_ONE.state[const.SPAWN]

    while True:
        game_state[const.GAME_CLOCK].tick(30)
        raw_game_inputs = pygame.event.get()
        system_game_inputs = input_interpreter.parse_input(raw_game_inputs, GAME_SYSTEM_INPUT_CONFIG)
        if system_game_inputs: utils.process_game_inputs(game_state, game_input_handler, system_game_inputs)
        if game_state[const.SHOULD_EXIT_FLAG]: return
        if game_state[const.SHOULD_ADVANCE_FRAME]:
            GAME_PLAYER_ONE.get_state()[const.FRAME] += 1
            GAME_PLAYER_ONE.update_state(game_state, GAME_WORLD.get_state(), raw_game_inputs)
            GAME_WORLD.update_state(game_state, GAME_PLAYER_ONE)
            if game_state[const.IS_DEBUG_MODE_ACTIVE]: print_game_states(game_state)
            game_world_surface = GAME_WORLD.get_surface(game_state, GAME_PLAYER_ONE)
            draw_screen(game_state, game_world_surface)
            
        if game_state[const.IS_DEBUG_MODE_ENABLED]: game_state[const.SHOULD_ADVANCE_FRAME] = not game_state[const.IS_DEBUG_MODE_ACTIVE]

# main loop
while True:
    for e in pygame.event.get():
        if e.type == QUIT: quit()
        if e.type == KEYDOWN:
            if e.key == K_RIGHT: CURSOR[0] += 32
            if e.key == K_LEFT: CURSOR[0] -= 32
            if e.key == K_UP: CURSOR[1] -= 32
            if e.key == K_DOWN: CURSOR[1] += 32

            if pygame.key.get_mods() & KMOD_CTRL:
                if e.key == K_s: submenu(GAME_STATE, const.SPIKES)
                if e.key == K_p: submenu(GAME_STATE, const.PLATFORMS)
                if e.key == K_a: submenu(GAME_STATE, const.ACTORS)
                if e.key == K_RETURN: save()
            else:
                if e.key == K_p: make_platform(LEVEL)
                if e.key == K_r: LEVEL[const.SPAWN] = tuple(CURSOR)
                if e.key == K_s: make_spike(LEVEL)
                if e.key == K_RETURN:
                    GAME_STATE = reset_game_state()
                    alt_main_loop(GAME_STATE)

    GAME_STATE[const.SCREEN].blit(get_surface(LEVEL), (0, 0))
    draw_cursor()
    pygame.display.update()
