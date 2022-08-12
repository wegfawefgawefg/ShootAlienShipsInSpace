class Controller:
    def __init__(self, scene):
        self.scene = scene
        scene.add_controller(self)

    def control(self, key, press):
        raise NotImplementedError

    def step():
        raise NotImplementedError
