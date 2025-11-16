import pygame

from src.Network.NetworkManager import NetworkManager
from src.Network.NetworkController import NetworkGameController

from src.scenes.MenuScene import MenuScene
from src.scenes.GameScene import GameScene
from src.scenes.GameOverScene import GameOverScene

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        icon_image = pygame.image.load('assets/logo/HomographioAppIcon.png')
        pygame.display.set_icon(icon_image)

        pygame.display.set_caption("Homographio")
        self.net = NetworkManager()
        self.net_ctrl = NetworkGameController(self, self.net)

        self.current_scene = MenuScene(self)

        self.running = True
        self.player_id = None

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            dt = clock.tick(60) / 1000.0
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.current_scene.handle_events(events)
            self.current_scene.update(dt)
            self.current_scene.render(self.screen)

            pygame.display.flip()

        pygame.quit()

    def change_scene(self, new_scene):
        self.current_scene = new_scene

    def start_gameplay(self):
        self.change_scene(GameScene(self))
    
    def end_gameplay(self):
        self.change_scene(GameOverScene(self))
    
    def restart_gameplay(self):
        self.net = NetworkManager()
        self.net_ctrl = NetworkGameController(self, self.net)
        self.current_scene = MenuScene(self)


if __name__ == "__main__":
    game = Game()
    game.run()
