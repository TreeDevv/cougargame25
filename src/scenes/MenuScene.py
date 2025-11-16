import pygame
import random
from src.scenes.Scene import Scene
from src.util.math import relative_to_pixel

def create_dithered_surface():
    noise = pygame.Surface(pygame.display.get_window_size())
    for x in range(0, noise.get_size()[0], 4):
        for y in range(0, noise.get_size()[1], 4):
            shade = 30 if random.random() < 0.5 else -30
            color = (128 + shade, 20, 128 + shade)
            noise.fill(color, (x, y, 4, 4))
    return noise


class MenuScene(Scene):
    def __init__(self, game):
        self.game = game
        self.net_ctrl = game.net_ctrl  # use network controller

        screen = pygame.display.get_surface()
        self.screen_rect = screen.get_rect()

        self.font_title = pygame.font.Font("assets/fonts/StarCrush.ttf", 64)
        self.font_input = pygame.font.Font("assets/fonts/StarCrush.ttf", 32)
        self.font_button = pygame.font.Font("assets/fonts/StarCrush.ttf", 36)
        self.font_info = pygame.font.Font("assets/fonts/StarCrush.ttf", 28)

        self.title_surf = self.font_title.render("Homographio", True, (255, 255, 255))
        self.title_rect = self.title_surf.get_rect(center=relative_to_pixel((0.5, 0.2)))

        self.input_rect = pygame.Rect(0, 0, 300, 48)
        self.input_rect.center = relative_to_pixel((0.5, 0.4))
        self.input_text = ""
        self.input_active = False

        self.button_rect = pygame.Rect(0, 0, 320, 60)
        self.button_rect.center = relative_to_pixel((0.5, 0.55))
        self.lobby_message = ""

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                self.game.running = False

            if e.type == pygame.MOUSEBUTTONDOWN:
                self.input_active = self.input_rect.collidepoint(e.pos)

                if self.button_rect.collidepoint(e.pos):
                    self.try_create_or_join()

            if e.type == pygame.KEYDOWN and self.input_active:
                if e.key == pygame.K_RETURN:
                    self.try_create_or_join()
                elif e.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    if len(self.input_text) < 12:
                        self.input_text += e.unicode

    def try_create_or_join(self):
        code = self.input_text.strip()

        if code == "":
            print("[MENU] Hosting lobby...")
            join_code = self.net_ctrl.host_lobby()
            self.lobby_message = f"JOIN CODE: {join_code}"
            print("JOIN CODE:", join_code)
        else:
            print("[MENU] Joining lobby:", code)
            self.net_ctrl.join_lobby(code)
            self.lobby_message = "Joining lobby..."

        self.input_text = ""


    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill((25, 100, 50))
        noise = create_dithered_surface()
        noise.set_alpha(40)
        screen.blit(noise, (0, 0))

        screen.blit(self.title_surf, self.title_rect)
        if self.lobby_message == "":
            pygame.draw.rect(screen,
                            (255, 255, 255) if self.input_active else (200, 200, 200),
                            self.input_rect, 2)

            input_text = self.input_text or "Enter Join Code"
            input_surf = self.font_input.render(input_text, True, (255, 255, 255))
            screen.blit(input_surf, (self.input_rect.x + 8, self.input_rect.y + 8))

            pygame.draw.rect(screen, (128, 0, 128), self.button_rect, border_radius=8)
            btn_surf = self.font_button.render("Create Lobby / Join", True, (255, 255, 255))
            screen.blit(btn_surf, btn_surf.get_rect(center=self.button_rect.center))

        if self.lobby_message != "":
            info_surf = self.font_info.render(self.lobby_message, True, (255, 255, 0))
            info_rect = info_surf.get_rect(center=relative_to_pixel((0.5, 0.70)))
            screen.blit(info_surf, info_rect)
