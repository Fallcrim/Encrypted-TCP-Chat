import logging

from client.framework.client import Client
from framework.commands import command


@command()
def connect(self, address: str) -> None:
    """
    Command to connect to a chatroom
    :param self: Client
    :param address: str
    :return:
    """
    logging.debug(address)
    args = address.split(" ")[1:]
    if len(args) > 1:
        logging.error("Too many arguments")
    elif len(args) == 1:
        host, port = args[0].split(":")
        self.client_socket.connect((host, int(port)))
    else:
        logging.error("Not enough arguments")

@command()
def disconnect(client: Client) -> None:
    """
    Command to disconnect from current server
    :return:
    """
    client.client_socket.send("DISCONNECT".encode("utf-8"))
    client.client_socket.close()