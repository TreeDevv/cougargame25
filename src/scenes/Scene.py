import pygame
import random
class Scene:
    def clamp(self, v):
        return max(0, min(255, v))

    def create_dithered_surface(self):
        width, height = pygame.display.get_window_size()
        noise = pygame.Surface((width, height))
        base = (30, 100, 200)
        
        for x in range(0, width, 4):
            for y in range(0, height, 4):
                shade = 30 if random.random() < 0.5 else -30
                r = self.clamp(base[0] + shade)
                g = self.clamp(base[1] + shade)
                b = self.clamp(base[2] + shade)
                noise.fill((r, g, b), (x, y, 4, 4))
        return noise
    def handle_events(self, events):
        pass;
    def update(self, dt: float):
        pass;
    def render(self, screen):
        pass;