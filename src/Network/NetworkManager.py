import time
from src.Network.Client import Client
from src.Network.Server import Server
import pickle
import socket

class NetworkManager:
    def __init__(self):
        self.server = None
        self.client = None
        self.is_host = False
        self.on_message = None

    def host(self, on_message, port=5001):
        if self.server is not None:
            print("[NETWORK] Host already running. Restarting...")
            self.stop_network()

        self.is_host = True
        self.on_message = on_message

        self.server = Server(self.get_local_ip(), port=port)
        self.server.start(on_message=self._server_message)

        time.sleep(0.2)

        self.client = Client(self.get_local_ip(), port)
        self.client.start(on_message=self._client_message)
        self._client_message(1, {"type": "init", "id": 1})

        print("[NETWORK] Hosting game.")
        return self.server.lobby_code

    
    def join(self, code, on_message, ip, port=5001):
        self.is_host = False
        self.on_message = on_message
        ip = self.get_local_ip()
        self.client = Client(ip, port)
        self.client.start(on_message=self._client_message)

        time.sleep(0.3)
        self.client.send({
            "type": "join",
            "code": code
        })

    def stop_network(self):
        print("[NETWORK] Stopping network...")

        # Stop client
        try:
            if hasattr(self, "client") and self.client and self.client.connected:
                self.client.stop()
        except:
            pass

        # Stop server
        try:
            if hasattr(self, "server") and self.server:
                self.server.stop()
        except:
            pass

        self.client = None
        self.server = None
        print("[NETWORK] Stopped.")


    def _server_message(self, sender, msg):
        print("[SERVER MSG]", sender, msg)
        if self.on_message:
            self.on_message(sender, msg)

    def _client_message(self, sender, msg):
        print("[CLIENT MSG]", sender, msg)
        if self.on_message:
            self.on_message(sender, msg)

    def send(self, msg):
        if self.is_host:
            for pid, conn in self.server.clients.items():
                conn.send(pickle.dumps((1, msg)))
        else:
            self.client.send(msg)

    def send_to_all(self, data):
        if self.is_host:
            packet = pickle.dumps((-1, data))  # -1 = server event, not a player
            for pid, conn in self.server.clients.items():
                try:
                    conn.send(packet)
                except:
                    pass  # ignore broken connections

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            print(ip)
        except:
            ip = "127.0.0.1"
        finally:
            s.close()
        with open("src/Network/IPConfig.txt", "r") as file:
            for line in file:
                if "=" in line:
                    _, value = line.strip().split("=", 1)
                    ip = value
        return "146.163.43.136"
