import socket
import logging
import threading

from utils.config import get_config_key
from framework.interaction import server_event, trigger_server_event, command, trigger_command


class Server:
    def __init__(self):
        self.socket: socket.socket  # initialization of instance variable; no declaration
        self.config = {
                    "address": get_config_key(key="server_address"),  # the address to listen on
                    "port": get_config_key(key="server_port")  # the port to listen on
                }
        self.clients = []  # containing client socket objects
        self.nicknames = []  # containing client nicknames

    def startup(self) -> None:
        """
        Starts the server socket and listens for incoming connections
        :return: None
        """
        logging.debug(f"Starting server socket on {self.config['address']}:{self.config['port']}")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.config["address"], self.config["port"]))
        self.socket.listen()
        self.run()

    def broadcast(self, message: str | bytes, sender: socket.socket) -> None:
        """
        Sends a message to all connected clients
        :param message: bytes
        :param sender: socket.socket
        :return: None
        """
        for idx, client in enumerate(self.clients):
            if client != sender:
                try:
                    client.send(message)
                except ConnectionResetError:
                    self.clients.pop(idx)
                    self.nicknames.pop(idx)

    def handle_client(self, client: socket.socket) -> None:
        """
        Handles a single client connection; used as thread target
        :param client: socket.socket
        """
        logging.info(f"Server socket started on {self.config['address']}:{self.config['port']}")
        while True:
            try:
                message = client.recv(1024).decode("utf-8")
                if message.startswith("CMD"):
                    trigger_command(message.split(" ")[1], message, client)
                elif message == "DISCONNECT":
                    index = self.clients.index(client)
                    self.clients.pop(index)
                    self.nicknames.pop(index)
                else:
                    trigger_server_event("new_client_message", message, client)
            except ConnectionResetError:
                logging.info(f"Client {self.clients[self.clients.index(client)]} disconnected")
                self.clients.pop(self.clients.index(client))
                break

    def run(self) -> None:
        """
        Starts the server and listens for incoming connections
        :return: None
        """
        while True:
            client, address = self.socket.accept()
            logging.info(f"New connection from {address[0]}:{address[1]}")

            client.send("NICKREQ".encode("utf-8"))
            nickname = client.recv(1024).decode("utf-8")
            if nickname in self.nicknames:
                client.send("ERROR {'msg': 'Nickname already connected!''}".encode("utf-8"))
                client.close()
                continue
            self.clients.append(client)
            self.nicknames.append(nickname)

            logging.debug(f"Nickname of {address[0]}:{address[1]} is {nickname}")
            self.broadcast(f"{nickname} connected to the server\n".encode("utf-8"), client)
            client.send("*Connected to the server*\n".encode("utf-8"))

            trigger_server_event("client_connect", client)

            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

    @server_event("client_connect")
    def send_motd(self, client: socket.socket) -> None:
        """
        Sends the message of the day to a client
        :param client: socket.socket
        :param nickname: str
        :return: None
        """
        client.send(f"{get_config_key('motd')}\n".encode("utf-8"))

    @server_event("new_client_message")
    def process_message(self, message: str | bytes, sender: socket.socket) -> None:
        """
        Processes a message from a client
        :param message: str | bytes
        :param sender: socket.socket
        :return: None
        """
        logging.debug("Message received")
        self.broadcast(message, sender)

    @command
    def disconnect(self, msg, client: socket.socket) -> None:
        """
        Disconnects a client
        :param client: socket.socket
        :return: None
        """
        client.send("DISCONNECT".encode("utf-8"))
        self.clients.pop(self.clients.index(client))
        client.close()
        self.nicknames.pop(self.clients.index(client))
        self.broadcast(f"{self.nicknames[self.clients.index(client)]} disconnected from the server\n".encode("utf-8"), client)
