import pygame;

from src.scenes.MenuScene import MenuScene

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((800, 600));
        self.current_scene = MenuScene(self);
    def run(self):
        self.running = True;

        screen = self.screen
        clock = pygame.time.Clock();

        while self.running:
            dt = clock.tick(60) / 1000.0;
            events = pygame.event.get();
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False;
            self.current_scene.handle_events(events);
            self.current_scene.update(dt);
            self.current_scene.render(screen);
    
            pygame.display.flip();
    def change_scene(self, new_scene):
        self.current_scene = new_scene;

if __name__ == "__main__":
    game = Game();
    game.run();