from pygame.locals import (
    K_SPACE
)

import controller


class WarpController(controller.Controller):
    def __init__(self, scene, star_field):
        super().__init__(scene)

        self.star_field = star_field
        self.warping = False

    def control(self, key, press):
        if key == K_SPACE:
            if press:
                self.warping = True
                self.scene.game.sounds.start_warp.play()
            else:
                self.warping = False
                self.warp_level = 0.0
                self.scene.game.sounds.stop_warp.play()

    def step(self):
        dt = self.scene.game.dt
        if self.warping:
            self.star_field.warp_level += dt * 0.00001
            self.star_field.warp_level = min(20.0, self.star_field.warp_level)
            for _ in range(10):
                self.star_field.new_star()
        else:
            self.star_field.warp_level = max(
                self.star_field.warp_level*0.99,
                0.0)
