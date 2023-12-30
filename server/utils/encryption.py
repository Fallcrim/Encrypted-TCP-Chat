import rsa
from cryptography.fernet import Fernet


def get_encryption_key() -> bytes:
    """
    Gets the encryption key from the config file
    :return: bytes
    """
    try:
        with open("../group_key.key", "rb") as f:
            return f.read()
    except FileNotFoundError:
        generate_encryption_key()
        return get_encryption_key()


def generate_encryption_key() -> None:
    """
    Generates a new encryption key and saves it to the config file
    :return: None
    """
    key = Fernet.generate_key()
    with open("../group_key.key", "wb") as f:
        f.write(key)


def encrypt_group_key(group_key: bytes, public_key: rsa.PublicKey) -> bytes:
    """
    Encrypts the group key with the public key
    :param group_key: bytes
    :param public_key: rsa.PublicKey
    :return: bytes
    """
    return rsa.encrypt(group_key, public_key)
