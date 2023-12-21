import logging

from utils.config import get_config_key
from framework.server import Server

logging_levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "error": logging.ERROR
}


def main():
    logging.basicConfig(level=logging_levels.get(get_config_key("loggingLevel")),
                        format="[%(asctime)s] [%(levelname)s] : %(message)s", datefmt="%H:%M:%S")

    server = Server()
    server.startup()


if __name__ == "__main__":
    main()
