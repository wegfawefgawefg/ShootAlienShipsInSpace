class Scene:
    def __init__(self, game) -> None:
        self.game = game

    def control(self, event):
        raise NotImplementedError

    def step(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError
