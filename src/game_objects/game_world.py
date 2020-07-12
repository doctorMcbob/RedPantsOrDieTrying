"""
Main game board logic
"""

import pygame

from pygame import (
    Rect,
    Surface,
)

from src.const import GameConstants as const
from src.game_objects.game_object import GameObject
from src.lib.sprite_manager.sprite_sheet import load_sprite_sheet
from src.lib.utils import is_near

class GameWorld(GameObject):
    def __init__(self, game_world_state_template):
        super(GameWorld, self).__init__(game_world_state_template)

    def update_state(self, game_state, player_one):
        player_one_state = player_one.get_state()

        scroll_state = self.state[const.SCROLL]
        player_one_x = player_one_state[const.X_COORD]
        player_one_y = player_one_state[const.Y_COORD]

                
        board_width = game_state[const.WIDTH]
        board_height = game_state[const.HEIGHT]

        scroll_state[0] = 0 - player_one_x + board_width / 2 - 16
        scroll_state[1] = 0 - player_one_y + board_height / 2 - 32

    def get_surface(self, game_state, player_one):
        game_width = game_state[const.WIDTH]
        game_height = game_state[const.HEIGHT]
        game_world_surface = Surface((game_width, game_height))

        game_world_surface.fill((255, 255, 255)) #draw background -- later

        # right now, platforms and spikes are static, 
        # eventually more complex game objects will handle their own sprite sheets
        
        for plat in filter(lambda p: is_near(game_state, self, Rect((p[0], p[1]), (p[2], p[3]))), game_state[const.LEVEL][const.PLATFORMS]):
            platform_surface = self.__get_platform_surface(game_state, plat)
            platform_position = self.__get_board_position(plat[0], plat[1])

            game_world_surface.blit(platform_surface, platform_position)

        for spike in filter(lambda s: is_near(game_state, self, Rect((s[0], s[1]), (32, 32))), game_state[const.LEVEL][const.SPIKES]):
            spike_surface = self.__get_spike_surface(game_state, spike)
            spike_position = self.__get_board_position(spike[0], spike[1])

            game_world_surface.blit(spike_surface, spike_position)

        for actor in filter(lambda a: is_near(game_state, self, Rect(
                (a.state[const.X_COORD], a.state[const.Y_COORD]), (a.state[const.WIDTH], a.state[const.HEIGHT]))
        ), game_state[const.LOADED_ACTORS]):
            actor_surface = actor.get_surface(game_state)
            actor_position = self.__get_board_position(actor.state[const.X_COORD], actor.state[const.Y_COORD])

            game_world_surface.blit(actor_surface, actor_position)
        
        self.__draw_player(game_state, game_world_surface, player_one)

        return game_world_surface

    def __get_board_position(self, x_pos, y_pos):
        """Get new position coordinats based off of current position coordinates and board state"""
        scroll_state = self.state[const.SCROLL]

        return (x_pos + scroll_state[0], y_pos + scroll_state[1])

    def __get_platform_surface(self, game_state, plat):
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
            font = game_state[const.FONTS][const.FONT_HELVETICA]
             
            surface.fill([(100, 100, 100), (200, 100, 100), (100, 200, 100), (100, 100, 200)][plat[4]])
            surface.blit(font.render("Platform", 0, (0, 0, 0)), (0, 0))

        surface.set_colorkey((1, 255, 1))
        return surface

    def __get_spike_surface(self, game_state, spike):
        surface = load_sprite_sheet("spike")['spike']

        surface = pygame.transform.rotate(surface, spike[2] * 90)

        return surface

    def __draw_player(self, game_state, game_world_surface, player):
        player_one_surface = player.get_surface(game_state)
        player_one_state = player.get_state()
        player_one_direction = player_one_state[const.DIRECTION]
        player_one_x_pos = player_one_state[const.X_COORD]
        player_one_y_pos = player_one_state[const.Y_COORD]

        game_world_surface.blit(
            pygame.transform.flip(player_one_surface, player_one_direction > 0, 0),
            self.__get_board_position(player_one_x_pos, player_one_y_pos)
        )
