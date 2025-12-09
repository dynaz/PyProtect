
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
                # You might want to adjust this based on your use case.
                return None
        # Re-raise the original exception for other cases
        raise e

# Replace the original function immediately
ast.literal_eval = _safe_literal_eval

import base64
import sys

_STRINGS = ['__ENCRYPTED__YzNWd1pYSmZjMlZqY21WMFgydGxlVjh4TWpNME5RPT0=__ENCRYPTED__', '__ENCRYPTED__UVdOalpYTnpJR2R5WVc1MFpXUWg=__ENCRYPTED__', '__ENCRYPTED__UVdOalpYTnpJR1JsYm1sbFpDRT0=__ENCRYPTED__', '__ENCRYPTED__RGVjcnlwdCBzdHJpbmcgYXQgZ2l2ZW4gaW5kZXg=__ENCRYPTED__']  # Will be populated by obfuscator

def _decrypt_str(index):
    """Decrypt string at given index"""
    encrypted = _STRINGS[int(index)]
    # Handle the new encrypted format
    if encrypted.startswith('__ENCRYPTED__') and encrypted.endswith('__ENCRYPTED__'):
        encrypted = encrypted[13:-13]  # Remove the markers
    try:
        return base64.b64decode(encrypted).decode()
    except Exception:
        # If decryption fails, return empty string to prevent crashes
        return ""


import base64
import sys
_obf_0 = [_decrypt_str('0'), _decrypt_str('1'), _decrypt_str('2')]

def _fn_0(_obf_1):
    _decrypt_str('3')
    _obf_2 = _obf_0[int(_obf_1)]
    return base64.b64decode(_obf_2).decode()

def _fn_1(_obf_3):
    _obf_4 = _fn_0('0')
    if _obf_3 == _obf_4:
        return _fn_0('1')
    else:
        return _fn_0('2')
