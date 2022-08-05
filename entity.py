class Entity:
    def __init__(self, scene):
        self.scene = scene

    def step(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError
