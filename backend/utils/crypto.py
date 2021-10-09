from typing import Any

from cryptography.fernet import Fernet

from Main.settings import ENCRYPTION_KEY

crypt = Fernet(ENCRYPTION_KEY)


def encrypt(data: Any):
    return crypt.encrypt(str(data).encode("utf-8")).decode("utf-8")


def decrypt(data: str):
    return crypt.decrypt(bytes(data, "utf-8")).decode()
