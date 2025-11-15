import pygame
import sys
from NetworkManager import NetworkManager

pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

net = NetworkManager()
PLAYER_ID = None
chat_messages = []
input_text = ""

FONT = pygame.font.SysFont(None, 24)

def on_message(sender, msg):
    global PLAYER_ID

    if msg["type"] == "init":
        PLAYER_ID = msg["id"]
        return

    if msg["type"] == "chat":
        chat_messages.append(f"P{sender}: {msg['text']}")

mode = input("HOST or JOIN? ").strip().lower()
if mode == "host":
    print("IP: ",net.get_local_ip())
    code = net.host(on_message)
    print("JOIN CODE:", code)

elif mode == "join":
    ip = input("IP ADDRESS: ")
    code = input("Enter join code: ")
    net.join(code,on_message,ip)

else:
    sys.exit()

running = True
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if input_text.strip() != "":
                    net.send({"type": "chat", "text": input_text})
                    input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                if event.unicode.isprintable():
                    input_text += event.unicode

    screen.fill((20, 20, 20))

    y = 10
    for line in chat_messages[-15:]:
        surface = FONT.render(line, True, (255, 255, 255))
        screen.blit(surface, (10, y))
        y += 25

    pygame.draw.rect(screen, (50, 50, 50), (0, 360, 600, 40))
    surface = FONT.render(input_text, True, (255, 255, 255))
    screen.blit(surface, (10, 370))

    pygame.display.flip()

pygame.quit()
