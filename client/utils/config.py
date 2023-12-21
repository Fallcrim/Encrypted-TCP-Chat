import json
from typing import Any


def get_config() -> dict:
    """
    Loads the complete config for the server module
    :return: dict
    """
    with open("config.json", "r") as configfile:
        config = json.load(configfile)
    return config


def get_config_key(key: str) -> Any:
    """
    Returns the configuration value for a specific key
    :param key: str
    :return: Any
    """
    return get_config().get(key)
