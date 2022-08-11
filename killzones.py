import pygame
import pymunk

import entity


class KillZones(entity.Entity):
    def __init__(self, scene) -> None:
        super().__init__(scene)

        dims = self.scene.game.graphics.screen_dims
        self.right_shape = self.make_body((dims.x, 0), (dims.x, dims.y))
        self.left_shape = self.make_body((-1, 0), (-1, dims.y))
        self.back_shape = self.make_body((0, 0), (dims.x, 0))
        self.front_shape = self.make_body((0, dims.y), (dims.x, dims.y))

    def make_body(self, a, b):
        line_moment = pymunk.moment_for_segment(0, a, b, 10)
        line_body = pymunk.Body(1, line_moment, body_type=pymunk.Body.STATIC)
        # line_body.position = a
        line_shape = pymunk.Segment(line_body, a, b, 1)
        self.scene.physics.add(line_body, line_shape)
        return line_shape

    def step(self):
        pass

    def draw_line(self, shape):
        pygame.draw.line(
            self.scene.game.graphics.PRIMARY_SURFACE,
            (255, 0, 0),
            (shape.a.x, shape.a.y),
            (shape.b.x, shape.b.y),
            1,
        )

    def draw(self):
        pass
        # self.draw_line(self.left_shape)
        # self.draw_line(self.right_shape)
        # self.draw_line(self.back_shape)
        # self.draw_line(self.front_shape)
