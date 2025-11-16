import socket
import pickle
import threading


class Client:
    def __init__(self, ip, port):
        self.server_ip = ip
        self.server_port = port
        self.client = None

        self.my_id = None
        self.lobby_code = None
        self.connected = False

        self._thread = None

    def start(self, on_message=None):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_ip, self.server_port))
        self.connected = True

        # Receive ID (8 bytes)
        self.my_id = int(self.client.recv(8).decode())

        # Receive join code
        sender, code = pickle.loads(self.client.recv(4096))
        self.lobby_code = code

        print("[CLIENT] ID:", self.my_id)
        print("[CLIENT] Lobby Code:", self.lobby_code)

        self._thread = threading.Thread(
            target=self._listen_loop,
            args=(on_message,),
            daemon=True
        )
        self._thread.start()

    def send(self, message):
        if not self.connected:
            return
        try:
            self.client.send(pickle.dumps(message))
        except:
            self.connected = False

    def stop(self):
        self.connected = False
        try:
            self.client.close()
        except:
            pass

    def _listen_loop(self, on_message):
        while self.connected:
            try:
                data = self.client.recv(4096)
                if not data:
                    break

                sender, msg = pickle.loads(data)

                if on_message:
                    on_message(sender, msg)

            except:
                break

        print("[CLIENT] Disconnected.")
        self.connected = False

    def stop(self):
        print("[CLIENT] Stopping client...")
        try:
            self.connected = False
            if hasattr(self, "client") and self.client:
                self.client.close()
                self.client = None
        except Exception as e:
            print("[CLIENT] Error while closing client socket:", e)

