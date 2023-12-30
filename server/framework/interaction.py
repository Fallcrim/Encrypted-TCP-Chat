import logging
from typing import Callable

event_handlers = {}
client_commands = {}


def server_event(event_id: str) -> Callable:
    """
    Registers a server event
    :param event_id: str
    """

    def decorator(func):
        if event_id not in event_handlers:
            event_handlers[event_id] = []
        event_handlers[event_id].append(func)
        return func

    return decorator


def trigger_server_event(event_id: str, *args, **kwargs) -> None:
    """
    Triggers a server event
    :param event_id: str
    :param args: list
    :param kwargs: dict
    """
    if event_id in event_handlers:
        for handler in event_handlers[event_id]:
            try:
                handler(*args, **kwargs)
            except Exception as e:
                logging.error(f"Error while executing event handler {handler.__name__}: {e}")


def command() -> Callable:
    """
    Registers a command
    """

    def decorator(func):
        if func.__name__ not in client_commands:
            client_commands[func.__name__] = func
        return func

    return decorator


def trigger_command(command_name: str, *args, **kwargs) -> None:
    """
    Triggers a command
    :param command_name: str
    :param args: list
    :param kwargs: dict
    """
    if command_name in client_commands:
        try:
            client_commands[command_name](*args, **kwargs)
        except Exception as e:
            logging.error(f"Error while executing command {command_name}: {e}")
