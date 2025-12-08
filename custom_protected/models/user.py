
import base64
import sys

_STRINGS = ['ClVzZXIgbW9kZWwK', 'dG9rZW5fYWJjZGVmMTIzNDU2', 'VGhpcyBpcyBjb25maWRlbnRpYWwgaW5mb3JtYXRpb24=', 'R2V0IHVzZXIgcHJvZmlsZQ==', 'YWRtaW4xMjMhQCM=', 'bmFtZQ==', 'dG9rZW4=', 'ZGF0YQ==', 'ZGJfcGFzcw==', 'QXV0aGVudGljYXRlIHVzZXI=', 'bWFzdGVyX3Bhc3N3b3JkXzIwMjQ=']  # Will be populated by obfuscator

def _decrypt_str(index):
    """Decrypt string at given index"""
    encrypted = _STRINGS[int(index)]
    return base64.b64decode(encrypted).decode()


_decrypt_str('0')

class User:

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.api_token = _decrypt_str('1')
        self.secret_data = _decrypt_str('2')

    def get_profile(self):
        _decrypt_str('3')
        _obf_0 = _decrypt_str('4')
        return {_decrypt_str('5'): self.name, 'age': self.age, _decrypt_str('6'): self.api_token, _decrypt_str('7'): self.secret_data, _decrypt_str('8'): _obf_0}

    def authenticate(self, password):
        _decrypt_str('9')
        _obf_1 = _decrypt_str('10')
        return password == _obf_1
