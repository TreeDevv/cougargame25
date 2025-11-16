import pygame;
import thorpy as tp;
import sys
from src.Network.NetworkManager import NetworkManager
from src.Network.Client import Client
from src.Network.Server import Server


from src.scenes.MenuScene import MenuScene
from src.scenes.GameScene import GameScene

from src.util.ImageLoader import get_image_by_index, get_Random_Index, get_record_name
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600));
        self.net = NetworkManager()
        tp.set_default_font("assets/fonts/StarCrush.ttf", 32)
        tp.init(self.screen, tp.theme_game1)
        self.start_network()
        self.current_scene = GameScene(self);
        self.submitted_words = {}
        self.word = ""
        self.counter = 0
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

    def start_network(self):
        mode = input("HOST or JOIN? ").strip().lower()

        def on_message(sender, msg):
            if msg["type"] == "init":
                self.player_id = msg["id"]
                print("Assigned ID:", self.player_id)
                return
            if msg["type"] == "submit":
                self.submitted_words[sender] = msg["text"]
                print(f"[NET] Player {sender} submitted:", msg["text"])
                print(len(self.submitted_words))
                # When both players submitted
                if len(self.submitted_words) == 2:
                    words = list(self.submitted_words.values())
                    match = (words[0] == words[1] == self.word)

                    # Tell everyone the result
                    # self.net.send_to_all({
                    #     "type": "result",
                    #     "match": match,
                    #     "words": words
                    # })
                    if match:
                        print("Game won")
                        if self.net.is_host and len(self.net.server.clients) >= 2:
                            image_index = get_Random_Index()
            
                            self.net.send({
                                "type": "image",
                                "id": image_index
                            })
                    else:
                        print("Wrong")
                    self.submitted_words.clear()
                return
            if msg["type"] == "join":
                 if self.net.is_host and len(self.net.server.clients) >= 2:
                    image_index = get_Random_Index()
    
                    self.net.send({
                        "type": "image",
                        "id": image_index
                    })
    
            if msg["type"] == "image":
                print("[NET] Received image index:", msg["id"])
                path = "./images/scenes/Media/"
                print(path)
                bo = self.net.is_host
                self.word = get_record_name(msg["id"])
                index = get_image_by_index(msg["id"], bo)
                print(index)
                try:
                    image = pygame.image.load(path + index).convert_alpha()
                    image = pygame.transform.smoothscale(image, self.current_scene.placeholder_rect.size)

                    self.current_scene.display_image = image

                    print("[NET] Image loaded:", path)
                except Exception as e:
                    print("[ERROR] Failed to load image:", path, e)


        if mode == "host":
            print("LOCAL IP:", self.net.get_local_ip())
            code = self.net.host(on_message)
            print("JOIN CODE:", code)

        elif mode == "join":
            ip = input("Server IP: ")
            code = input("Join Code: ")
            self.net.join(code, on_message, ip)

        else:
            print("Invalid selection. Exiting.")
            exit()

    def net_send(self, text):
        self.net.send({"type": "submit", "text": text})

if __name__ == "__main__":
    game = Game();
    game.run();