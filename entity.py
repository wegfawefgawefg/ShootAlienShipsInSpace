class Entity:
    ID = 0
    def __init__(self, scene):
        self.scene = scene
        self.scene.add_entity(self)

        self.id = Entity.ID
        Entity.ID += 1
        self.physics_objects = None

    def step(self):
        raise NotImplementedError

    def remove_physics_objects(self):
        if self.physics_objects:
            for physics_object in self.physics_objects:
                self.scene.physics.remove(physics_object)

    def draw(self):
        raise NotImplementedError

    def add_physics_object(self, physics_object):
        if not self.physics_objects:
            self.physics_objects = []
        self.physics_objects.append(physics_object)
        return physics_object
