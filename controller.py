class Controller:
    def __init__(self, scene):
        self.scene = scene

    def control(self, key, press):
        raise NotImplementedError

    def step(dt):
        raise NotImplementedError
