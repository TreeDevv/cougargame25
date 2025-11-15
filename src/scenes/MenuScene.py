import pygame

from src.ui.TextBox import TextBox
from src.ui.TextLabel import TextLabel
from src.util.math import relative_to_pixel, anchor_center
from src.scenes.Scene import Scene

class MenuScene(Scene):
    def __init__(self, game):
        self.game = game;
        self.font = pygame.font.SysFont("Arial", 24);
        self.title_label = TextLabel("HomoGraphio", self.font, (255, 255, 255), (0, 0.5, 0, 0.15), (0.5, 0.5))
        self.title_box = TextBox(self.font, (255, 255, 255), (128, 0, 128), (0, 0.5, 0, 0.75), (400, 0, 50, 0), (0.5, 0.5))
        self.title_box.set_text("Create a lobby");

    def handle_events(self, events):
        pass;
    def update(self, dt: float):
        pass;
    def render(self, screen):
        screen.fill((25, 100, 50));
        # Render the ui elements in scene
        screen.blit(self.title_label.get_surface(), self.title_label.get_pos());
        screen.blit(self.title_box.get_surface(), self.title_box.get_pos());
