"""
Red Pants of Die Trying
this time, its personal

the next big blockbuster red pants game, this time no deadlines
STILL NOT WORRYING ABOUT IT
hopefully I can stay motivated

similar to the last one in achitecture but thinking a little more ahead of time,
taking it slow

platforms [(x, y, w, h, idx)]

ideas:
   initial dash for running?

TODO LIST: {x:done,/:working on,.:started,?:thinking,}  
--------------------------
Pixel Art:
    [/] player
       [x] IDLE
       [] CROUCH
       [x] RUN
       [x] SLIDE
       [x] JUMPSQUAT
       [x] RISING
       [x] AIR
       [x] FALLING
       [x] LANDING
       [] FASTFALLING
       [] DIVE
       [] DIVELAND
    [] walls
    [] spikes
    [] enemies
    [] backgrounds
Programming:
    [/] architecture
    [/] player movement
       [x] left right
       [x] jump
       [] fastfall
       [] dive
       [x] gravity
       [x] platform hit detection
    [x] platforms
    [] spikes
    [] enemies
    [] backgrounds
"""
import pygame
from pygame.locals import *
from pygame.rect import Rect
from pygame import Surface

import sys

pygame.init()

#tokens
W="W";H="H";X="X";Y="Y";STATE="STATE";MOV="MOV";JMP="JMP";SPEED="SPEED"
DIR="DIR";TRACTION="TRACTION";X_VEL="X_VEL";Y_VEL="Y_VEL";JMPSPEED="JMPSPEED"
GRAV="GRAV";PLATS="PLATS";ENEMIES="ENEMIES";SPIKES="SPIKES";LVL="LVL"
AIR="AIR";DRIFT="DRIFT";FRAME="FRAME";LANDF="LANDF";JSQUATF="JSQUATF"
SCROLL="SCROLL"
FA="FA"

G = {
    W:960,H:480,
    X:0,Y:0,
    SCROLL:[0, 0],
    X_VEL:0,Y_VEL:0,
    STATE:"IDLE",DIR:1,MOV:0,JMP:0,

    FRAME:0,
    LANDF:2,JSQUATF:2,
    
    SPEED:10,TRACTION:2,DRIFT:2,
    JMPSPEED:-24,GRAV:2,AIR:16,
    
    FA: '-f' not in sys.argv,
}

def scroll(x, y): return x+G[SCROLL][0], y+G[SCROLL][1]
def adjust_scroller():
    G[SCROLL][0] = 0 - G[X] + (G[W]/2) - 16
    G[SCROLL][1] = 0 - G[Y] + (G[H]/2) - 32

DEMO = {
    PLATS:[(-G[W], 400, G[W]*3, 96, 2), (420, 336, 126, 64, 1), (612, 400-126, 64, 126, 1),
           (420-(64*3), 336-126, 64, 64, 1), (420-(64*6), 336-126-64, 126, 64, 1)],
    ENEMIES:[],
    SPIKES:[],
}

G[LVL] = DEMO

SCREEN = pygame.display.set_mode((G[W], G[H]))
pygame.display.set_caption("lookin good")
CLOCK = pygame.time.Clock()
HEL16 = pygame.font.SysFont("Helvetica", 16)

from data import sprites

def drawn_player(G=G): #placeholder untill i have pixel art
    if G[STATE] in sprites: return sprites[G[STATE]]
    f = G[FRAME]
    while f>=0:
        if G[STATE]+":"+str(f) in sprites: return sprites[G[STATE]+":"+str(f)]
        f -= 1
    raise IndexError("no sprite found for player "+G[STATE])

def drawn_platform(plat):
    surf = Surface((plat[2], plat[3]))
    surf.fill([(100, 100, 100), (200, 100, 100), (100, 200, 100), (100, 100, 200)][plat[4]])
    surf.blit(HEL16.render("Platform", 0, (0, 0, 0)), (0, 0))
    return surf


def drawn(G=G):
    surf = Surface((G[W], G[H]))
    surf.fill((255, 255, 255)) #draw background -- later
    for plat in G[LVL][PLATS]: surf.blit(drawn_platform(plat), scroll(plat[0], plat[1]))
    surf.blit(pygame.transform.flip(drawn_player(G), G[DIR]>0, 0), scroll(G[X],G[Y]))
    return surf


def player_state_machine(G=G):
    G[Y_VEL] += G[GRAV]
    G[FRAME] += 1
    if G[STATE] == "IDLE":
        if G[MOV]:
            G[DIR] = G[MOV]
            G[STATE] = "RUN"
            G[FRAME] = 0
    
    if G[STATE] == "RUN":
        G[FRAME] = G[FRAME] % 30
        G[X_VEL] = G[SPEED] * G[DIR]
        if G[MOV] != G[DIR]:
            G[STATE] = "SLIDE"
            G[FRAME] = 0
            
    elif G[STATE] not in ["RISING", "AIR", "FALLING", "FASTFALLING", "DIVE"]:
        if G[X_VEL] > 0: G[X_VEL] = max(G[X_VEL] - G[TRACTION], 0)
        else: G[X_VEL] = min(G[X_VEL] + G[TRACTION], 0)
        
    if G[STATE] == "SLIDE":
        if G[X_VEL] == 0:
            G[STATE] = "IDLE"
            G[FRAME] = 0
        elif G[X_VEL] < 5: G[FRAME] = 1
        else: G[FRAME] = 0
        
    if G[JMP] and G[STATE] not in ["RISING", "AIR", "FALLING", "FASTFALLING", "DIVE"]:
        G[STATE] = "JUMPSQUAT"
        G[FRAME] = 0
    
    if G[STATE] == "JUMPSQUAT" and G[FRAME] >= G[JSQUATF]:
        G[Y_VEL] += G[JMPSPEED]

    if abs(G[Y_VEL]) > G[GRAV]:
        G[STATE] = "AIR"
        G[FRAME] = 0
        
    if G[Y_VEL] < -G[AIR]: 
        G[STATE] = "RISING"
        G[FRAME] = 0

    if G[STATE] == "AIR" and G[MOV]:
        if abs(G[X_VEL] + G[DRIFT] * G[MOV]) <= G[SPEED]: G[X_VEL] += G[DRIFT] * G[MOV]
        if G[X_VEL]: G[DIR] = G[MOV]

    if G[Y_VEL] > G[AIR]:
        G[STATE] = "FALLING"
        G[FRAME] = 0

    if G[STATE] == "LAND":
        if G[FRAME] == G[LANDF]:
            G[STATE] = "IDLE"
            G[FRAME] = 0

    G[JMP] = 0

def hit_detection(G=G):
    #platform hit detection
    plats = [Rect((x, y), (w, h)) for x, y, w, h, idx in G[LVL][PLATS]]
    hitbox = Rect((G[X]+16, G[Y]), (32, 64))
    if G[X_VEL]:
        while hitbox.move(G[X_VEL], 0).collidelist(plats) != -1:
            G[X_VEL] += 1 if G[X_VEL] < 0 else -1
    if G[Y_VEL]:
        flag = G[Y_VEL] > 0
        while hitbox.move(0, G[Y_VEL]).collidelist(plats) != -1:
            G[Y_VEL] += 1 if G[Y_VEL] < 0 else -1
        if flag and not G[Y_VEL]:
            # i dont love changing the state here but it seems fine
            if G[STATE] in ["FALLING", "AIR"]:
                G[STATE] = "LAND"
                G[FRAME] = 0
    if G[X_VEL] and G[Y_VEL]:
        while hitbox.move(G[X_VEL], G[Y_VEL]).collidelist(plats) != -1:
            G[X_VEL] += 1 if G[X_VEL] < 0 else -1
            G[Y_VEL] += 1 if G[Y_VEL] < 0 else -1

def advance_frame(input_get, G=G):
    CLOCK.tick(30)
    adjust_scroller()
    frame_advance = G[FA]
    for e in input_get():
        if e.type == QUIT or e.type == KEYDOWN and e.key == K_ESCAPE: quit()
        if e.type == KEYDOWN:
            if e.key == K_RIGHT: G[MOV] = min(G[MOV] + 1, 1)
            if e.key == K_LEFT: G[MOV] = max(G[MOV] - 1, -1)
            if e.key == K_SPACE: G[JMP] += 1

            if e.key == K_d and "-d" in sys.argv: G[FA] = not G[FA]
            if e.key == K_n: frame_advance = True

        if e.type == KEYUP:
            if e.key == K_RIGHT: G[MOV] -= 1
            if e.key == K_LEFT: G[MOV] -= -1

    
    #state machine -> hit detection -> move
    if frame_advance:
        if not G[FA]: debug()
        player_state_machine(G)
        hit_detection(G)
        G[X] += G[X_VEL]
        G[Y] += G[Y_VEL]
    
gkeys = list(G.keys())
gkeys.sort()
def debug(G=G):
    print("-"*20)
    for key in gkeys:
        print(key + " | ", G[key])
        
while __name__ == """__main__""":
    advance_frame(pygame.event.get)
    SCREEN.blit(drawn(), (0, 0))
    pygame.display.update()

