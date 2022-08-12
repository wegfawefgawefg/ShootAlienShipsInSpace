import random
import pygame
import pymunk

import entity
from enums import CollisionType


def kill_entity(arbiter, space, data):
    killable_shape = arbiter.shapes[1]
    if hasattr(killable_shape, "entity"):
        e = killable_shape.entity
        e.scene.remove_entity(e)
        # random.choice(e.scene.game.sounds.rock_hit_by_laser).play()

    return True

class KillZones(entity.Entity):
    def __init__(self, scene) -> None:
        super().__init__(scene)

        dims = self.scene.game.graphics.screen_dims
        self.right_shape = self.make_body((dims.x, 0), (dims.x, dims.y))
        self.left_shape = self.make_body((-1, 0), (-1, dims.y))
        self.back_shape = self.make_body((0, 0), (dims.x, 0))
        self.front_shape = self.make_body((0, dims.y), (dims.x, dims.y))

        shapes = [self.right_shape, self.left_shape, self.back_shape, self.front_shape]

        for shape in shapes:
            shape.collision_type = CollisionType.KILL_ZONE.value
            self.scene.physics.add_collision_handler(
                CollisionType.KILL_ZONE.value, CollisionType.BULLET.value).begin = kill_entity
            self.scene.physics.add_collision_handler(
                CollisionType.KILL_ZONE.value, CollisionType.DEBRIS.value).begin = kill_entity


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
