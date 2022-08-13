import random
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

    def draw_sprite(self, sprite_sheet, tile, x, y):
        x, y = int(x), int(y)
        tile = tile % (sprite_sheet.width * sprite_sheet.height)
        self.primary_surface.blit(
            sprite_sheet.sheet,
            (x - sprite_sheet.half_sprite_width, y - sprite_sheet.half_sprite_height),
            sprite_sheet.get_tile_area(tile),
        )

    def get_random_place_on_screen(self):
        return Vector2(
            random.randint(0, self.screen_dims.x), 
            random.randint(0, self.screen_dims.y))
