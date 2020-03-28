"""
Level editor

right now im just going for platforms
check out the redpantsadventure repo to see what im going for 
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

ROOT_DIR = Path('.')
ENV_FILE_PATH = ROOT_DIR / '.env'

# Load environment variables from .env file
load_dotenv(dotenv_path=ENV_FILE_PATH)

# Add root game directory to system path for module loading
sys.path.append(ROOT_DIR.as_posix())

from src.game_levels.levels import load_level
from src.const import GameConstants as const
from src.game_data_templates.game_world_state import GAME_WORLD_STATE_TEMPLATE
from src.game_data_templates.game_state import GAME_STATE_TEMPLATE
from src.game_objects.game_world import GameWorld

pygame.init()

try:
    LEVEL = load_level(sys.argv[-1])
except IOError:
    print("Could not load level, starting fresh")
    
    LEVEL = {
        const.PLATFORMS: [],
        const.ENEMIES: [],
        const.SPIKES: [],
    }

GAME_WORLD = GameWorld(GAME_WORLD_STATE_TEMPLATE)
GAME_STATE = GAME_STATE_TEMPLATE.copy()            
GAME_STATE[const.SCREEN] = pygame.display.set_mode((
        GAME_STATE[const.WIDTH],
        GAME_STATE[const.HEIGHT]
))
GAME_STATE[const.LEVEL] = LEVEL
GAME_STATE[const.GAME_CLOCK] = pygame.time.Clock()
font = GAME_STATE[const.FONTS][const.FONT_HELVETICA] = pygame.font.SysFont("Helvetica", 16)

CURSOR = [0, 0]


def get_surface(level):
    scroll = GAME_WORLD.state[const.SCROLL]
    surf = Surface((
        GAME_STATE[const.WIDTH],
        GAME_STATE[const.HEIGHT]
    ))
    surf.fill((255, 255, 255))
    for plat in level[const.PLATFORMS]:
        surface = Surface((plat[2], plat[3]))
        surface.fill([(100, 100, 100), (200, 100, 100), (100, 200, 100), (100, 100, 200)][plat[4]])
        surface.blit(font.render("Platform", 0, (0, 0, 0)), (0, 0))
        surf.blit(surface, (plat[0] + scroll[0], plat[1] + scroll[1]))
    return surf

def draw_cursor():
    w = GAME_STATE[const.WIDTH] / 2
    h = GAME_STATE[const.HEIGHT] / 2
    pygame.draw.line(GAME_STATE[const.SCREEN], (255, 0, 0), (w, h), (w+32, h+32), 2)
    pygame.draw.line(GAME_STATE[const.SCREEN], (255, 0, 0), (w, h+32), (w+32, h), 2)
        
    
while True:
    for e in pygame.event.get():
        if e.type == QUIT or e.type == KEYDOWN and e.key == K_ESCAPE: quit()
        if e.type == KEYDOWN:
            if e.key == K_RIGHT: CURSOR[0] -= 32
            if e.key == K_LEFT: CURSOR[0] += 32
            if e.key == K_UP: CURSOR[1] += 32
            if e.key == K_DOWN: CURSOR[1] -= 32

    GAME_WORLD.state[const.SCROLL] = CURSOR
    GAME_STATE[const.SCREEN].blit(get_surface(LEVEL), (0, 0))
    draw_cursor()
    pygame.display.update()
    

    
