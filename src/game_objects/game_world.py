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
        
        for plat in game_state[const.LEVEL][const.PLATFORMS]:
            platform_surface = self.__get_platform_surface(game_state, plat)
            platform_position = self.__get_board_position(plat[0], plat[1])

            game_world_surface.blit(platform_surface, platform_position)

        for spike in game_state[const.LEVEL][const.SPIKES]:
            spike_surface = self.__get_spike_surface(game_state, spike)
            spike_position = self.__get_board_position(spike[0], spike[1])

            game_world_surface.blit(spike_surface, spike_position)

        for actor in game_state[const.LOADED_ACTORS]:
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
        # placeholder
        font = game_state[const.FONTS][const.FONT_HELVETICA]
        surface = Surface((plat[2], plat[3]))

        surface.fill([(100, 100, 100), (200, 100, 100), (100, 200, 100), (100, 100, 200)][plat[4]])
        surface.blit(font.render("Platform", 0, (0, 0, 0)), (0, 0))

        return surface

    def __get_spike_surface(self, game_state, spike):
        # placeholder
        font = game_state[const.FONTS][const.FONT_HELVETICA]
        surface = Surface((32, 32))

        surface.fill((255, 100, 100))
        surface.blit(font.render("Spike", 0, (0, 0, 0)), (0, 0))

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

