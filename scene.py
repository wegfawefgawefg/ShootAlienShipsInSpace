import pymunk
import pygame
from pygame.locals import (
    K_q,
    K_ESCAPE,
)

class Scene:
    def __init__(self, game) -> None:
        self.game = game
        self.physics = None
        self.entities = None
        self.controllers = None

    def control(self, event):
        if self.controllers:
            if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                for controller in self.controllers:
                    controller.control(event.key, press=(event.type == pygame.KEYDOWN))

    def step(self):
        if self.controllers:
            for controller in self.controllers:
                controller.step()
        if self.physics:
            self.physics.step(self.game.dt)
        if self.entities:
            for entity in self.entities:
                entity.step()

    def draw(self):
        if self.entities:
            for entity in self.entities:
                entity.draw()

    def add_controller(self, controller):
        if not self.controllers:
            self.controllers = []
        self.controllers.append(controller)
        return controller

    def create_physics(self):
        if not self.physics:
            self.physics = pymunk.Space()

    def add_entity(self, entity):
        if not self.entities:
            self.entities = []
        self.entities.append(entity)
        return entity

    def remove_entity(self, entity):
        for i in range(len(self.entities)):
            iie = self.entities[i]
            if iie.id == entity.id:
                self.entities.pop(i)
                entity.remove_physics_objects()
                break

        if entity.physics_objects:
            for physics_object in entity.physics_objects:
                # self.physics.remove(self.shape, self.shape.body)
                self.physics.remove(physics_object)