from pygame import Vector2
import pymunk
from pymunk.vec2d import Vec2d as pvec2

from entity import Entity


class Ship(Entity):
    def __init__(self, scene):
        super().__init__(scene)

        mass = 1
        radius = 3
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)

        pos = self.scene.game.graphics.screen_dims.elementwise() * Vector2(0.5, 0.8)
        body.position = pos.x, pos.y
        self.shape = pymunk.Circle(body, radius, pvec2(0, 0))

        self.scene.physics.add(body, self.shape)

    def get_pos(self):
        return self.shape.body.position

    def get_vel(self):
        return self.shape.body.velocity

    def step(self):
        opposite = -self.shape.body.velocity * 10.0
        self.shape.body.apply_force_at_local_point(opposite)

    def fly(self, dir):
        d = dir * 1200.0
        vfrom = pvec2(d.x, d.y)
        self.shape.body.apply_force_at_local_point(vfrom)

    def draw(self):
        vel = self.get_vel()
        sprite = 1
        if vel.x <= -10:
            sprite = 0
        if vel.x >= 10:
            sprite = 2
        p = self.get_pos()
        self.scene.game.graphics.draw_sprite(
            self.scene.game.sprite_sheets.ships,
            sprite, p.x, p.y)
