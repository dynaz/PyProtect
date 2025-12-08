
import base64
import sys

_STRINGS = []  # Will be populated by obfuscator

def _decrypt_str(index):
    """Decrypt string at given index"""
    encrypted = _STRINGS[int(index)]
    return base64.b64decode(encrypted).decode()



