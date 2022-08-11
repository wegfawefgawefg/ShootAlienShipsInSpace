import pygame
from pygame import Vector2
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_a, K_s, K_d, K_f

import controller
from bullet import Bullet


class BulletController(controller.Controller):
    def __init__(self, scene, ship):
        super().__init__(scene)

        self.ship = ship

    def control(self, key, press):
        if key in [
            K_LEFT,
            K_RIGHT,
            K_UP,
            K_DOWN,
        ]:
            return

        if key not in [K_a, K_s, K_d, K_f]:
            return
        if press and key == K_f:
            ship_pos = self.ship.get_pos()
            Bullet(self.scene, Vector2(ship_pos.x, ship_pos.y), 1)

    def step(self):
        pass
