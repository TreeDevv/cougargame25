from src.scenes.Scene import Scene
import pygame
import time
from src.util.ImageLoader import get_total_num
class GameScene(Scene):
    def __init__(self, game):
        pygame.mixer.init()
        pygame.mixer.music.load("assets/music/beepBoop1.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

        self.game = game
        self.title_font = pygame.font.Font("assets/fonts/StarCrush.ttf", 24)
        self.font = pygame.font.Font("assets/fonts/StarCrush.ttf", 48)
        self.input_font = pygame.font.Font("assets/fonts/StarCrush.ttf", 32)

        self.display_image = None
        screen = pygame.display.get_surface()
        screen_rect = screen.get_rect()
        self.total_Score = get_total_num()
        self.timer_duration = 300
        self.timer = time.time() + self.timer_duration

        self.score = 0

        self.title_surf = self.title_font.render("Homographio", True, (255, 255, 255))
        self.title_rect = self.title_surf.get_rect(center=(screen_rect.centerx, screen_rect.centery -420 ))

        self.placeholder_rect = pygame.Rect(0, 0, 400, 300)
        self.placeholder_rect.center = (screen_rect.centerx, screen_rect.centery -150)

        self.enter_surf = self.font.render("Guess the homograph!", True, (255, 255, 255))
        self.enter_rect = self.enter_surf.get_rect(center=(screen_rect.centerx, screen_rect.centery - 360))

        self.input_box = pygame.Rect(0, 0, 350, 50)
        self.input_box.center = (screen_rect.centerx - 100, screen_rect.centery + 80)
        self.input_text = ""
        self.active = False

        self.button_surf = self.font.render("Submit", True, (0, 0, 0))
        self.button_rect = pygame.Rect(0, 0, 150, 50)
        self.button_rect.midleft = (self.input_box.right + 15, self.input_box.centery)

        self.chat_history = []
        self.max_chat_lines = 2
        self.chat_draft = ""
        self.chat_active = False
        self.chat_rect = pygame.Rect(20, screen_rect.height - 140, screen_rect.width - 40, 120)


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.active = self.input_box.collidepoint(event.pos)
                self.chat_active = self.chat_rect.collidepoint(event.pos)

                if self.button_rect.collidepoint(event.pos):
                    self.submit_clicked()

            if event.type == pygame.KEYDOWN:

                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.submit_clicked()
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        if event.unicode.isprintable():
                            self.input_text += event.unicode

                if self.chat_active:
                    if event.key == pygame.K_RETURN:
                        self.submit_chat()
                    elif event.key == pygame.K_BACKSPACE:
                        self.chat_draft = self.chat_draft[:-1]
                    else:
                        if event.unicode.isprintable():
                            self.chat_draft += event.unicode


    def submit_clicked(self):
        text = self.input_text.strip()
        if text != "":
            self.game.net_ctrl.send_word(text)
            self.input_text = ""

    def Update_Score(self):
        self.score += 1

    def submit_chat(self):
        text = self.chat_draft.strip()
        if text != "":
            self.game.net_ctrl.send_chat(text)

        self.chat_draft = ""


    def update(self, dt):
        pass


    def render(self, screen):
        screen.fill((25, 100, 50))

        noise = super().create_dithered_surface()
        noise.set_alpha(40)
        screen.blit(noise, (0, 0))

        screen.blit(self.title_surf, self.title_rect)

        if self.display_image is None:
            pygame.draw.rect(screen, (200, 200, 200), self.placeholder_rect, border_radius=20)
            pygame.draw.rect(screen, (150, 150, 150), self.placeholder_rect, 4, border_radius=20)
        else:
            img_rect = self.display_image.get_rect(center=self.placeholder_rect.center)
            screen.blit(self.display_image, img_rect)

        screen.blit(self.enter_surf, self.enter_rect)

        remaining = int(self.timer - time.time())
        if remaining <= 0:
            self.game.end_gameplay()
            remaining = 0

        timer_text = self.font.render(f"Time: {remaining}", True, (255, 255, 255))
        screen.blit(timer_text, (screen.get_width() - 250, 20))

        score_text = self.font.render(f"Score: {self.score} / {self.total_Score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

        color = (255, 255, 255) if self.active else (180, 180, 180)
        pygame.draw.rect(screen, color, self.input_box, border_radius=8)
        pygame.draw.rect(screen, (50, 50, 50), self.input_box, 3, border_radius=8)

        text_surface = self.input_font.render(self.input_text, True, (0, 0, 0))
        screen.blit(text_surface, (self.input_box.x + 10, self.input_box.y + 10))

        pygame.draw.rect(screen, (255, 255, 255), self.button_rect, border_radius=10)
        screen.blit(self.button_surf, self.button_surf.get_rect(center=self.button_rect.center))

        pygame.draw.rect(screen, (255,255,255), self.chat_rect, border_radius=10)
        pygame.draw.rect(screen, (50, 50, 50), self.chat_rect, 2, border_radius=10)

        y = self.chat_rect.y + 8

        for msg in self.chat_history:
            chat_surf = self.input_font.render(msg, True, (0, 0, 0))
            screen.blit(chat_surf, (self.chat_rect.x + 10, y))
            y += chat_surf.get_height() + 2

        if self.chat_draft != "":
            draft_surf = self.input_font.render("> " + self.chat_draft, True, (100, 100, 100))
            screen.blit(draft_surf, (self.chat_rect.x + 10, y))
