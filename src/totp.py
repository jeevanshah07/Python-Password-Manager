"""
Credit to Luiz Rosa on hackernoon for the code
https://hackernoon.com/implementing-2fa-how-time-based-one-time-password-actually-works-with-python-examples-cm1m3ywt
"""

import hashlib
import hmac
import math
import secrets
import time


def generate_shared_secret() -> str:
    """
    Generates a secret needed for the time based one time password

    Returns:
        hex: a token
    """
    return secrets.token_hex(16)


def dynamic_truncation(raw_key: hmac.HMAC, length: int) -> str:
    """
    Convert a hash into a binary string, then into an integer

    Args:
        raw_key (hmac.HMAC)
        length (int)

    Returns:
        str
    """
    bitstring = bin(int(raw_key.hexdigest(), base=16))
    last_four_bits = bitstring[-4:]
    offset = int(last_four_bits, base=2)
    chosen_32_bits = bitstring[offset * 8:offset * 8 + 32]
    full_totp = str(int(chosen_32_bits, base=2))

    return full_totp[-length:]


def generate_totp(shared_key: str, length: int = 6) -> str:
    """
    Generates a time based one time password

    Args:
        shared_key (str): The key or token
        length (int): The length of the code

    Returns:
        str: The time based one time password
    """
    now_in_seconds = math.floor(time.time())
    step_in_seconds = 30
    t = math.floor(now_in_seconds / step_in_seconds)
    hash = hmac.new(
        bytes(shared_key, encoding="utf-8"),
        t.to_bytes(length=8, byteorder="big"),
        hashlib.sha256,
    )

    return dynamic_truncation(hash, length)


def validate_totp(totp: str, shared_key: str) -> bool:
    """
    Validates the time based one time password

    Args:
        totp (str): The actual time based one time password
        shared_key (str): The shared key

    Returns:
        bool
    """
    return totp == generate_totp(shared_key)
