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
from src.game_data_templates.player_state import PLAYER_STATE_TEMPLATE
from src.game_data_templates.game_world_state import GAME_WORLD_STATE_TEMPLATE
from src.game_data_templates.game_player_hitbox_config import GAME_PLAYER_HITBOX_CONFIG

from src.game_data_templates.input_config import (
    INPUT_CONFIG_TEMPLATE,
)

pygame.init()

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
    }

def save():
    filename = input("Save as (blank for NO SAVE)\n> ")
    if not filename: return
    level = {
        "SPAWN": LEVEL[const.SPAWN],
        "PLATS": LEVEL[const.PLATFORMS],
        "ENEMIES": LEVEL[const.ENEMIES],
        "SPIKES": LEVEL[const.SPIKES],
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
        surface.blit(font.render("Spike", 0, (0, 0, 0)), (0, 0))
        surf.blit(surface, (spike[0] - xscroll , spike[1] - yscroll))
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
        if e.type == QUIT or e.type == KEYDOWN and e.key == K_ESCAPE: quit()
        if e.type == KEYDOWN:
            if e.key == K_RIGHT: CURSOR[0] += 32
            if e.key == K_LEFT: CURSOR[0] -= 32
            if e.key == K_UP: CURSOR[1] -= 32
            if e.key == K_DOWN: CURSOR[1] += 32

            if e.key == K_SPACE: make_platform(LEVEL)
            if e.key == K_p: LEVEL[const.SPAWN] = tuple(CURSOR)
            if e.key == K_s: make_spike(LEVEL)
            
            if e.key == K_s and pygame.key.get_mods() & KMOD_CTRL: save()
            if e.key == K_RETURN:
                GAME_STATE = reset_game_state()
                alt_main_loop(GAME_STATE)
    GAME_STATE[const.SCREEN].blit(get_surface(LEVEL), (0, 0))
    draw_cursor()
    pygame.display.update()
