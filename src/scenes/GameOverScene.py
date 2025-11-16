from src.scenes.Scene import Scene
import pygame

class GameOverScene(Scene):
    def __init__(self, game, winner_text="Game Over"):
        self.game = game
        self.title_font = pygame.font.Font("assets/fonts/StarCrush.ttf", 72)
        self.font = pygame.font.Font("assets/fonts/StarCrush.ttf", 36)

        self.winner_text = winner_text  # message like "You Win!" or "Words didn't match!"

        screen = pygame.display.get_surface()
        screen_rect = screen.get_rect()

        # Title
        self.title_surf = self.title_font.render("Game Over", True, (255, 255, 255))
        self.title_rect = self.title_surf.get_rect(center=(screen_rect.centerx, screen_rect.centery - 120))

        # Winner result text
        self.result_surf = self.font.render(self.winner_text, True, (255, 220, 120))
        self.result_rect = self.result_surf.get_rect(center=(screen_rect.centerx, screen_rect.centery - 40))

        # Button - Return to Menu
        self.button_surf = self.font.render("Back to Menu", True, (0, 0, 0))
        self.button_rect = pygame.Rect(0, 0, 300, 80)
        self.button_rect.center = (screen_rect.centerx, screen_rect.centery + 120)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    self.go_to_menu()

    def go_to_menu(self):
        self.game.restart_gameplay()

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill((100, 20, 20))

        screen.blit(self.title_surf, self.title_rect)
        screen.blit(self.result_surf, self.result_rect)

        pygame.draw.rect(screen, (255, 255, 255), self.button_rect, border_radius=12)
        screen.blit(self.button_surf, self.button_surf.get_rect(center=self.button_rect.center))
