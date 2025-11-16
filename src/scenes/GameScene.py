from src.scenes.Scene import Scene
import pygame
from src.util.ImageLoader import get_Random_Index, get_image_by_index
class GameScene(Scene):
    def __init__(self, game):
        self.game = game
        self.title_font = pygame.font.Font("assets/fonts/StarCrush.ttf", 64)
        self.font = pygame.font.Font("assets/fonts/StarCrush.ttf", 40)
        self.input_font = pygame.font.Font("assets/fonts/StarCrush.ttf", 32)
        self.display_image = None 
        screen = pygame.display.get_surface()
        screen_rect = screen.get_rect()

        self.title_surf = self.title_font.render("Homographio", True, (255, 255, 255))
        self.title_rect = self.title_surf.get_rect(center=(screen_rect.centerx, screen_rect.centery - 200))

        self.placeholder_rect = pygame.Rect(0, 0, 300, 200)
        self.placeholder_rect.center = screen_rect.center

        self.enter_surf = self.font.render("Enter World", True, (255, 255, 255))
        self.enter_rect = self.enter_surf.get_rect(center=(screen_rect.centerx, screen_rect.centery + 140))

        self.input_box = pygame.Rect(0, 0, 350, 50)
        self.input_box.center = (screen_rect.centerx, screen_rect.centery + 200)
        self.input_text = ""
        self.active = False

        # Submit button
        self.button_surf = self.font.render("Submit", True, (0, 0, 0))
        self.button_rect = pygame.Rect(0, 0, 180, 60)
        self.button_rect.center = (screen_rect.centerx, screen_rect.centery + 280)

    def handle_events(self, events):
        for event in events:

            # Click detection for input box
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_box.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False

                # Button click
                if self.button_rect.collidepoint(event.pos):
                    self.submit_clicked()

            # Keyboard input (active only)
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.submit_clicked()
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        if event.unicode.isprintable():
                            self.input_text += event.unicode

    def submit_clicked(self):
        print("Submitted Text:", self.input_text)
        if self.input_text.strip() != "":
            self.game.net_send(self.input_text)  # send to server/clients
            print("Sent:", self.input_text)
            self.input_text = ""

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill((25, 100, 50))

        screen.blit(self.title_surf, self.title_rect)

        if self.display_image is None:
            # draw rectangle placeholder
            pygame.draw.rect(screen, (200, 200, 200), self.placeholder_rect, border_radius=20)
            pygame.draw.rect(screen, (150, 150, 150), self.placeholder_rect, 4, border_radius=20)
        else:
            # center image inside placeholder
            img_rect = self.display_image.get_rect(center=self.placeholder_rect.center)
            screen.blit(self.display_image, img_rect)


        screen.blit(self.enter_surf, self.enter_rect)
        color = (255, 255, 255) if self.active else (180, 180, 180)
        pygame.draw.rect(screen, color, self.input_box, border_radius=8)
        pygame.draw.rect(screen, (50, 50, 50), self.input_box, 3, border_radius=8)

        text_surface = self.input_font.render(self.input_text, True, (0, 0, 0))
        screen.blit(text_surface, (self.input_box.x + 10, self.input_box.y + 10))
        pygame.draw.rect(screen, (255, 255, 255), self.button_rect, border_radius=10)
        screen.blit(self.button_surf, self.button_surf.get_rect(center=self.button_rect.center))
