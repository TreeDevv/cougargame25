import pygame
from src.util.ImageLoader import get_Random_Index, get_record_name, get_image_by_index

class NetworkGameController:
    def __init__(self, game, network):
        self.game = game
        self.net = network

        self.submitted_words = {}
        self.secret_word = ""

    def on_message(self, sender, msg):
        msg_type = msg.get("type", None)

        if msg_type == "init":
            self.game.player_id = msg["id"]
            print("[NET] Assigned ID:", msg["id"])
            return

        if msg_type == "submit":
            self.handle_submit(sender, msg["text"])
            return

        if msg_type == "join":
            self.handle_join()
            return
        if msg_type == "Start":  
            self.game.start_gameplay()
            self.handle_image(msg["id"])
            return
        if msg_type == "image":
            self.game.current_scene.Update_Score()
            self.handle_image(msg["id"])
            return
        if msg_type == "chat":
            self.AddMessage(msg["text"])

            return

    def AddMessage(self, msg):
        self.game.current_scene.chat_history.append(msg)
        self.chat_history = self.game.current_scene.chat_history

        if len(self.chat_history) > self.game.current_scene.max_chat_lines:
            self.chat_history.pop(0)


    def handle_submit(self, sender, text):
        self.submitted_words[sender] = text
        print(f"[NET] Player {sender} submitted:", text)

        if len(self.submitted_words) == 2:
            values = list(self.submitted_words.values())
            correct = (
                values[0].lower() == values[1].lower() == self.secret_word.lower()
            )


            if correct:
                print("[GAME] Words match! Correct homograph.")
                if self.net.is_host and len(self.net.server.clients) >= 2:
                    self.send_new_image()
                self.submitted_words.clear()

            else:
                print("[GAME] Incorrect words. Try again.")


    def handle_join(self):
        if self.net.is_host and len(self.net.server.clients) >= 2:
            img_id = get_Random_Index()
            self.net.send({"type": "Start", "id" : img_id})
            self.game.start_gameplay()
            self.handle_image(img_id)
            #self.send_new_image()

    def handle_image(self, image_id):
        print("[NET] Received image id:", image_id)
        path = "./images/scenes/Media/Invertedcolor/"

        host = self.net.is_host
        self.secret_word = get_record_name(image_id)
        file_name = get_image_by_index(image_id, host)

        try:
            image = pygame.image.load(path + file_name).convert_alpha()
            image = pygame.transform.smoothscale(
                image, self.game.current_scene.placeholder_rect.size
            )
            self.game.current_scene.display_image = image
            print("[NET] Image loaded.")
        except Exception as e:
            print("[ERROR] Failed to load image:", e)


    def send_word(self, word):
        self.net.send({"type": "submit", "text": word})

    def send_chat(self, word):
        self.net.send({"type": "chat", "text": word})
        if not self.net.is_host:
            self.AddMessage(word)

    def send_new_image(self):
        img_id = get_Random_Index()
        if img_id == None:
            self.game.end_gameplay()
            return
        self.net.send({"type": "image", "id": img_id})

    def host_lobby(self):
        code = self.net.host(self.on_message)
        return code

    def join_lobby(self, code, ip = None):
        self.net.join(code, self.on_message, ip)
