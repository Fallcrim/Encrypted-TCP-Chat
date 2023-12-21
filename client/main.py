import threading
import logging

from utils.config import get_config_key
from framework.client import Client


def main():
    logging.basicConfig(level=get_config_key("loggingLevel"), format="[%(asctime)s] [%(levelname)s] : %(message)s",
                        datefmt="%H:%M:%S")
    client = Client()
    threading.Thread(target=client.write).start()


if __name__ == "__main__":
    main()
