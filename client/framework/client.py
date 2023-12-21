import socket
import logging

from utils import get_config_key
from framework.commands import trigger_command
from framework.events import call_client_event


class Client:
    def __init__(self):
        """
        Initialising client instance
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_list = get_config_key(key="serverList")  # not implemented yet
        self.nickname = get_config_key(key="nickname")
        self.is_connected = False

    def interpret_input(self, user_input: str) -> None:
        if not user_input.startswith("#"):
            self.client_socket.send(f"{self.nickname}: {user_input}".encode("utf-8"))
            return
        self.run_command(user_input)

    def run_command(self, user_input: str) -> None:
        """
        Gets run if a command is entered by the user
        :param user_input: str
        :return:
        """
        command = user_input.split("#")[1]
        trigger_command(self, *command.split(" "))

    def handle_connection(self):
        """
        Used to handle the connection; thread target
        :return:
        """
        while True:
            try:
                server_message = self.client_socket.recv(1024)
                call_client_event("on_server_message", message=server_message)
            except ConnectionResetError:
                logging.error("Connection was shut down by server.")
            except ConnectionRefusedError:
                logging.error("Connection refused by server.")

    def write(self):
        """
        Used to write to the socket; thread target
        :return:
        """
        while True:
            user_input = input("> ")
            self.interpret_input(user_input)
