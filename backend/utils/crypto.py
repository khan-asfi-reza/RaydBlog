from typing import Any

from cryptography.fernet import Fernet

from Main.settings import ENCRYPTION_KEY

crypt = Fernet(ENCRYPTION_KEY)


# Encrypts Data
def encrypt(data: Any):
    return crypt.encrypt(str(data).encode("utf-8")).decode("utf-8")


# Decrypts Data
def decrypt(data: str):
    return crypt.decrypt(bytes(data, "utf-8")).decode()
