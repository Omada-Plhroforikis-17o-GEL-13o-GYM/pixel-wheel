import pygame
import time
from .tleng2.engine.properties import RendererProperties

def lerp(a, b, t):
    return a + (b - a) * t

class LoadingScene:
    def __init__(self, scenes_to_load):
        self.display = RendererProperties._window
        self.scenes_to_load = scenes_to_load
        self.loaded_scenes = []
        self.progress = 0.0  # 0.0 to 1.0
        self.target_progress = 0.0
        self.bar_width = 400
        self.bar_height = 40
        self.bar_x = (self.display.get_width() - self.bar_width) // 2
        self.bar_y = (self.display.get_height() - self.bar_height) // 2
        self.bg_color = (30, 30, 30)
        self.bar_bg_color = (80, 80, 80)
        self.bar_fg_color = (0, 200, 0)
        self.animation_speed = 0.15  # Lerp speed

    def draw(self):
        self.display.fill(self.bg_color)
        # Draw bar background
        pygame.draw.rect(self.display, self.bar_bg_color, (self.bar_x, self.bar_y, self.bar_width, self.bar_height))
        # Draw bar foreground (animated)
        fill_width = int(self.bar_width * self.progress)
        pygame.draw.rect(self.display, self.bar_fg_color, (self.bar_x, self.bar_y, fill_width, self.bar_height))
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        self.progress = 0.0
        self.draw()  # <-- Force initial draw
        pygame.event.pump()  # Let the OS process window events
        # Now continue with loading...
        total = len(self.scenes_to_load)
        for idx, (scene_cls, scene_name) in enumerate(self.scenes_to_load):
            # Actually load/initialize the scene
            scene = scene_cls(scene_name)
            self.loaded_scenes.append(scene)
            self.target_progress = (idx + 1) / total

            # Animate the bar to the new target
            while abs(self.progress - self.target_progress) > 0.01:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                self.progress = lerp(self.progress, self.target_progress, self.animation_speed)
                self.draw()
                clock.tick(60)
            self.progress = self.target_progress
            self.draw()
            time.sleep(0.1)
        # Ensure bar is full at the end
        self.progress = 1.0
        self.draw()
        time.sleep(0.5)  # Pause before switching scenes

# Example usage:
# from loader import LoadingScene
# loading_scene = LoadingScene([
#     (FreeRoam, 'Free Roam'),
#     (Menu, 'Menu'),
#     (Credits, 'Credits')
# ])
# loading_scene.run()