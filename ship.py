from pygame import Vector2

from entity import Entity


class Ship(Entity):
    def __init__(self, scene):
        super().__init__(scene)

        self.vel = Vector2(0.0, 0.0)
        self.pos = self.scene.game.graphics.screen_dims.elementwise() * Vector2(0.5, 0.8)

    def step(self):
        dt = self.scene.game.dt
        self.pos = self.pos.elementwise() + self.vel * dt
        self.vel = self.vel * 0.99 * (1.0 - dt)

        x_max = self.scene.game.graphics.screen_dims.x
        y_max = self.scene.game.graphics.screen_dims.y
        if self.pos.y >= y_max:
            self.pos.y = y_max
            self.vel.y = 0.0

        if self.pos.x < 0:
            self.pos.x = 0
            self.vel.x = 0
        elif self.pos.x > x_max:
            self.pos.x = x_max
            self.vel.x = 0

    def fly(self, dir):
        print(f"flying {dir}")
        self.vel += dir * 2.0

    def draw(self):
        sprite = 1
        if self.vel.x <= -10:
            sprite = 0
        if self.vel.x >= 10:
            sprite = 2

        self.scene.game.graphics.draw_sprite(
            self.scene.game.sprite_sheets.ships,
            sprite, self.pos.x, self.pos.y)
