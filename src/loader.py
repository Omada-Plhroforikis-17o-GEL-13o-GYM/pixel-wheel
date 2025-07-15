import pygame
import time
import os
from .tleng2.engine.properties import RendererProperties
from .tleng2.utils.utils import get_parent_dir

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

        # Load logo image
        assets_dir = os.path.join(get_parent_dir(__file__, 2), "assets")
        print(assets_dir)
        logo_path = os.path.join(assets_dir, "logo", "pixel_wheel_whole_logo.png")
        self.logo_img = pygame.image.load(logo_path).convert_alpha()
        # Scale logo if needed
        max_logo_width = 300
        if self.logo_img.get_width() > max_logo_width:
            scale = max_logo_width / self.logo_img.get_width()
            new_size = (int(self.logo_img.get_width() * scale), int(self.logo_img.get_height() * scale))
            self.logo_img = pygame.transform.smoothscale(self.logo_img, new_size)

        # Load Tleng2 logo
        tleng2_logo_path = os.path.join(assets_dir, "logo", "tleng2_logo.png")
        self.tleng2_logo = pygame.image.load(tleng2_logo_path).convert_alpha()
        # Scale Tleng2 logo if needed
        max_tleng2_width = 48
        if self.tleng2_logo.get_width() > max_tleng2_width:
            scale = max_tleng2_width / self.tleng2_logo.get_width()
            new_size = (int(self.tleng2_logo.get_width() * scale), int(self.tleng2_logo.get_height() * scale))
            self.tleng2_logo = pygame.transform.smoothscale(self.tleng2_logo, new_size)

        # Load font
        font_path = os.path.join(assets_dir, "Font", "megamax-jonathan-too-font", "MegamaxJonathanToo-YqOq2.ttf")  # Replace with your font filename
        self.font = pygame.font.Font(font_path, 22)

    def draw(self):
        self.display.fill(self.bg_color)
        # Draw logo above the bar
        logo_rect = self.logo_img.get_rect(midbottom=(self.display.get_width() // 2, self.bar_y - 20))
        self.display.blit(self.logo_img, logo_rect)

        # Draw bar background
        pygame.draw.rect(self.display, self.bar_bg_color, (self.bar_x, self.bar_y, self.bar_width, self.bar_height))
        # Draw bar foreground (animated)
        fill_width = int(self.bar_width * self.progress)
        pygame.draw.rect(self.display, self.bar_fg_color, (self.bar_x, self.bar_y, fill_width, self.bar_height))

        # Draw "Powered by the Tleng2 Engine" text and logo at bottom right
        text = "Powered by the Tleng2 Engine"
        text_surf = self.font.render(text, True, (200, 200, 200))
        text_rect = text_surf.get_rect()
        margin = 16
        logo_margin = 8
        # Position: bottom right, with some margin
        x = self.display.get_width() - text_rect.width - self.tleng2_logo.get_width() - logo_margin - margin
        y = self.display.get_height() - max(text_rect.height, self.tleng2_logo.get_height()) - margin
        self.display.blit(text_surf, (x, y))
        # Tleng2 logo to the right of the text
        self.display.blit(self.tleng2_logo, (x + text_rect.width + logo_margin, y + (text_rect.height - self.tleng2_logo.get_height()) // 2))

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        self.progress = 0.0
        self.draw()  # <-- Force initial draw
        pygame.event.pump()  # Let the OS process window events
        total = len(self.scenes_to_load)
        for idx, (scene_cls, scene_name) in enumerate(self.scenes_to_load):
            scene = scene_cls(scene_name)
            self.loaded_scenes.append(scene)
            self.target_progress = (idx + 1) / total

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
        self.progress = 1.0
        self.draw()
        time.sleep(0.5)  # Pause before switching scenes