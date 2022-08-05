import pygame
from pygame import Vector2


class Graphics:
    def __init__(self) -> None:
        self.screen_dims = Vector2(240, 160)
        self.window_dims = self.screen_dims * 4.0

        self.primary_surface = pygame.Surface(self.screen_dims)
        self.window = pygame.display.set_mode(self.window_dims)
        # self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        pygame.mouse.set_visible(False)
