import pygame

from src.ui.TextBox import TextBox
from src.ui.TextLabel import TextLabel
from src.util.math import relative_to_pixel, anchor_center
from src.scenes.Scene import Scene

class MenuScene(Scene):
    def __init__(self, game):
        self.game = game;
        self.title_font = pygame.font.Font("assets/fonts/StarCrush.ttf", 64);
        self.font = pygame.font.Font("assets/fonts/StarCrush.ttf", 24);
        self.title_label = TextLabel("HomoGraphio", self.title_font, (255, 255, 255), (0, 0.5, 0, 0.15), (0.5, 0.5))

        self.join_lobby_input = TextBox(self.font, (50, 50, 50), (230, 230, 230), (0, 0.5, 0, 0.45), (400, 0, 50, 0), (0.5, 0.5))
        self.join_lobby_input.set_text("Enter Lobby Code");

        self.create_label_box = TextBox(self.font, (255, 255, 255), (128, 0, 128), (0, 0.5, 0, 0.55), (400, 0, 50, 0), (0.5, 0.5))
        self.create_label_box.set_text("Create a lobby");

        def click_callback_test():
            print("Textbox clicked!");
        self.create_label_box.on_click(click_callback_test);

    def handle_events(self, events):
        pass;
    def update(self, dt: float):
        pass;
    def render(self, screen):
        screen.fill((25, 100, 50));
        # Render the ui elements in scene
        screen.blit(self.title_label.get_surface(), self.title_label.get_pos());
        screen.blit(self.create_label_box.get_surface(), self.create_label_box.get_pos());
        screen.blit(self.join_lobby_input.get_surface(), self.join_lobby_input.get_pos());
