import json
import logging

from framework.events import client_event
from framework.client import Client


@client_event()
def on_server_message(client: Client, message: bytes) -> None:
    """
    Called when a message is received from the server
    :param message: str
    :return:
    """
    if message == "NICKREQ":
        client.client_socket.send(client.nickname.encode("utf-8"))
    elif message.decode("utf-8").startswith("ERROR"):
        _, error_data = message.decode("utf-8").split(" ")
        logging.error(json.loads(error_data)["msg"])
        client.client_socket.close()
    else:
        print(message)