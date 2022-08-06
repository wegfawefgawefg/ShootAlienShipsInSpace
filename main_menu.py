import math

import pygame
from pygame.locals import (
    K_q, K_ESCAPE,
)

from scene import Scene
from space_battle import SpaceBattle


class MainMenu(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.game.music.main_menu_song.play(loops=-1)

        self.double_screen_dims = game.graphics.screen_dims * 2.0

        self.game.graphics.primary_surface = pygame.Surface(
            self.double_screen_dims)

        background_size = self.double_screen_dims * 1.2
        self.background = pygame.transform.scale(
            self.game.images.main_menu_background, (background_size.x, background_size.y))

        title_size = self.double_screen_dims * 1.2
        self.title = pygame.transform.scale(
            self.game.images.main_menu_title, (title_size.x, title_size.y))

        title_shadow_size = title_size * 1.1
        self.title_shadow = pygame.transform.scale(
            self.game.images.main_menu_title, (title_shadow_size.x, title_shadow_size.y))
        self.title_shadow.fill(
            (0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.title_shadow.set_alpha(220)

    def control(self, event):
        if event.type == pygame.KEYDOWN and event.key in [K_ESCAPE, K_q]:
            self.game.quit()
            return

            # self.game.music.main_menu_song.stop()
            # self.game.graphics.primary_surface = pygame.Surface(
            #     self.game.graphics.screen_dims)
            # self.game.set_scene(SpaceBattle(self.game))

    def step(self):
        pass

    def draw(self):
        self.game.graphics.primary_surface.fill((0, 0, 0))

        offset = self.double_screen_dims.y / 10.0
        background_y = 0.3*math.sin(self.game.time*0.003)*offset - offset * 1.5
        background_x = 0.3 * \
            math.sin(self.game.time*0.0013)*offset - offset * 1.5
        self.game.graphics.primary_surface.blit(
            self.background, (background_x, background_y))

        t_o = -self.double_screen_dims * 0.1

        title_y = 0.5 + math.sin(self.game.time*0.001)*0.5
        title_y *= self.double_screen_dims.y * 0.05
        title_y -= title_y * 0.5

        self.game.graphics.primary_surface.blit(
            self.title_shadow, (t_o.x, title_y+t_o.y))
        self.game.graphics.primary_surface.blit(
            self.title, (t_o.x - t_o.x * 0.4, title_y+t_o.y - t_o.y * 0.2))
