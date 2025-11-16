import socket
import threading
import pickle
import random
import string


class Server:
    def __init__(self, host="0.0.0.0", port=5000):
        self.host = host
        self.port = port

        self.server_socket = None
        self.clients = {}  # id -> socket
        self.lock = threading.Lock()

        self.next_id = 1
        self.on_message = None

        self.lobby_code = self.generate_join_code()
        print("[SERVER] Lobby Code:", self.lobby_code)

    def generate_join_code(self, length=4):
        return ''.join(random.choice(string.ascii_uppercase + string.digits)
                       for _ in range(length))

    def start(self, on_message):
        self.on_message = on_message

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        print(f"[SERVER] Listening at {self.host}:{self.port}")

        threading.Thread(target=self._accept_loop, daemon=True).start()

    def _accept_loop(self):
        while True:
            conn, addr = self.server_socket.accept()

            with self.lock:
                player_id = self.next_id
                self.next_id += 1
                self.clients[player_id] = conn

            print(f"[SERVER] Player {player_id} connected.")

            # Send ID + Lobby Code
            conn.send(str(player_id).encode().ljust(8, b' '))
            conn.send(pickle.dumps(("LOBBY_CODE", self.lobby_code)))
            conn.send(pickle.dumps((player_id, {
                "type": "init",
                "id": player_id
            })))

            threading.Thread(
                target=self._handle_client,
                args=(conn, player_id),
                daemon=True
            ).start()

    def _handle_client(self, conn, pid):
        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    break

                msg = pickle.loads(data)

                # Handle join code (optional)
                if isinstance(msg, dict) and msg.get("type") == "join":
                    print(f"[SERVER] Player {pid} entered join code:", msg["code"])

                # Send message to host
                if self.on_message:
                    self.on_message(pid, msg)

                # Broadcast to all players except sender
                self._broadcast(pid, msg)
            except:
                break

        print(f"[SERVER] Player {pid} disconnected.")
        with self.lock:
            del self.clients[pid]
        conn.close()

    def _broadcast(self, sender_id, msg):
        packet = pickle.dumps((sender_id, msg))
        with self.lock:
            for pid, conn in self.clients.items():
                if pid != sender_id:  # do not echo back to sender
                    conn.send(packet)
