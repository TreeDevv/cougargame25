import pygame;

from src.scenes.MenuScene import MenuScene
from src.ui.TextBox import instances as textbox_instances

def handle_textbox_collision(mouse_pos, textbox):
    pos = textbox.get_pos();
    size = textbox.get_size();
    rect = pygame.Rect(pos[0], pos[1], size[0], size[1]);
    if rect.collidepoint(mouse_pos):
        # Handle collision callbacks here
        if textbox.click_callback:
            textbox.click_callback();
        return True;
    return False;

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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos();
                    for textbox in textbox_instances:
                        handle_textbox_collision(mouse_pos, textbox);
            self.current_scene.handle_events(events);
            self.current_scene.update(dt);
            self.current_scene.render(screen);
    
            pygame.display.flip();
    def change_scene(self, new_scene):
        self.current_scene = new_scene;

if __name__ == "__main__":
    game = Game();
    game.run();