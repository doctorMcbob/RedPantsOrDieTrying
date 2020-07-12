"""
Level editor

--- Guide ---
keys:
   p         -  make platform (first press sets corner, second press completes)
   s         -  make spike
   c         -  make collectable
   r         -  move (re)spawn point   
   a         -  make actor (starts construction menu)
``return     -  play demo
  space      -  select object via collision

  Ctrl p     -  platform select menu
  Ctrl s     -  spike select menu
  Ctrl a     -  actor select menu
Ctrl return  -  save
  
~~ TO DO LIST ~~
[x] show cursor coordinates
[x] show moving platform path
 -- [x] during constructor 
[x] select objects through hit detection
[x] scrolling menus
[x] text entry field 
[x] saving without terminal
 -- [x] remember filename from commandline
[x] log text
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
from src.game_levels.levels import load_level, load_actor
from src.const import GameConstants as const
from src.config import GAME_CONFIG as config
from src.game_data_templates.game_world_state import GAME_WORLD_STATE_TEMPLATE
from src.game_data_templates.game_state import GAME_STATE_TEMPLATE
from src.game_objects.game_world import GameWorld
from src.lib.input_manager.input_handlers import (
    game as game_input_handler,
)
import src.lib.level_manager as level_manager
from src.lib.sprite_manager.sprite_sheet import load_sprite_sheet

from src.lib import utils
from src.lib.input_manager import input_interpreter
from src.game_objects.game_player import GamePlayer
from src.game_objects.game_world import GameWorld
from src.game_objects.game_actor import GameActor
from src.game_objects.game_world_entity import GameWorldEntity
from src.game_data_templates.player_state import PLAYER_STATE_TEMPLATE
from src.game_data_templates.game_world_state import GAME_WORLD_STATE_TEMPLATE
from src.game_data_templates.game_player_hitbox_config import GAME_PLAYER_HITBOX_CONFIG
from src.game_data_templates.actor_templates import ACTOR_FUNCTION_MAP, COLLECTABLE_TEMPLATE
from src.game_data_templates.input_config import (
    INPUT_CONFIG_TEMPLATE,
)

pygame.init()
HEL32 = pygame.font.SysFont("Helvetica", 32)
HEL16 = pygame.font.SysFont("Helvetica", 16)

LOG = Surface((256, 1024))
LOG.fill((150, 150, 150))

STATIC_OBJ_TEXT_KEY = {
    const.PLATFORMS: ["X", "Y", "Width", "Height", "image idx"],
    const.SPIKES: ["X", "Y", "direction"],
}

ALPHABET_KEY_MAP = {
    K_a: "a", K_b: "b", K_c: "c", K_d: "d", K_e: "e",
    K_f: "f", K_g: "g", K_h: "h", K_i: "i", K_j: "j",
    K_k: "k", K_l: "l", K_m: "m", K_n: "n", K_o: "o",
    K_p: "p", K_q: "q", K_r: "r", K_s: "s", K_t: "t",
    K_u: "u", K_v: "v", K_w: "w", K_x: "x", K_y: "y",
    K_z: "z", K_SPACE: " ", K_UNDERSCORE: "_",
    K_0: "0", K_1: "1", K_2: "2", K_3: "3", K_4: "4",
    K_5: "5", K_6: "6", K_7: "7", K_8: "8", K_9: "9",
    K_PLUS: "+", K_MINUS: "-", K_COLON: ":",
}

# try to load level from command line
try:
    FILENAME = sys.argv[-1]
    LEVEL = load_level(FILENAME)
except IOError:
    FILENAME = False
    print("Could not load level, starting fresh")
    
    LEVEL = {
        const.SPAWN: (0, 0),
        const.PLATFORMS: [],
        const.ENEMIES: [],
        const.SPIKES: [],
        const.ACTORS: [],
    }

def load(game_state):
    global LEVEL, FILENAME
    surf = Surface((256, 64))
    surf.fill((150, 150, 150)) 
    surf.blit(HEL16.render("(have you saved?) Load:", 0, (0, 0, 0)), (16, 16))
    GAME_STATE[const.SCREEN].blit(surf, (0, 0))
    filename = get_text_input((16, 32))
    if not filename: return
    FILENAME = filename
    LEVEL = load_level(filename)
    level_manager.get_level(game_state, filename)

def savable(d):
    new = {}
    for key in d.keys():
        if type(key) == const: new[key.name] = d[key]
        else: new[key] = d[key]

        try:
            for thing in new[key.name]:
                if isinstance(thing, GameWorldEntity):
                    print(thing)
                    new.remove(thing)
        except TypeError:
            continue # object is not iterable
            
    return new
        
    
def save(FILENAME=False):
    if FILENAME: filename = FILENAME
    if not FILENAME:
        surf = Surface((256, 64))
        surf.fill((150, 150, 150))
        surf.blit(HEL16.render("Save as:", 0, (0, 0, 0)), (16, 16))
        GAME_STATE[const.SCREEN].blit(surf, (0, 0))
        filename = get_text_input((16, 32))
    if not filename: return
    actors = [savable(a) for a in LEVEL[const.ACTORS]]

    level = {
        "SPAWN": LEVEL[const.SPAWN],
        "PLATS": LEVEL[const.PLATFORMS],
        "ENEMIES": LEVEL[const.ENEMIES],
        "SPIKES": LEVEL[const.SPIKES],
        "ACTORS": actors,
    }
    with open(path_to_levels / filename, "w") as f:
        f.write(repr(level))
    log("saved as " + filename)


def reset_game_state():
    GAME_STATE = GAME_STATE_TEMPLATE.copy()
    GAME_STATE[const.SCREEN] = pygame.display.set_mode((
        GAME_STATE[const.WIDTH],
        GAME_STATE[const.HEIGHT]
    ))
    GAME_STATE[const.LEVEL] = LEVEL
    GAME_STATE[const.LOADED_ACTORS] = [load_actor(actor) for actor in LEVEL[const.ACTORS]]

    GAME_STATE[const.GAME_CLOCK] = pygame.time.Clock()
    GAME_STATE[const.FONTS][const.FONT_HELVETICA] = pygame.font.SysFont("Helvetica", 16)

    pygame.display.set_caption("LEVEL EDITOR")

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
        surface.fill((1, 255, 1))
        try:
            sprites = load_sprite_sheet("platform" + str(plat[4]))
            for y in range(plat[3] // 32):
                if y == 0: i = '0'
                elif y == (plat[3] // 32) - 1: i = '2'
                else: i = '1'
                for x in range(plat[2] // 32):
                    if x == 0: j = '0'
                    elif x == (plat[2] // 32) - 1: j = '2'
                    else: j = '1'

                    surface.blit(sprites['p'+i+j], (x*32, y*32))

        except KeyError:
            surface.fill([(100, 100, 100), (200, 100, 100), (100, 200, 100), (100, 100, 200)][plat[4]])
            surface.blit(font.render("Platform", 0, (0, 0, 0)), (0, 0))

        surface.set_colorkey((1, 255, 1))
        surf.blit(surface, (plat[0] - xscroll , plat[1] - yscroll))
    for spike in level[const.SPIKES]:
        surface = load_sprite_sheet("spike")['spike']
        surface = pygame.transform.rotate(surface, spike[2] * 90)
        surf.blit(surface, (spike[0] - xscroll , spike[1] - yscroll))
    for actor in level[const.ACTORS]:
        surface = Surface((actor[const.WIDTH], actor[const.HEIGHT]))
        surface.fill((150, 255, 150))
        surface.blit(font.render(actor[const.NAME], 0, (0, 0, 0)), (0, 0))
        surf.blit(surface, (actor[const.X_COORD] - xscroll , actor[const.Y_COORD] - yscroll))
        if const.PATH in actor: draw_path(surf, actor[const.PATH])
    if CORNER is not None: surf.blit(font.render("C", 0, (0, 0, 0)), (CORNER[0]-xscroll, CORNER[1]-yscroll))

    spwn = Surface((64, 64))
    spwn.fill((0, 255, 0))
    surf.blit(spwn, (LEVEL[const.SPAWN][0] - xscroll , LEVEL[const.SPAWN][1] - yscroll))
    
    return surf

def expect_input(expectlist=[]):
    while True:
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == QUIT: quit()
            if e.type == KEYDOWN:
                if expectlist:
                    if e.key in expectlist: return e.key
                else: return e.key

def log(text):
    global LOG
    new = Surface((256, 1024))
    new.fill((150, 150, 150))
    new.blit(LOG, (0, 16))
    new.blit(HEL16.render(text, 0, (0, 0, 0)), (0, 0))
    LOG = new

def show_log():
    GAME_STATE[const.SCREEN].blit(LOG, (GAME_STATE[const.WIDTH]-256, 0))
    expect_input()
    
def draw_path(surf, path):
    if not path: return
    xscroll = CURSOR[0] - GAME_STATE[const.WIDTH] // 2
    yscroll = CURSOR[1] - GAME_STATE[const.HEIGHT] // 2
    for point in path:
        point = int(point[0] - xscroll), int(point[1] - yscroll)
        pygame.draw.circle(surf, (0, 180, 0), point, 5)
    i = 0
    while i + 1 < len(path):
        p1 = path[i][0] - xscroll, path[i][1] - yscroll
        p2 = path[(i + 1) % len(path)]
        p2 = p2[0] - xscroll, p2[1] - yscroll
        pygame.draw.line(surf, (0, 210, 0), p1, p2, 2)
        i += 1

def draw_cursor():
    pygame.draw.line(GAME_STATE[const.SCREEN], (255, 0, 0), 
        (GAME_STATE[const.WIDTH] // 2, GAME_STATE[const.HEIGHT] // 2),
        (GAME_STATE[const.WIDTH] // 2 + 32, GAME_STATE[const.HEIGHT] // 2 + 32), 2)
    pygame.draw.line(GAME_STATE[const.SCREEN], (255, 0, 0),
        (GAME_STATE[const.WIDTH] // 2, GAME_STATE[const.HEIGHT] // 2 + 32),
        (GAME_STATE[const.WIDTH] // 2 + 32, GAME_STATE[const.HEIGHT] // 2), 2)
    GAME_STATE[const.SCREEN].blit(HEL16.render(str(int(CURSOR[0])) + ", " + str(int(CURSOR[1])), 0, (255, 0, 0)), (GAME_STATE[const.WIDTH] // 2, GAME_STATE[const.HEIGHT] // 2 + 32))
    

def make_spike(level):
    level[const.SPIKES].append([int(CURSOR[0]), int(CURSOR[1]), 0])
    log("made spike at " + str(CURSOR))
    
def make_platform(level):
    global CORNER
    if CORNER is None:
        CORNER = CURSOR.copy()
        return
    x = int(min(CURSOR[0], CORNER[0]))
    y = int(min(CURSOR[1], CORNER[1]))
    w = int(abs(CURSOR[0] - CORNER[0]) + 32)
    h = int(abs(CURSOR[1] - CORNER[1]) + 32)
    
    level[const.PLATFORMS].append([x, y, w, h, 1])

    CORNER = None
    log("made platform at " + str((x, y)))
    
def make_collectable(level):
    template = COLLECTABLE_TEMPLATE.copy()
    template[const.X_COORD] = CURSOR[0]
    template[const.Y_COORD] = CURSOR[1]
    level[const.ACTORS].append(template)
    log("made collectable at " + str(CURSOR))

def select_from_list(l, pos, dim):
    global CURSOR
    if not l: return False
    selected = 0
    while True:
        surf = Surface((dim[0], max(dim[1], len(l) * 16)))
        surf.fill((150, 150, 150))
        for i, data in enumerate(l):
            col = (0, 0, 0) if i != selected else (200, 100, 100)
            surf.blit(HEL16.render(str(data), 0, col), (0, i * 16))
        if type(l[selected]) == list:
            CURSOR = [l[selected][0], l[selected][1]]
        elif type(l[selected]) == dict and const.X_COORD in l[selected]:
            CURSOR = [l[selected][const.X_COORD], l[selected][const.Y_COORD]]
        GAME_STATE[const.SCREEN].blit(get_surface(LEVEL), (0, 0))
        draw_cursor()
        GAME_STATE[const.SCREEN].blit(surf, (pos[0], pos[1] - (selected * 16)))
        pygame.display.update()

        inp = expect_input()
        if inp == K_ESCAPE: return False
        if inp == K_UP: selected = (selected - 1) % len(l)
        if inp == K_DOWN: selected = (selected + 1) % len(l)
        if inp in [K_RETURN, K_SPACE]: return l[selected]

def get_text_input(pos):
    string = ''
    while True:
        surf = Surface((128, 16))
        surf.fill((230, 230, 230))
        surf.blit(HEL16.render(string, 0, (0, 0, 0)), (0, 0))
        GAME_STATE[const.SCREEN].blit(surf, pos)
        pygame.display.update()

        inp = expect_input()
        if inp == K_ESCAPE: return False
        if inp == K_BACKSPACE: string = string[:-1]
        if inp == K_RETURN: return string
        
        if pygame.key.get_mods() & KMOD_SHIFT:
            if inp in ALPHABET_KEY_MAP:
                string = string + ALPHABET_KEY_MAP[inp].upper()
        elif inp in ALPHABET_KEY_MAP:
            string = string + ALPHABET_KEY_MAP[inp]


def get_numeric_input(pos):
    num = ''
    while True:
        surf = Surface((128, 16))
        surf.fill((230, 230, 230))
        surf.blit(HEL16.render(num, 0, (0, 0, 0)), (0, 0))
        GAME_STATE[const.SCREEN].blit(surf, pos)
        pygame.display.update()

        inp = expect_input()
        if inp == K_ESCAPE: return False
        if inp == K_BACKSPACE: num = num[:-1]
                
        if inp == K_0: num += '0'
        if inp == K_1: num += '1'
        if inp == K_2: num += '2'
        if inp == K_3: num += '3'
        if inp == K_4: num += '4'
        if inp == K_5: num += '5'
        if inp == K_6: num += '6'
        if inp == K_7: num += '7'
        if inp == K_8: num += '8'
        if inp == K_9: num += '9'
        if inp == K_MINUS:
            if num.startswith("-"): num = num[1:]
            else: num = "-" + num

        if inp in [K_SPACE, K_RETURN]: return bool(num) and int(num)


def choose_position(path=None):
    while True:
        GAME_STATE[const.SCREEN].blit(get_surface(LEVEL), (0, 0))
        if path is not None: draw_path(GAME_STATE[const.SCREEN], path)
        draw_cursor()
        GAME_STATE[const.SCREEN].blit(HEL32.render(str(CURSOR), 0, (0 ,0, 0)), (0, 0))
        if path is not None: GAME_STATE[const.SCREEN].blit(HEL32.render("choose path", 0, (0, 0, 0)), (0, 32))
        pygame.display.update()

        inp = expect_input()
        if inp == K_ESCAPE: return False
        if inp in [K_SPACE, K_RETURN]: return tuple(CURSOR)
        if inp == K_RIGHT: CURSOR[0] += 32
        if inp == K_LEFT: CURSOR[0] -= 32
        if inp == K_DOWN: CURSOR[1] += 32
        if inp == K_UP: CURSOR[1] -= 32


def make_path():
    path = []
    pos =  choose_position(path)
    while pos:
        path.append(pos)
        pos =  choose_position(path)
    return path
        
def static_menu(name, obj, pos):
    """
    much better this time
    """
    if obj is False: return
    selected = 0
    while True:
        surf = Surface((256, (len(obj) + 2) * 16 + 32))
        surf.fill((150, 150, 150))
        for i, text in enumerate(STATIC_OBJ_TEXT_KEY[name] + ["move", "delete"]):
            col = (0, 0, 0) if i != selected else (200, 100, 100)
            surf.blit(HEL16.render(text, 0, col), (16, 16 + (i * 16)))
            if i < len(obj):
                surf.blit(HEL16.render(str(obj[i]), 0, col), (128, 16 + (i * 16)))

        GAME_STATE[const.SCREEN].blit(get_surface(LEVEL), (0, 0))
        draw_cursor()
        GAME_STATE[const.SCREEN].blit(surf, pos)
        pygame.display.update()

        inp = expect_input()
        if inp == K_ESCAPE: return

        if inp == K_UP: selected = (selected - 1) % (len(obj) + 2)
        if inp == K_DOWN: selected = (selected + 1) % (len(obj) + 2)

        if selected >= len(obj):
            if inp in [K_SPACE, K_RETURN]:
                if selected == len(obj):
                    obj[0], obj[1] = choose_position()
                if selected == len(obj) + 1:
                    LEVEL[name].remove(obj)
                    return
        elif type(obj[selected]) == int:
            if inp in [K_SPACE, K_RETURN]:
                n = get_numeric_input((126, 16 + (selected * 16)))
                if not n is False: obj[selected] = n
            
            if inp == K_RIGHT: obj[selected] += 1
            if inp == K_LEFT: obj[selected] -= 1
            if pygame.key.get_mods() & KMOD_SHIFT:
                if inp == K_RIGHT: obj[selected] += 15
                if inp == K_LEFT: obj[selected] -= 15


def actor_menu(actor, pos):
    if actor is False: return
    if actor == "new...": return actor_constructor()
    keys = list(actor.keys())
    selected = 0
    while True:
        surf = Surface((638, 32 + (16 * (len(keys) + 2))))
        surf.fill((150, 150, 150))
        for i, key in enumerate(keys + ["move", "delete"]):
            col = (0, 0, 0) if selected != i else (200, 100, 100)
            surf.blit(HEL16.render(str(key), 0, col), (16, 16 + (i * 16)))
            if key in actor:
                surf.blit(HEL16.render(str(actor[key]), 0, col), (320, 16 + (i * 16)))

        GAME_STATE[const.SCREEN].blit(get_surface(LEVEL), (0, 0))
        draw_cursor()
        GAME_STATE[const.SCREEN].blit(surf, pos)
        pygame.display.update()

        inp = expect_input()
        if inp == K_ESCAPE: return

        if inp == K_UP: selected = (selected - 1) % (len(keys) + 2)
        if inp == K_DOWN: selected = (selected + 1) % (len(keys) + 2)

        if selected >= len(keys):
            if inp in [K_SPACE, K_RETURN]:
                if selected == len(keys):
                    actor[const.X_COORD], actor[const.Y_COORD] = choose_position()
                if selected == len(keys) + 1:
                    LEVEL[const.ACTORS].remove(actor)
                    return
        
        elif type(actor[keys[selected]]) == int: 
            if inp in [K_SPACE, K_RETURN]:
                n = get_numeric_input((320, 16 + (selected * 16)))
                if not n is False: actor[keys[selected]] = n
            
            if inp == K_RIGHT: actor[keys[selected]] += 1
            if inp == K_LEFT: actor[keys[selected]] -= 1
            if pygame.key.get_mods() & KMOD_SHIFT:
                if inp == K_RIGHT: actor[keys[selected]] += 15
                if inp == K_LEFT: actor[keys[selected]] -= 15

        elif type(actor[keys[selected]]) == str:
            if inp in [K_SPACE, K_RETURN]:
                s = get_text_input((320, 16 + (selected * 16)))
                if not s is False: actor[keys[selected]] = s

        elif keys[selected] == const.DROP:
            if inp in [K_SPACE, K_RETURN]:
                actor[keys[selected]] = choose_position()

        elif keys[selected] == const.PATH:
            if inp in [K_SPACE, K_RETURN]:
                path = make_path()
                if path: actor[const.PATH] = path

def set_attr_menu(name, pos, dim):
    surf = Surface(dim)
    surf.fill((150, 150, 150))
    surf.blit(HEL32.render(name, 0, (0, 0, 0)), (16, 16))
    GAME_STATE[const.SCREEN].blit(get_surface(LEVEL), (0, 0))
    draw_cursor()
    GAME_STATE[const.SCREEN].blit(surf, pos)
    return get_numeric_input((pos[0] + 16, pos[1] + 64))
    
def actor_constructor():
    name = select_from_list(list(ACTOR_FUNCTION_MAP.keys()), (0, 128), (128, 128))
    if name is False: return
    template = ACTOR_FUNCTION_MAP[name]['template'].copy()
    keys = list(template.keys())
    for key in keys:
        if key == const.X_COORD: template[key] = int(CURSOR[0])
        if key == const.Y_COORD: template[key] = int(CURSOR[1])
        if key == const.PATH: template[key] = make_path()

        if key in [const.HEIGHT, const.WIDTH, const.SPEED, const.TIMER]:
            template[key] = int(set_attr_menu(key.value, (0, 0), (128, 128)))

    LEVEL[const.ACTORS].append(template)
    log("made " + name + " at " + str(CURSOR))

def collision_select():
    hitbox = Rect(tuple(CURSOR), (32, 32))
    i = hitbox.collidelist([Rect((p[0], p[1]), (p[2], p[3])) for p in LEVEL[const.PLATFORMS]])
    if i != -1: return static_menu(const.PLATFORMS, LEVEL[const.PLATFORMS][i], (0, 0))
    i = hitbox.collidelist([Rect((s[0], s[1]), (32, 32)) for s in LEVEL[const.SPIKES]])
    if i != -1: return static_menu(const.SPIKES, LEVEL[const.SPIKES][i], (0, 0))
    i = hitbox.collidelist([Rect((a[const.X_COORD], a[const.Y_COORD]), (a[const.WIDTH], a[const.HEIGHT])) for a in LEVEL[const.ACTORS]])
    if i != -1: return actor_menu(LEVEL[const.ACTORS][i], (0, 0))

# set up environment, emulate main loop
def play(game_state):
    GAME_PLAYER_ONE = GamePlayer(
        PLAYER_STATE_TEMPLATE,
        config[const.PLAYER_ONE_SPRITE_SHEET],
        GAME_PLAYER_HITBOX_CONFIG
    )
    game_state[const.PLAYERS] = [GAME_PLAYER_ONE]
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
            for actor in game_state[const.LOADED_ACTORS]: actor.update_function(actor, game_state, GAME_WORLD.state)
            GAME_PLAYER_ONE.update_state(game_state, GAME_WORLD.get_state(), raw_game_inputs)
            GAME_WORLD.update_state(game_state, GAME_PLAYER_ONE)
            if game_state[const.IS_DEBUG_MODE_ACTIVE]: print_game_states(game_state)
            game_world_surface = GAME_WORLD.get_surface(game_state, GAME_PLAYER_ONE)
            draw_screen(game_state, game_world_surface)
            
        if game_state[const.IS_DEBUG_MODE_ENABLED]: game_state[const.SHOULD_ADVANCE_FRAME] = not game_state[const.IS_DEBUG_MODE_ACTIVE]

# main loop
while True:
    GAME_STATE[const.SCREEN].blit(get_surface(LEVEL), (0, 0))
    GAME_STATE[const.SCREEN].blit(LOG, (GAME_STATE[const.WIDTH]-256, GAME_STATE[const.HEIGHT]-16))
    draw_cursor()
    pygame.display.update()

    inp = expect_input()
    if inp == K_RIGHT: CURSOR[0] += 32
    if inp == K_LEFT: CURSOR[0] -= 32
    if inp == K_UP: CURSOR[1] -= 32
    if inp == K_DOWN: CURSOR[1] += 32

    if inp == K_SPACE: collision_select()
            
    if pygame.key.get_mods() & KMOD_CTRL:
        if inp == K_p: static_menu(const.PLATFORMS, select_from_list(LEVEL[const.PLATFORMS], (0, 320), (256, 640)), (0, 0))
        if inp == K_s: static_menu(const.SPIKES, select_from_list(LEVEL[const.SPIKES], (0, 320), (256, 640)), (0, 0))

        if inp == K_a: actor_menu(select_from_list(LEVEL[const.ACTORS] + ["new..."], (0, 320), (256, 640)), (0, 0))
        if inp == K_RETURN: save(FILENAME)
        if inp == K_BACKSPACE: load(GAME_STATE)
    else:
        if inp == K_l: show_log()
        if inp == K_a: actor_constructor()
        if inp == K_p: make_platform(LEVEL)
        if inp == K_r: LEVEL[const.SPAWN] = tuple(CURSOR)
        if inp == K_s: make_spike(LEVEL)
        if inp == K_c: make_collectable(LEVEL)
        if inp == K_RETURN:
            GAME_STATE = reset_game_state()
            play(GAME_STATE)
