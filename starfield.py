import random

from pygame import Vector2

import entity

'''
add graphics
add constants holder
'''


class StarField(entity.Entity):
    def __init__(self, scene):
        super().__init__(scene)

        self.warp_level = 10.0
        self.stars = []
        for _ in range(200):
            y = random.random() * self.game.graphics.SCREEN_DIMS.y * \
                2.0 - self.game.graphics.SCREEN_DIMS.y // 2
            self.new_star(y)

    def new_star(self, y=None):
        center_x = self.game.graphics.SCREEN_DIMS.x / 2.0
        y = y if y else -(self.game.graphics.SCREEN_DIMS.y // 2)
        p = Vector2(self.game.graphics.SCREEN_DIMS.x *
                    random.random() * 2.0, y)
        p.x -= self.game.graphics.SCREEN_DIMS.x // 2.0
        vy = (20.0 + (abs((center_x - p.x)) * 0.08) ** 2.0)
        v = self.game.graphics.Vector2(0.0, vy)
        new_star = Star(p, v)
        self.stars.append(new_star)

    def step(self, dt):
        if random.random() > 0.5:
            self.new_star()

        for star in self.stars:
            star.step(dt * (1.0 + self.warp_level))
            if star.pos.y >= (self.game.graphics.SCREEN_DIMS.y * 1.5):
                self.remove(star)

    def remove(self, star):
        for i in range(len(self.stars)):
            s = self.stars[i]
            if star.id == s.id:
                self.stars.pop(i)
                break

    def draw(self):
        ship = self.scene.ship
        c = self.game.graphics.SCREEN_DIMS / 2.0
        for star in self.stars:
            offset = (c.elementwise() - ship.pos) / 2
            star.draw(offset)


class Star:
    ID = 0

    def __init__(self, pos, vel):

        self.id = Star.ID
        Star.ID += 1
        self.pos = Vector2(pos.x, pos.y)
        self.vel = Vector2(vel.x, vel.y)

    def step(self, dt):
        self.pos += self.vel * self.scene.dt

    def draw(self, offset):
        p = offset + self.pos
        self.game.assets.PARTICLE_SPRITES.draw_sprite(28, p.x, p.y)
