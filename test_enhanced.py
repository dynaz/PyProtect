
import ast

# Override ast.literal_eval IMMEDIATELY to handle encrypted strings gracefully
_original_literal_eval = ast.literal_eval

def _safe_literal_eval(node_or_string):
    """Safe version of ast.literal_eval that handles encrypted strings"""
    try:
        return _original_literal_eval(node_or_string)
    except (ValueError, SyntaxError) as e:
        # If literal_eval fails, check if it's due to encrypted strings
        if isinstance(node_or_string, str):
            # Try to detect if this might be a decrypted string that contains code
            if any(keyword in node_or_string for keyword in ['import ', 'def ', 'class ', 'if ', 'for ']):
                # This looks like Python code, not a literal. Return a safe default.
                return None
        # Re-raise the original exception for other cases
        raise e

# Replace the original function immediately
ast.literal_eval = _safe_literal_eval

import base64
import hashlib
import random
import time
import sys

_STRINGS = ['__ENCRYPTED__ESsvMi4nYiQ3LCE2Ky0sYjYtYjYnMTZiLSAkNzEhIzYrLSw=__ENCRYPTED__', '__ENCRYPTED__CyYvLyxvYwYtKyItICYnYxM6EzEsNyYgN2I=__ENCRYPTED__', '__ENCRYPTED__AyEsIzUsITQlYDM1LWAvJmA0Ny9gLjUtIiUyMw==__ENCRYPTED__', '__ENCRYPTED__EjQsYS4nYQ==__ENCRYPTED__', '__ENCRYPTED__EiM1MmYqKSk2ZikkIDM1JScyLyko__ENCRYPTED__', '__ENCRYPTED__Ey8uNGc0MzUuKSBnMC4rK2clImciKSQ1PjczIiM=__ENCRYPTED__', '__ENCRYPTED__ECE3MC0qI2Q3MDYtKiNkISonNj00MC0rKn5k__ENCRYPTED__', '__ENCRYPTED__CSoqNWUsMSA3JDEsKit/ZQ==__ENCRYPTED__', '__ENCRYPTED__BysjJGosPyQpPiMlJA==__ENCRYPTED__', '__ENCRYPTED__CiUkPyMuOWs/Ljg/azg/OSIlLA==__ENCRYPTED__', '__ENCRYPTED__ES08aCkmJzwgLTpoOzw6ISYv__ENCRYPTED__', '__ENCRYPTED__Hyg7ICgrJSw6c2k=__ENCRYPTED__', '__ENCRYPTED__EREjLycgERE=__ENCRYPTED__']

def _decrypt_str(index):
    """Enhanced string decryption with anti-tampering"""
    # Junk code to confuse reverse engineers
    _junk_var1 = sum([i*i for i in range(100)]) % 7
    _junk_var2 = hashlib.md5(b"dummy").hexdigest()[:8]
    
    if _junk_var1 == 999:  # Never true - dead code
        print("This will never execute")
        return "fake_string"
    
    # Convert index to int if it's a string
    index_int = int(index) if isinstance(index, str) else index
    encrypted = _STRINGS[index_int]
    
    # More junk operations
    _temp_calc = (index_int * 13 + 7) % 256
    if _temp_calc > 1000:  # Never true
        encrypted = encrypted[::-1]
    
    # Handle the new encrypted format
    if encrypted.startswith('__ENCRYPTED__') and encrypted.endswith('__ENCRYPTED__'):
        encrypted = encrypted[13:-13]  # Remove the markers
    
    # Enhanced XOR layer for extra security
    try:
        decoded = base64.b64decode(encrypted).decode()
        # XOR decryption with key derived from index
        xor_key = (index_int % 256) ^ 0x42
        result = ''.join(chr(ord(c) ^ xor_key) for c in decoded)
        
        # More junk code
        if len(result) < 0:  # Never true
            result = result + _junk_var2
            
        return result
    except Exception:
        # If decryption fails, return empty string to prevent crashes
        return ""



"""
Test file for PyProtect Enhanced features
"""

def method_l1l0l1l():
    _decrypt_str(0 + 0 * 1)
    I1I1I0I1I = _decrypt_str(1 + 0 * 1)
    print(I1I1I0I1I)
    return I1I1I0I1I

def func_O0O1O0O(a, b):
    _decrypt_str(2 + 0 * 1)
    __1__ = a + b
    print(_decrypt_str(3 + 0 * 1) + str(a) + ' and ' + str(b) + ' is ' + str(__1__))
    return __1__

def method_l1l2l1l():
    _decrypt_str(4 + 0 * 1)
    var_2_e = _decrypt_str(5 + 0 * 1)
    print(_decrypt_str(6 + 0 * 1) + var_2_e)
    for var_3_15 in range(3):
        print(_decrypt_str(7 + 0 * 1) + str(var_3_15))

def main():
    _decrypt_str(8 + 0 * 1)
    method_l1l0l1l()
    __1__ = func_O0O1O0O(15, 25)
    method_l1l2l1l()
    _x4_y4_z4 = _decrypt_str(9 + 0 * 1)
    O0O0O5O0O = _decrypt_str(10 + 0 * 1)
    print(_decrypt_str(11 + 0 * 1) + _x4_y4_z4 + ' and ' + O0O0O5O0O)
if __name__ == _decrypt_str(12 + 0 * 1):
    __3_9__()