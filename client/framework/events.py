import logging
from typing import Callable


events = {}


def client_event() -> Callable:
    """
    Decorator for a local client event
    :param func: Callable
    """
    def decorator(func):
        if func.__name__ not in events:
            events[func.__name__] = []
        events[func.__name__].append(func)
        logging.debug(f"Registered client event '{func.__name__}'")
        return func
    return decorator


def call_client_event(event: str, *args, **kwargs) -> None:
    if event in events:
        for func in events[event]:
            func(*args, **kwargs)
        return
    logging.error(f"Couldn't find event '{event}' as it is not registered")