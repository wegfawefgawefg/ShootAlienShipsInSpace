import math
from pprint import pprint
import random

import math
import pygame
from pygame import Vector2
from pygame.locals import (
    K_q,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_f,
)

SCREEN_DIMS = Vector2(240, 160) / 2
WINDOW_DIMS = SCREEN_DIMS * 8.0

PRIMARY_SURFACE = None
WINDOW = None
SHIP_SPRITES = None
PARTICLE_SPRITES = None


class SpriteSheet:
    def __init__(self, path, width, height, sprite_width, sprite_height):
        self.path = path
        self.sheet = pygame.image.load(path)  # .convert_alpha()
        self.width, self.height, self.sprite_width, self.sprite_height = width, height, sprite_width, sprite_height
        self.half_sprite_width = sprite_width // 2
        self.half_sprite_height = sprite_height // 2

    def draw_sprite(self, tile, x, y):
        x, y = int(x), int(y)
        tile = tile % (self.width * self.height)
        PRIMARY_SURFACE.blit(self.sheet, (x - self.half_sprite_width, y -
                                          self.half_sprite_height), self.get_tile_area(tile))

    def get_tile_area(self, i):
        y = math.floor(i / self.width)
        py = y * self.sprite_height
        x = i % self.width
        px = x * self.sprite_width
        return (px, py, self.sprite_width, self.sprite_height)

    def __repr__(self) -> str:
        return self.path


BULLETS = []


class Bullet:
    ID = 0
    SPEED = 1

    def __init__(self, x, y, t) -> None:
        self.creation_time = pygame.time.get_ticks()
        self.id = Bullet.ID
        Bullet.ID += 1

        self.moving = False
        self.x, self.y, self.t = x, y - 8, t
        BULLETS.append(self)

    def step(self):
        if self.moving:
            self.y -= Bullet.SPEED
        if self.y < 0:
            # remove yourself from the bullet list
            for i in range(len(BULLETS)):
                bullet = BULLETS[i]
                if bullet.id == self.id:
                    BULLETS.pop(i)
                    break

    def charge(self, t):
        self.t = min(11, (t - self.creation_time) // 50)

    def release(self):
        self.moving = True

    def draw(self):
        PARTICLE_SPRITES.draw_sprite(self.t, self.x, self.y)


def main():
    pygame.init()
    global PRIMARY_SURFACE
    global WINDOW
    global SHIP_SPRITES
    global PARTICLE_SPRITES

    PRIMARY_SURFACE = pygame.Surface(SCREEN_DIMS)
    WINDOW = pygame.display.set_mode(WINDOW_DIMS)

    pygame.mouse.set_visible(False)
    # window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    SHIP_SPRITES = SpriteSheet("./ships.png", 10, 10, 8, 8)
    PARTICLE_SPRITES = SpriteSheet("./particles.png", 6, 10, 8, 8)

    clock = pygame.time.Clock()
    running = True

    press = 100

    key_to_charging_bullet = {}
    presstimes = {}
    while running:
        t = pygame.time.get_ticks()

        mt = pygame.mouse.get_pos()
        m = (Vector2(mt[0], mt[1]).elementwise() /
             WINDOW_DIMS).elementwise() * SCREEN_DIMS

        for event in pygame.event.get():
            if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                if event.key in [K_ESCAPE, K_q]:
                    running = False

                name = pygame.key.name(event.key)
                if event.type == pygame.KEYDOWN:
                    presstimes[name] = t
                    new_bullet = Bullet(m.x, m.y - 8, 0)
                    key_to_charging_bullet[name] = new_bullet

                elif event.type == pygame.KEYUP:
                    d = t - presstimes[name]
                    del presstimes[name]

                    if d < press:
                        print(f"{name} - pressed")
                    else:
                        print(f"{name} - released after - {d}s")

                    if name in key_to_charging_bullet:
                        key_to_charging_bullet[name].release()
                        del key_to_charging_bullet[name]

            if event.type == pygame.QUIT:
                running = False

        # launch holds
        # for key_name in presstimes:
        #     d = t - presstimes[key_name]
        #     if d > press:
        #         print(f"{key_name} - held for - {d}s")
        #         if name in key_to_charging_bullet:
        #             bullet = key_to_charging_bullet[key_name]
        #             bullet.charge(t)
        #             bullet.x = m.x
        #             bullet.y = m.y - 8
        #         else:
        #             key_to_charging_bullet[name] = Bullet(m.x, m.y, 0)

        PRIMARY_SURFACE.fill((0, 0, 0))

        SHIP_SPRITES.draw_sprite(1, m.x, m.y)

        for bullet in BULLETS:
            bullet.step()
            bullet.draw()

        blit = pygame.transform.scale(PRIMARY_SURFACE, WINDOW.get_size())
        WINDOW.blit(blit, (0, 0))
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
