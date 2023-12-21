import logging
from typing import Callable


commands = {}


def command() -> Callable:
    """
    Decorator for a local client command
    """
    def decorator(func):
        if func.__name__ not in commands:
            commands[func.__name__] = func
            logging.debug(f"Registered command '{func.__name__}'")
        else:
            logging.error(f"Couldn't map {func.__name__} as the name is already present!")
        return func
    return decorator


def trigger_command(client, command: str, *args) -> None:
    """
    Trigger a predefined command from the commands dict if present
    :param client: socket.socket
    :param command: str
    :param *args: Tuple(Any)
    """
    print(command, *args)
    if command in commands:
        commands[command](client, *args)
        return
    logging.error(f"Couldn't find command '{command}' as it is not registered")
