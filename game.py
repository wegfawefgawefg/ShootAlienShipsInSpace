from enum import Enum, auto

import pygame
from pygame import Vector2

from graphics import Graphics
from images import Images
from sprite_sheets import SpriteSheets
from sounds import Sounds
from music import Music
from main_menu import MainMenu


class Game:
    PRESS_THRESHOLD = 100

    def __init__(self) -> None:
        pygame.init()
        self.time = 0  # time

        self.graphics = Graphics()
        self.images = Images()
        self.sprite_sheets = SpriteSheets()
        self.sounds = Sounds()
        self.music = Music()

        self.scene = MainMenu(self)

    def set_scene(self, scene):
        del self.scene
        self.scene = scene

    def quit(self):
        self.running = False

    def get_mouse_position(self):
        wm = pygame.mouse.get_pos()
        return (
            Vector2(wm[0], wm[1]).elementwise()
            / self.graphics.window_dims).elementwise() \
            * self.graphics.screen_dims

    def run(self):
        last_time = pygame.time.get_ticks()
        self.running = True
        while self.running:
            self.time = pygame.time.get_ticks()
            self.dt = (self.time - last_time) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                else:
                    self.scene.control(event)
            if self.running == False:
                break
            self.scene.step()
            self.scene.draw()

            blit = pygame.transform.scale(
                self.graphics.primary_surface, self.graphics.window.get_size())
            self.graphics.window.blit(blit, (0, 0))
            pygame.display.flip()
        pygame.quit()
