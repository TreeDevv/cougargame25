import pygame;


class Game:
    def __init__(self):
        pygame.init()
        self.current_scene = None;
    def run(self):
        self.running = True;
        
        screen = pygame.display.set_mode((800, 600));
        clock = pygame.time.Clock();

        while self.running:
            dt = clock.tick(60) / 1000.0;
            events = pygame.event.get();

            self.current_scene.handle_events(events);
            self.current_scene.update(dt);
            self.current_scene.render(screen);
    def change_scene(self, new_scene):
        self.current_scene = new_scene;