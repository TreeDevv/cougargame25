import random
import pygame
import thorpy as tp

from src.util.math import relative_to_pixel, anchor_center
from src.scenes.Scene import Scene

def create_dithered_surface():
    noise = pygame.Surface(pygame.display.get_window_size())
    for x in range(0, noise.get_size()[0], 4):
        for y in range(0, noise.get_size()[1], 4):
            shade = 30 if random.random() < 0.5 else -30
            color = (128 + shade, 20, 128 + shade)   # small color jitter
            noise.fill(color, (x, y, 4, 4))
    return noise

class MenuScene(Scene):
    def __init__(self, game):
        self.game = game;
        self.title_font = pygame.font.Font("assets/fonts/StarCrush.ttf", 64);
        self.font = pygame.font.Font("assets/fonts/StarCrush.ttf", 24);
    
        self.title_label = tp.Text("Homographio", font_size=64)
        self.title_label.center_on(pygame.display.get_surface().get_rect())

        title_label_pos = relative_to_pixel((0.5, 0.2))
        self.title_label.set_center(title_label_pos[0], title_label_pos[1])

        self.join_code_input = tp.TextInput("", placeholder="Enter Join Code")
        join_code_pos = relative_to_pixel((0.5, 0.4))
        self.join_code_input.set_center(join_code_pos[0], join_code_pos[1])

        def focus_box():
            self.join_code_input.focus()
        self.join_code_input.default_at_click = focus_box

        self.create_lobby_button = tp.Button("Create Lobby")
        self.create_lobby_button.set_bck_color((128, 0, 128))
        create_lobby_pos = relative_to_pixel((0.5, 0.5))
        self.create_lobby_button.set_center(create_lobby_pos[0], create_lobby_pos[1])
    def handle_events(self, events):
        pass;
    def update(self, dt: float):
        self.join_code_input.update(pygame.mouse.get_pos());
    def render(self, screen):
        screen.fill((25, 100, 50));
        noise = create_dithered_surface()
        noise.set_alpha(40)
        screen.blit(noise, (0, 0))

        self.title_label.draw()
        self.join_code_input.draw()
        self.create_lobby_button.draw()
        # Render the ui elements in scene
