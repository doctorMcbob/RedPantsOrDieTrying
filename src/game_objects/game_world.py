"""
Main game board logic
"""

import pygame

from pygame import (
    Rect,
    Surface,
)

from const import GameConstants as const
from src.game_objects.game_object import GameObject

class GameWorld(GameObject):
    def __init__(self, game_world_state_template):
        super(GameWorld, self).__init__(game_world_state_template)

    def get_board_position(self, x_pos, y_pos):
        """Get new position coordinats based off of current position coordinates and board state"""
        scroll_state = self.state[const.SCROLL]

        return (x_pos + scroll_state[0], y_pos + scroll_state[1])

    def get_platform_surface(self, game_state, plat):
        font = game_state[const.FONTS][const.FONT_HELVETICA]
        surface = Surface((plat[2], plat[3]))

        surface.fill([(100, 100, 100), (200, 100, 100), (100, 200, 100), (100, 100, 200)][plat[4]])
        surface.blit(font.render("Platform", 0, (0, 0, 0)), (0, 0))

        return surface

    def draw_player(self, game_state, game_world_surface, player):
        player_one_surface = player.get_surface(game_state)
        player_one_state = player.get_state()
        player_one_direction = player_one_state[const.DIRECTION]
        player_one_x_pos = player_one_state[const.X_COORD]
        player_one_y_pos = player_one_state[const.Y_COORD]

        game_world_surface.blit(
            pygame.transform.flip(player_one_surface, player_one_direction > 0, 0),
            self.get_board_position(player_one_x_pos, player_one_y_pos)
        )

    def get_surface(self, game_state, player_one):
        game_width = game_state[const.WIDTH]
        game_height = game_state[const.HEIGHT]
        game_world_surface = Surface((game_width, game_height))

        game_world_surface.fill((255, 255, 255)) #draw background -- later

        for plat in game_state[const.LEVEL][const.PLATFORMS]:
            platform_surface = self.get_platform_surface(game_state, plat)
            platform_position = self.get_board_position(plat[0], plat[1])

            game_world_surface.blit(platform_surface, platform_position)

        self.draw_player(game_state, game_world_surface, player_one)

        return game_world_surface

    def update_state(self, game_state, player_one):
        player_one_state = player_one.get_state()

        scroll_state = self.state[const.SCROLL]
        player_one_x = player_one_state[const.X_COORD]
        player_one_y = player_one_state[const.Y_COORD]
        board_width = game_state[const.WIDTH]
        board_height = game_state[const.HEIGHT]

        scroll_state[0] = 0 - player_one_x + board_width / 2 - 16
        scroll_state[1] = 0 - player_one_y + board_height / 2 - 32
