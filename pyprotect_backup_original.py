
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

_STRINGS = ['__ENCRYPTED__ZGlzdA==__ENCRYPTED__', '__ENCRYPTED__Q3JlYXRlIGEgYmFja3VwIG9mIGV4aXN0aW5nIG91dHB1dCBiZWZvcmUgb3ZlcndyaXRpbmc=__ENCRYPTED__', '__ENCRYPTED__JVklbSVkXyVIJU0lUw==__ENCRYPTED__', '__ENCRYPTED__R2VuZXJhdGUgYSB1bmlxdWUgbWFjaGluZSBpZGVudGlmaWVyIGJhc2VkIG9uIGhhcmR3YXJl__ENCRYPTED__', '__ENCRYPTED__ezowMnh9__ENCRYPTED__', '__ENCRYPTED__bHNibGs=__ENCRYPTED__', '__ENCRYPTED__U0VSSUFM__ENCRYPTED__', '__ENCRYPTED__ICAgQmFja3VwIG5hbWVzIHNob3VsZCBtYXRjaDogbmFtZS5iYWNrdXBfWVlZWU1NRERfSEhNTVNT__ENCRYPTED__', '__ENCRYPTED__8J+UhCBSZXN0b3JlIE1vZGU=__ENCRYPTED__', '__ENCRYPTED__8J+UjSBDaGVja2luZyBMaWNlbnNlIFN0YXR1czo=__ENCRYPTED__', '__ENCRYPTED__Ki5saWNlbnNl__ENCRYPTED__', '__ENCRYPTED__cHJvamVjdC5saWNlbnNl__ENCRYPTED__', '__ENCRYPTED__TG9va2VkIGZvcjogKi5saWNlbnNlLCBwcm9qZWN0LmxpY2Vuc2U=__ENCRYPTED__', '__ENCRYPTED__dXRmLTg=__ENCRYPTED__', '__ENCRYPTED__TWFjaGluZSBJRA==__ENCRYPTED__', '__ENCRYPTED__VW5rbm93bg==__ENCRYPTED__', '__ENCRYPTED__TGljZW5zZSBLZXk=__ENCRYPTED__', '__ENCRYPTED__VW5rbm93bg==__ENCRYPTED__', '__ENCRYPTED__RXhwaXJlcw==__ENCRYPTED__', '__ENCRYPTED__VW5rbm93bg==__ENCRYPTED__', '__ENCRYPTED__UHJvdGVjdGVk__ENCRYPTED__', '__ENCRYPTED__VW5rbm93bg==__ENCRYPTED__', '__ENCRYPTED__VW5rbm93bg==__ENCRYPTED__', '__ENCRYPTED__4pyFIFZBTElE__ENCRYPTED__', '__ENCRYPTED__4p2MIElOVkFMSUQ=__ENCRYPTED__', '__ENCRYPTED__4pyFIE1hY2hpbmUgSUQgbWF0Y2hlcyBjdXJyZW50IG1hY2hpbmU=__ENCRYPTED__', '__ENCRYPTED__4p2MIEludmFsaWQgbGljZW5zZSBrZXkgZm9ybWF0__ENCRYPTED__', '__ENCRYPTED__8J+SoSBUaXA6IFVzZSAncHl0aG9uMyBweXByb3RlY3QucHkgLW0nIHRvIHNlZSB5b3VyIGN1cnJlbnQgbWFjaGluZSBJRA==__ENCRYPTED__', '__ENCRYPTED__UmVtb3ZlIGV4aXN0aW5nIG9iZnVzY2F0aW9uIHJ1bnRpbWUgY29kZSB0byBhbGxvdyByZS1vYmZ1c2NhdGlvbg==__ENCRYPTED__', '__ENCRYPTED__T3ZlcnJpZGUgYXN0LmxpdGVyYWxfZXZhbCBJTU1FRElBVEVMWQ==__ENCRYPTED__', '__ENCRYPTED__X3NhZmVfbGl0ZXJhbF9ldmFs__ENCRYPTED__', '__ENCRYPTED__X29yaWdpbmFsX2xpdGVyYWxfZXZhbA==__ENCRYPTED__', '__ENCRYPTED__X1NUUklOR1MgPSBbXQ==__ENCRYPTED__', '__ENCRYPTED__X1NUUklOR1MgPSBb__ENCRYPTED__', '__ENCRYPTED__X0xJQ0VOU0VfS0VZID0=__ENCRYPTED__', '__ENCRYPTED__X2NoZWNrX2xpY2Vuc2UoKQ==__ENCRYPTED__', '__ENCRYPTED__X2NoZWNrX2xpY2Vuc2UoKQ==__ENCRYPTED__', '__ENCRYPTED__X0xJQ0VOU0VfS0VZ__ENCRYPTED__', '__ENCRYPTED__X1NUUklOR1M=__ENCRYPTED__', '__ENCRYPTED__IyBPdmVycmlkZSBhc3QubGl0ZXJhbF9ldmFs__ENCRYPTED__', '__ENCRYPTED__X29yaWdpbmFsX2xpdGVyYWxfZXZhbA==__ENCRYPTED__', '__ENCRYPTED__SW52YWxpZCBsaWNlbnNlIGZvcm1hdA==__ENCRYPTED__', '__ENCRYPTED__TGljZW5zZSBleHBpcmVk__ENCRYPTED__', '__ENCRYPTED__SW52YWxpZCBsaWNlbnNlIHNpZ25hdHVyZQ==__ENCRYPTED__', '__ENCRYPTED__TGljZW5zZSB2YWxpZA==__ENCRYPTED__', '__ENCRYPTED__X2NvbXB1dGVf__ENCRYPTED__', '__ENCRYPTED__X2ludmVyc2Vf__ENCRYPTED__', '__ENCRYPTED__X3NlYXJjaF8=__ENCRYPTED__', '__ENCRYPTED__X29uY2hhbmdlXw==__ENCRYPTED__', '__ENCRYPTED__X2RlcGVuZHNf__ENCRYPTED__', '__ENCRYPTED__X2NvbnN0cmFpbnRf__ENCRYPTED__', '__ENCRYPTED__X3NxbF9jb25zdHJhaW50Xw==__ENCRYPTED__', '__ENCRYPTED__YWN0aW9uXw==__ENCRYPTED__', '__ENCRYPTED__YnV0dG9uXw==__ENCRYPTED__', '__ENCRYPTED__Z2V0Xw==__ENCRYPTED__', '__ENCRYPTED__X2dldF8=__ENCRYPTED__', '__ENCRYPTED__c2V0Xw==__ENCRYPTED__', '__ENCRYPTED__X3NldF8=__ENCRYPTED__', '__ENCRYPTED__X2NoZWNrXw==__ENCRYPTED__', '__ENCRYPTED__X3ByZXBhcmVf__ENCRYPTED__', '__ENCRYPTED__X2NyZWF0ZV8=__ENCRYPTED__', '__ENCRYPTED__X3dyaXRlXw==__ENCRYPTED__', '__ENCRYPTED__X3VwZGF0ZV8=__ENCRYPTED__', '__ENCRYPTED__X2RlZmF1bHRf__ENCRYPTED__', '__ENCRYPTED__c2hvd18=__ENCRYPTED__', '__ENCRYPTED__cHJvY2Vzc18=__ENCRYPTED__', '__ENCRYPTED__ZXhlY3V0ZQ==__ENCRYPTED__', '__ENCRYPTED__Y29tcGlsZQ==__ENCRYPTED__', '__ENCRYPTED__X2luZm8=__ENCRYPTED__', '__ENCRYPTED__RGV0ZWN0IE9kb28gZmllbGQgYXNzaWdubWVudHM=__ENCRYPTED__', '__ENCRYPTED__ZmllbGRz__ENCRYPTED__', '__ENCRYPTED__Q29sbGVjdCBhbGwgZnVuY3Rpb24vbWV0aG9kIG5hbWVz__ENCRYPTED__', '__ENCRYPTED__X25hbWU=__ENCRYPTED__', '__ENCRYPTED__X2Rlc2NyaXB0aW9u__ENCRYPTED__', '__ENCRYPTED__X2luaGVyaXQ=__ENCRYPTED__', '__ENCRYPTED__X2luaGVyaXRz__ENCRYPTED__', '__ENCRYPTED__X3JlY19uYW1l__ENCRYPTED__', '__ENCRYPTED__X29yZGVy__ENCRYPTED__', '__ENCRYPTED__X3NxbF9jb25zdHJhaW50cw==__ENCRYPTED__', '__ENCRYPTED__X2NvbnN0cmFpbnRz__ENCRYPTED__', '__ENCRYPTED__X2F1dG8=__ENCRYPTED__', '__ENCRYPTED__X3RhYmxl__ENCRYPTED__', '__ENCRYPTED__X3RhYmxlX3F1ZXJ5__ENCRYPTED__', '__ENCRYPTED__X3NlcXVlbmNl__ENCRYPTED__', '__ENCRYPTED__X3BhcmVudF9uYW1l__ENCRYPTED__', '__ENCRYPTED__X3BhcmVudF9zdG9yZQ==__ENCRYPTED__', '__ENCRYPTED__X2RhdGVfbmFtZQ==__ENCRYPTED__', '__ENCRYPTED__X2ZvbGRfbmFtZQ==__ENCRYPTED__', '__ENCRYPTED__X2Fic3RyYWN0__ENCRYPTED__', '__ENCRYPTED__X3RyYW5zaWVudA==__ENCRYPTED__', '__ENCRYPTED__X2xvZ19hY2Nlc3M=__ENCRYPTED__', '__ENCRYPTED__X2NoZWNrX2NvbXBhbnlfYXV0bw==__ENCRYPTED__', '__ENCRYPTED__X3JlZ2lzdGVyX2hvb2s=__ENCRYPTED__', '__ENCRYPTED__X3NldHVwX2NvbXBsZXRl__ENCRYPTED__', '__ENCRYPTED__X2NvbnN0cmFpbnRfbWV0aG9kcw==__ENCRYPTED__', '__ENCRYPTED__X2NvbHVtbnM=__ENCRYPTED__', '__ENCRYPTED__X2RlZmF1bHRz__ENCRYPTED__', '__ENCRYPTED__X3JlY19uYW1l__ENCRYPTED__', '__ENCRYPTED__X29yZGVy__ENCRYPTED__', '__ENCRYPTED__X2NvbnRleHQ=__ENCRYPTED__', '__ENCRYPTED__X3VpZA==__ENCRYPTED__', '__ENCRYPTED__Y3JlYXRl__ENCRYPTED__', '__ENCRYPTED__d3JpdGU=__ENCRYPTED__', '__ENCRYPTED__dW5saW5r__ENCRYPTED__', '__ENCRYPTED__c2VhcmNo__ENCRYPTED__', '__ENCRYPTED__YnJvd3Nl__ENCRYPTED__', '__ENCRYPTED__cmVhZA==__ENCRYPTED__', '__ENCRYPTED__c2VhcmNoX3JlYWQ=__ENCRYPTED__', '__ENCRYPTED__bmFtZV9nZXQ=__ENCRYPTED__', '__ENCRYPTED__bmFtZV9zZWFyY2g=__ENCRYPTED__', '__ENCRYPTED__bmFtZV9jcmVhdGU=__ENCRYPTED__', '__ENCRYPTED__ZGVmYXVsdF9nZXQ=__ENCRYPTED__', '__ENCRYPTED__ZmllbGRzX2dldA==__ENCRYPTED__', '__ENCRYPTED__ZmllbGRzX3ZpZXdfZ2V0__ENCRYPTED__', '__ENCRYPTED__bW9kZWxz__ENCRYPTED__', '__ENCRYPTED__ZmllbGRz__ENCRYPTED__', '__ENCRYPTED__dG9vbHM=__ENCRYPTED__', '__ENCRYPTED__c3RyaW5nX3R5cGVz__ENCRYPTED__', '__ENCRYPTED__dGV4dF90eXBl__ENCRYPTED__', '__ENCRYPTED__YmluYXJ5X3R5cGU=__ENCRYPTED__', '__ENCRYPTED__aW50ZWdlcl90eXBlcw==__ENCRYPTED__', '__ENCRYPTED__aXRlcml0ZW1z__ENCRYPTED__', '__ENCRYPTED__aXRlcmtleXM=__ENCRYPTED__', '__ENCRYPTED__aXRlcnZhbHVlcw==__ENCRYPTED__', '__ENCRYPTED__X2NvbXB1dGVf__ENCRYPTED__', '__ENCRYPTED__X2ludmVyc2Vf__ENCRYPTED__', '__ENCRYPTED__X3NlYXJjaF8=__ENCRYPTED__', '__ENCRYPTED__X29uY2hhbmdlXw==__ENCRYPTED__', '__ENCRYPTED__X2RlcGVuZHNf__ENCRYPTED__', '__ENCRYPTED__X2NvbnN0cmFpbnRf__ENCRYPTED__', '__ENCRYPTED__X3NxbF9jb25zdHJhaW50Xw==__ENCRYPTED__', '__ENCRYPTED__YWN0aW9uXw==__ENCRYPTED__', '__ENCRYPTED__YnV0dG9uXw==__ENCRYPTED__', '__ENCRYPTED__Z2V0Xw==__ENCRYPTED__', '__ENCRYPTED__X2dldF8=__ENCRYPTED__', '__ENCRYPTED__c2V0Xw==__ENCRYPTED__', '__ENCRYPTED__X3NldF8=__ENCRYPTED__', '__ENCRYPTED__X2NoZWNrXw==__ENCRYPTED__', '__ENCRYPTED__X3ByZXBhcmVf__ENCRYPTED__', '__ENCRYPTED__X2NyZWF0ZV8=__ENCRYPTED__', '__ENCRYPTED__X3dyaXRlXw==__ENCRYPTED__', '__ENCRYPTED__X3VwZGF0ZV8=__ENCRYPTED__', '__ENCRYPTED__X2RlZmF1bHRf__ENCRYPTED__', '__ENCRYPTED__c2hvd18=__ENCRYPTED__', '__ENCRYPTED__cHJvY2Vzc18=__ENCRYPTED__', '__ENCRYPTED__ZXhlY3V0ZQ==__ENCRYPTED__', '__ENCRYPTED__Y29tcGlsZQ==__ENCRYPTED__', '__ENCRYPTED__X2luZm8=__ENCRYPTED__', '__ENCRYPTED__R2VuZXJhdGUgb2JmdXNjYXRlZCB2YXJpYWJsZSBuYW1l__ENCRYPTED__', '__ENCRYPTED__R2VuZXJhdGUgb2JmdXNjYXRlZCBmdW5jdGlvbiBuYW1l__ENCRYPTED__', '__ENCRYPTED__X2xvZ2dlcg==__ENCRYPTED__', '__ENCRYPTED__X2xvZw==__ENCRYPTED__', '__ENCRYPTED__bG9nZ2Vy__ENCRYPTED__', '__ENCRYPTED__X2NhY2hl__ENCRYPTED__', '__ENCRYPTED__X3JlZ2lzdHJ5__ENCRYPTED__', '__ENCRYPTED__X21hcA==__ENCRYPTED__', '__ENCRYPTED__X2RpY3Q=__ENCRYPTED__', '__ENCRYPTED__X2xpc3Q=__ENCRYPTED__', '__ENCRYPTED__X3NldA==__ENCRYPTED__', '__ENCRYPTED__X3BhcnNlcnM=__ENCRYPTED__', '__ENCRYPTED__X2hhbmRsZXJz__ENCRYPTED__', '__ENCRYPTED__T2JmdXNjYXRlIHZhcmlhYmxlIG5hbWVz__ENCRYPTED__', '__ENCRYPTED__c2VsZg==__ENCRYPTED__', '__ENCRYPTED__X2xvZ2dlcg==__ENCRYPTED__', '__ENCRYPTED__X2xvZw==__ENCRYPTED__', '__ENCRYPTED__bG9nZ2Vy__ENCRYPTED__', '__ENCRYPTED__X2NhY2hl__ENCRYPTED__', '__ENCRYPTED__X3JlZ2lzdHJ5__ENCRYPTED__', '__ENCRYPTED__X21hcA==__ENCRYPTED__', '__ENCRYPTED__X2RpY3Q=__ENCRYPTED__', '__ENCRYPTED__X2xpc3Q=__ENCRYPTED__', '__ENCRYPTED__X3NldA==__ENCRYPTED__', '__ENCRYPTED__X3BhcnNlcnM=__ENCRYPTED__', '__ENCRYPTED__X2hhbmRsZXJz__ENCRYPTED__', '__ENCRYPTED__X2NhY2hl__ENCRYPTED__', '__ENCRYPTED__X3JlZ2lzdHJ5__ENCRYPTED__', '__ENCRYPTED__X21hcA==__ENCRYPTED__', '__ENCRYPTED__X2RpY3Q=__ENCRYPTED__', '__ENCRYPTED__X2xpc3Q=__ENCRYPTED__', '__ENCRYPTED__X3NldA==__ENCRYPTED__', '__ENCRYPTED__X3BhcnNlcnM=__ENCRYPTED__', '__ENCRYPTED__X2hhbmRsZXJz__ENCRYPTED__', '__ENCRYPTED__T2JmdXNjYXRlIGF0dHJpYnV0ZSBhY2Nlc3MgKGluY2x1ZGluZyBtZXRob2QgY2FsbHMp__ENCRYPTED__', '__ENCRYPTED__YXR0cg==__ENCRYPTED__', '__ENCRYPTED__c3VwZXI=__ENCRYPTED__', '__ENCRYPTED__c2VsZg==__ENCRYPTED__', '__ENCRYPTED__X19uYW1lX18=__ENCRYPTED__', '__ENCRYPTED__X19maWxlX18=__ENCRYPTED__', '__ENCRYPTED__X19pbml0X18=__ENCRYPTED__', '__ENCRYPTED__SGVscGVyIHRvIG9iZnVzY2F0ZSBhIHBhcmFtZXRlcg==__ENCRYPTED__', '__ENCRYPTED__c2VsZg==__ENCRYPTED__', '__ENCRYPTED__cG9zb25seWFyZ3M=__ENCRYPTED__', '__ENCRYPTED__Q29udHJvbGxlcg==__ENCRYPTED__', '__ENCRYPTED__Q29udHJvbGxlcg==__ENCRYPTED__', '__ENCRYPTED__X2RlY3J5cHRfc3Ry__ENCRYPTED__', '__ENCRYPTED__T2JmdXNjYXRlIGJpbmFyeSBvcGVyYXRpb25zIGJ5IG1ha2luZyB0aGVtIG1vcmUgY29tcGxleA==__ENCRYPTED__', '__ENCRYPTED__SGFuZGxlIGYtc3RyaW5ncyAtIG9iZnVzY2F0ZSB2YXJpYWJsZSBuYW1lcyBidXQgZG9uJ3QgZW5jcnlwdCBsaXRlcmFscw==__ENCRYPTED__', '__ENCRYPTED__SGFuZGxlIGxpc3QgY29tcHJlaGVuc2lvbnMgLSBvYmZ1c2NhdGUgbG9vcCB2YXJpYWJsZXM=__ENCRYPTED__', '__ENCRYPTED__SGFuZGxlIGRpY3QgY29tcHJlaGVuc2lvbnMgLSBvYmZ1c2NhdGUgbG9vcCB2YXJpYWJsZXM=__ENCRYPTED__', '__ENCRYPTED__SGFuZGxlIHNldCBjb21wcmVoZW5zaW9ucyAtIG9iZnVzY2F0ZSBsb29wIHZhcmlhYmxlcw==__ENCRYPTED__', '__ENCRYPTED__SGFuZGxlIGdlbmVyYXRvciBleHByZXNzaW9ucyAtIG9iZnVzY2F0ZSBsb29wIHZhcmlhYmxlcw==__ENCRYPTED__', '__ENCRYPTED__X19weWNhY2hlX18=__ENCRYPTED__', '__ENCRYPTED__ICAg8J+TnSBQeXRob24gZmlsZXM6__ENCRYPTED__', '__ENCRYPTED__ICAg8J+ThCBPdGhlciBmaWxlczo=__ENCRYPTED__', '__ENCRYPTED__cHJvamVjdC5saWNlbnNl__ENCRYPTED__', '__ENCRYPTED__dXRmLTg=__ENCRYPTED__', '__ENCRYPTED__dXRmLTg=__ENCRYPTED__', '__ENCRYPTED__X2RlY3J5cHRfc3RyKA==__ENCRYPTED__', '__ENCRYPTED__X1NUUklOR1MgPSBb__ENCRYPTED__', '__ENCRYPTED__X2NoZWNrX2xpY2Vuc2U=__ENCRYPTED__', '__ENCRYPTED__dXRmLTg=__ENCRYPTED__', '__ENCRYPTED__X19tYW5pZmVzdF9fLnB5__ENCRYPTED__', '__ENCRYPTED__X19vcGVuZXJwX18ucHk=__ENCRYPTED__', '__ENCRYPTED__X1NUUklOR1MgPSBbXQ==__ENCRYPTED__', '__ENCRYPTED__IyBPYmZ1c2NhdGVkIGNvZGUgd2lsbCBiZSBpbnNlcnRlZCBoZXJl__ENCRYPTED__', '__ENCRYPTED__IyBPYmZ1c2NhdGVkIGNvZGUgd2lsbCBiZSBpbnNlcnRlZCBoZXJl__ENCRYPTED__', '__ENCRYPTED__dXRmLTg=__ENCRYPTED__', '__ENCRYPTED__8J+UkiBHZW5lcmF0aW5nIG1hY2hpbmUgYmluZGluZyBsaWNlbnNlLi4u__ENCRYPTED__', '__ENCRYPTED__LmxpY2Vuc2U=__ENCRYPTED__', '__ENCRYPTED__dXRmLTg=__ENCRYPTED__', '__ENCRYPTED__X19tYW5pZmVzdF9fLnB5__ENCRYPTED__', '__ENCRYPTED__X19vcGVuZXJwX18ucHk=__ENCRYPTED__', '__ENCRYPTED__dXRmLTg=__ENCRYPTED__', '__ENCRYPTED__X1NUUklOR1MgPSBbXQ==__ENCRYPTED__', '__ENCRYPTED__IyBPYmZ1c2NhdGVkIGNvZGUgd2lsbCBiZSBpbnNlcnRlZCBoZXJl__ENCRYPTED__', '__ENCRYPTED__IyBPYmZ1c2NhdGVkIGNvZGUgd2lsbCBiZSBpbnNlcnRlZCBoZXJl__ENCRYPTED__', '__ENCRYPTED__dXRmLTg=__ENCRYPTED__', '__ENCRYPTED__X19tYWluX18=__ENCRYPTED__', '__ENCRYPTED__LS1pbnB1dA==__ENCRYPTED__', '__ENCRYPTED__LS1vdXRwdXQ=__ENCRYPTED__', '__ENCRYPTED__c3RvcmVfdHJ1ZQ==__ENCRYPTED__', '__ENCRYPTED__LS1kZXBsb3k=__ENCRYPTED__', '__ENCRYPTED__LS1yZXN0b3Jl__ENCRYPTED__', '__ENCRYPTED__LS11cmw=__ENCRYPTED__', '__ENCRYPTED__c3RvcmVfdHJ1ZQ==__ENCRYPTED__', '__ENCRYPTED__LS1tYWNoaW5lLWlk__ENCRYPTED__', '__ENCRYPTED__LS1jaGVjay1saWNlbnNl__ENCRYPTED__', '__ENCRYPTED__c3RvcmVfdHJ1ZQ==__ENCRYPTED__', '__ENCRYPTED__QmluZCBvYmZ1c2NhdGVkIGNvZGUgdG8gY3VycmVudCBtYWNoaW5l__ENCRYPTED__', '__ENCRYPTED__LS1iaW5kLW1hY2hpbmU=__ENCRYPTED__', '__ENCRYPTED__LS1leHBpcmF0aW9u__ENCRYPTED__', '__ENCRYPTED__c3RvcmVfdHJ1ZQ==__ENCRYPTED__', '__ENCRYPTED__LS1uby1wcmVzZXJ2ZS1hcGk=__ENCRYPTED__', '__ENCRYPTED__8J+UjSBDdXJyZW50IE1hY2hpbmUgSUQ6__ENCRYPTED__', '__ENCRYPTED__JVklbSVkXyVIJU0lUw==__ENCRYPTED__', '__ENCRYPTED__ICAgQ29udGludWluZyBhbnl3YXkuLi4=__ENCRYPTED__', '__ENCRYPTED__JVklbSVkXyVIJU0lUw==__ENCRYPTED__', '__ENCRYPTED__8J+Pl++4jyAgRGlyZWN0b3J5IG9iZnVzY2F0aW9uIG1vZGU=__ENCRYPTED__', '__ENCRYPTED__8J+UkyBQdWJsaWMgQVBJIHByZXNlcnZhdGlvbjogRU5BQkxFRCAoT2Rvby9GcmFtZXdvcmsgY29tcGF0aWJsZSk=__ENCRYPTED__', '__ENCRYPTED__8J+UkiBQdWJsaWMgQVBJIHByZXNlcnZhdGlvbjogRElTQUJMRUQgKEZ1bGwgb2JmdXNjYXRpb24p__ENCRYPTED__', '__ENCRYPTED__ICAgUmVtb3ZpbmcgZXhpc3RpbmcgYmFja3VwLi4u__ENCRYPTED__', '__ENCRYPTED__8J+ThCBTaW5nbGUgZmlsZSBvYmZ1c2NhdGlvbiBtb2Rl__ENCRYPTED__', '__ENCRYPTED__8J+UkyBQdWJsaWMgQVBJIHByZXNlcnZhdGlvbjogRU5BQkxFRCAoT2Rvby9GcmFtZXdvcmsgY29tcGF0aWJsZSk=__ENCRYPTED__', '__ENCRYPTED__8J+UkiBQdWJsaWMgQVBJIHByZXNlcnZhdGlvbjogRElTQUJMRUQgKEZ1bGwgb2JmdXNjYXRpb24p__ENCRYPTED__', '__ENCRYPTED__ICAgUmVtb3ZpbmcgZXhpc3RpbmcgYmFja3VwLi4u__ENCRYPTED__']  # Will be populated by obfuscator

def _decrypt_str(index):
    """Advanced string decryption with anti-tampering"""
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
    
    # Additional XOR layer for extra security
    try:
        decoded = base64.b64decode(encrypted).decode()
        # Simple XOR with key derived from index
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
Simple Python Obfuscator with Machine ID Binding - Proof of Concept
==================================================================

This demonstrates Python code obfuscation with hardware binding.
NOT suitable for production use - just educational.

Features:
- Variable name obfuscation
- String encryption
- Machine ID binding
- License key verification
- Hardware fingerprinting
- Anti-tampering measures
"""
import ast
import base64
import hashlib
import os
import sys
import platform
import uuid
import subprocess
import time
import shutil
from pathlib import Path
import random
import threading

def _check_environment():
    """Anti-debugging and environment checks"""
    # Check for common debugging tools
    suspicious_processes = ['ida', 'ollydbg', 'x64dbg', 'windbg', 'gdb', 'lldb', 'radare2']
    
    try:
        if platform.system() == 'Windows':
            import ctypes
            # Check if debugger is present (Windows)
            if ctypes.windll.kernel32.IsDebuggerPresent():
                sys.exit(0)
        
        # Check for suspicious environment variables
        suspicious_vars = ['_', 'PYTHONPATH', 'PYCHARM_HOSTED', 'VSCODE_PID']
        for var in suspicious_vars:
            if var in os.environ and 'debug' in os.environ.get(var, '').lower():
                time.sleep(random.uniform(1, 3))  # Random delay
                sys.exit(0)
                
        # Check process list for debugging tools
        try:
            if platform.system() == 'Windows':
                result = subprocess.run(['tasklist'], capture_output=True, text=True, timeout=2)
                process_list = result.stdout.lower()
            else:
                result = subprocess.run(['ps', 'aux'], capture_output=True, text=True, timeout=2)
                process_list = result.stdout.lower()
                
            for proc in suspicious_processes:
                if proc in process_list:
                    # Add random delay to make detection harder
                    time.sleep(random.uniform(0.5, 2))
                    sys.exit(0)
        except:
            pass  # Ignore errors in process checking
            
    except Exception:
        pass  # Ignore all errors to avoid breaking legitimate usage

# Run environment check immediately
_check_environment()

def _verify_code_integrity():
    """Verify code integrity to detect tampering"""
    try:
        # Get current file path
        current_file = __file__
        
        # Calculate file hash
        with open(current_file, 'rb') as f:
            file_content = f.read()
            file_hash = hashlib.sha256(file_content).hexdigest()
        
        # Check if hash matches expected (this would be set during obfuscation)
        # For now, just perform the check without failing
        expected_patterns = [b'_decrypt_str', b'_STRINGS', b'__ENCRYPTED__']
        
        for pattern in expected_patterns:
            if pattern not in file_content:
                # Code has been tampered with
                time.sleep(random.uniform(1, 3))
                sys.exit(0)
                
    except Exception:
        # If integrity check fails, exit silently
        pass

# Run integrity check
_verify_code_integrity()

# Dummy functions to confuse reverse engineers
def _dummy_func_1():
    """Fake function that does complex calculations but returns nothing useful"""
    result = 0
    for i in range(1000):
        result += i * i
        if result > 999999:
            result = result % 12345
    return result

def _dummy_func_2(x, y):
    """Another fake function with complex logic"""
    if x > y:
        return _dummy_func_1() + x - y
    else:
        return _dummy_func_1() - x + y

def _fake_decrypt(data):
    """Fake decryption function to mislead"""
    fake_key = "fake_key_12345"
    result = ""
    for i, char in enumerate(data):
        result += chr(ord(char) ^ ord(fake_key[i % len(fake_key)]))
    return result

# Call dummy functions to make them appear used
_dummy_result = _dummy_func_1()
if _dummy_result < 0:  # Never true
    _fake_decrypt("dummy_data")

def get_default_output_path():
    """Get the default output path in PyProtect/dist directory"""
    _obf_0 = Path(__file__).resolve()
    _obf_1 = _obf_0.parent.absolute()
    return _obf_1 / _decrypt_str('0')

def create_backup(output_path):
    _decrypt_str('1')
    if output_path.exists():
        _obf_2 = time.strftime(_decrypt_str('2'))
        _obf_3 = f'{output_path.name}_backup_{_obf_2}'
        if output_path.is_dir():
            _obf_4 = output_path.parent / _obf_3
            try:
                shutil.copytree(str(output_path), str(_obf_4))
                print(f'📦 Created backup: {_obf_4}')
            except Exception as e:
                print(f'⚠️  Warning: Could not create directory backup: {e}')
        else:
            _obf_4 = output_path.parent / _obf_3
            try:
                shutil.copy2(str(output_path), str(_obf_4))
                print(f'📦 Created backup: {_obf_4}')
            except Exception as e:
                print(f'⚠️  Warning: Could not create file backup: {e}')

def get_machine_id():
    _decrypt_str('3')
    _obf_5 = []
    try:
        _obf_6 = platform.processor()
        if _obf_6:
            _obf_5.append(f'cpu:{_obf_6}')
    except:
        pass
    try:
        _obf_7 = platform.machine()
        if _obf_7:
            _obf_5.append(f'arch:{_obf_7}')
    except:
        pass
    try:
        _obf_8 = ':'.join([_decrypt_str('4').format(uuid.getnode() >> _obf_9 & 255) for _obf_9 in range(0, 2 * 6, 2)][::-1])
        _obf_5.append(f'mac:{_obf_8}')
    except:
        pass
    try:
        _obf_10 = subprocess.run([_decrypt_str('5'), '-o', _decrypt_str('6'), '-n', '-d'], capture_output=True, text=True, timeout=5)
        if _obf_10.returncode == 0 and _obf_10.stdout.strip():
            _obf_11 = _obf_10.stdout.strip().split('\n')[0]
            if _obf_11:
                _obf_5.append(f'disk:{_obf_11}')
    except:
        pass
    _obf_12 = '|'.join(_obf_5)
    _obf_13 = hashlib.sha256(_obf_12.encode()).hexdigest()[:32]
    return _obf_13

def restore_from_backup(backup_path):
    """Restore original from backup"""
    import re
    backup_path = Path(backup_path)
    if not backup_path.exists():
        print(f'❌ Backup not found: {backup_path}')
        return False
    _obf_14 = backup_path.name
    if backup_path.is_dir():
        _obf_15 = re.match('^(.+)\\.backup_\\d{8}_\\d{6}$', _obf_14)
    else:
        _obf_15 = re.match('^(.+)\\.backup_\\d{8}_\\d{6}(\\..+)?$', _obf_14)
    if not _obf_15:
        print(f'❌ Not a valid backup name: {_obf_14}')
        print(_decrypt_str('7'))
        return False
    if backup_path.is_dir():
        _obf_16 = _obf_15.group(1)
    else:
        _obf_16 = _obf_15.group(1) + (_obf_15.group(2) or '')
    _obf_17 = backup_path.parent / _obf_16
    print('\n' + '=' * 60)
    print(_decrypt_str('8'))
    print('=' * 60)
    print(f'📦 Backup: {backup_path}')
    print(f'🎯 Will restore to: {_obf_17}')
    if _obf_17.exists():
        print(f'⚠️  Current version exists and will be REMOVED')
    else:
        print(f'✅ Target location is empty')
    print()
    _obf_18 = input('⚠️  Proceed with restore? (y/n): ').strip().lower()
    if _obf_18 not in ['y', 'yes']:
        print('\n🛑 Restore cancelled by user')
        return False
    print('\n🔄 Restoring...')
    try:
        if _obf_17.exists():
            if _obf_17.is_dir():
                shutil.rmtree(str(_obf_17))
            else:
                _obf_17.unlink()
            print(f'✅ Removed current version at: {_obf_17}')
        shutil.move(str(backup_path), str(_obf_17))
        print(f'✅ Backup restored to: {_obf_17}')
        print(f'\n💡 Original restored successfully!')
        return True
    except Exception as e:
        print(f'\n❌ Restore failed: {e}')
        return False

def check_license_status(directory):
    """Check license status in the specified directory"""
    print(_decrypt_str('9'))
    print('=' * 50)
    _obf_19 = Path(directory)
    if not _obf_19.exists():
        print(f'❌ Directory not found: {directory}')
        return
    _obf_20 = []
    _obf_20.extend(_obf_19.glob(_decrypt_str('10')))
    _obf_20.extend(_obf_19.glob(_decrypt_str('11')))
    if not _obf_20:
        print(f'❌ No license files found in: {directory}')
        print(_decrypt_str('12'))
        return
    print(f'Found {len(_obf_20)} license file(s):')
    _obf_21 = get_machine_id()
    for _obf_22 in _obf_20:
        print(f'\n📄 License File: {_obf_22.name}')
        print('-' * 30)
        try:
            with open(_obf_22, 'r', encoding=_decrypt_str('13')) as _obf_23:
                _obf_24 = _obf_23.read().strip()
            _obf_25 = _obf_24.split('\n')
            _obf_26 = {}
            for _obf_27 in _obf_25:
                if ':' in _obf_27:
                    _obf_28, _obf_29 = _obf_27.split(':', 1)
                    _obf_26[_obf_28.strip()] = _obf_29.strip()
            _obf_30 = _obf_26.get(_decrypt_str('14'), _decrypt_str('15'))
            _obf_31 = _obf_26.get(_decrypt_str('16'), _decrypt_str('17'))
            _obf_32 = _obf_26.get(_decrypt_str('18'), _decrypt_str('19'))
            _obf_33 = _obf_26.get(_decrypt_str('20'), _decrypt_str('21'))
            print(f'Machine ID: {_obf_30}')
            print(f'License Key: {_obf_31}')
            print(f'Expires: {_obf_32}')
            print(f'Protected: {_obf_33}')
            if _obf_31 and _obf_31 != _decrypt_str('22'):
                _obf_34, _obf_35 = _fn_6(_obf_31)
                _obf_36 = _decrypt_str('23') if _obf_34 else _decrypt_str('24')
                print(f'Status: {_obf_36} - {_obf_35}')
                if _obf_30 == _obf_21:
                    print(_decrypt_str('25'))
                else:
                    print('⚠️  Machine ID does not match current machine')
                    print(f'   License Machine: {_obf_30}')
                    print(f'   Current Machine: {_obf_21}')
            else:
                print(_decrypt_str('26'))
        except Exception as e:
            print(f'❌ Error reading license file: {e}')
    print('\n' + '=' * 50)
    print(_decrypt_str('27'))

def generate_license_key(machine_id, expiration_days=365):
    """Generate a license key for the machine"""
    _obf_37 = int(time.time()) + expiration_days * 24 * 60 * 60
    _obf_38 = f'{machine_id}:{_obf_37}'
    _obf_39 = hashlib.sha256(f'secret_salt:{_obf_38}'.encode()).hexdigest()[:16]
    _obf_40 = f'{_obf_38}:{_obf_39}'
    return (_obf_40, _obf_37)

def extract_future_imports(source: str):
    """Extract leading __future__ imports (and preceding blank/comment lines) to keep them at the top."""
    _obf_41 = source.splitlines()
    _obf_42 = []
    _obf_43 = []
    _obf_44 = False
    for _obf_45 in _obf_41:
        _obf_46 = _obf_45.lstrip()
        if not _obf_44:
            if _obf_46.startswith('from __future__ import'):
                _obf_42.append(_obf_45)
                continue
            elif _obf_46 == '' or _obf_46.startswith('#'):
                _obf_42.append(_obf_45)
                continue
            else:
                _obf_44 = True
                _obf_43.append(_obf_45)
        else:
            _obf_43.append(_obf_45)
    while _obf_42 and _obf_42[-1].strip() == '':
        _obf_42.pop()
    _obf_47 = '\n'.join(_obf_42) if _obf_42 else ''
    _obf_48 = '\n'.join(_obf_43)
    return (_obf_47, _obf_48)

def strip_existing_runtime_code(source: str):
    _decrypt_str('28')
    _obf_49 = source.splitlines()
    _obf_50 = []
    _obf_51 = False
    _obf_52 = [_decrypt_str('29'), _decrypt_str('30'), _decrypt_str('31'), _decrypt_str('32'), _decrypt_str('33'), 'def _decrypt_str(', _decrypt_str('34'), 'def _get_machine_id(', 'def _check_license(', _decrypt_str('35')]
    _obf_53 = 0
    while _obf_53 < len(_obf_49):
        _obf_54 = _obf_49[_obf_53]
        _obf_55 = _obf_54.strip()
        _obf_56 = any((_obf_57 in _obf_54 for _obf_57 in _obf_52))
        if _obf_56:
            if _obf_55.startswith(_decrypt_str('36')):
                _obf_53 += 1
                continue
            elif _obf_55.startswith('def _') or _obf_55.startswith(_decrypt_str('37')) or _obf_55.startswith(_decrypt_str('38')):
                _obf_51 = True
                _obf_53 += 1
                continue
            elif _decrypt_str('39') in _obf_54 or _decrypt_str('40') in _obf_54:
                _obf_51 = True
                _obf_53 += 1
                continue
        if _obf_51:
            if _obf_55 and (not _obf_54.startswith(' ')) and (not _obf_54.startswith('\t')):
                if not any((_obf_58 in _obf_54 for _obf_58 in _obf_52)):
                    _obf_51 = False
                    _obf_50.append(_obf_54)
            _obf_53 += 1
            continue
        _obf_50.append(_obf_54)
        _obf_53 += 1
    return '\n'.join(_obf_50)

def verify_license_key(license_key):
    """Verify if license is valid for current machine"""
    try:
        _obf_59 = license_key.split(':')
        if len(_obf_59) != 3:
            return (False, _decrypt_str('41'))
        _obf_60 = _obf_59[0]
        _obf_61 = int(_obf_59[1])
        _obf_62 = _obf_59[2]
        _obf_63 = int(time.time())
        if _obf_63 > _obf_61:
            return (False, _decrypt_str('42'))
        _obf_64 = hashlib.sha256(f'secret_salt:{_obf_60}:{_obf_61}'.encode()).hexdigest()[:16]
        if _obf_62 != _obf_64:
            return (False, _decrypt_str('43'))
        _obf_65 = get_machine_id()
        if _obf_60 != _obf_65:
            return (False, 'License not valid for this machine')
        return (True, _decrypt_str('44'))
    except Exception as e:
        return (False, f'License verification error: {e}')

class NameCollector(ast.NodeVisitor):
    """Collect all Odoo field names and method names before obfuscation"""

    def __init__(self):
        self.field_names = set()
        self.method_names = {}
        self.odoo_method_patterns = [_decrypt_str('45'), _decrypt_str('46'), _decrypt_str('47'), _decrypt_str('48'), _decrypt_str('49'), _decrypt_str('50'), _decrypt_str('51'), _decrypt_str('52'), _decrypt_str('53'), _decrypt_str('54'), _decrypt_str('55'), _decrypt_str('56'), _decrypt_str('57'), _decrypt_str('58'), _decrypt_str('59'), _decrypt_str('60'), _decrypt_str('61'), _decrypt_str('62'), _decrypt_str('63'), _decrypt_str('64'), _decrypt_str('65'), _decrypt_str('66'), _decrypt_str('67'), _decrypt_str('68')]

    def visit_Assign(self, node):
        _decrypt_str('69')
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Attribute):
                if isinstance(node.value.func.value, ast.Name):
                    if node.value.func.value.id == _decrypt_str('70'):
                        for _obf_66 in node.targets:
                            if isinstance(_obf_66, ast.Name):
                                self.field_names.add(_obf_66.id)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        _decrypt_str('71')
        _obf_67 = False
        for _obf_68 in self.odoo_method_patterns:
            if _obf_68 in node.name:
                _obf_67 = True
                break
        self.method_names[node.name] = _obf_67
        self.generic_visit(node)

class Obfuscator(ast.NodeTransformer):
    """AST-based obfuscator with advanced complexity"""

    def __init__(self, _obf_69=None, _obf_70=None, _obf_71=True):
        self.var_count = 0
        self.func_count = 0
        self.class_count = 0
        self.var_map = {}
        self.func_map = {}
        self.class_map = {}
        self.strings = []
        self.preserve_public_api = _obf_71
        self.module_level_depth = 0
        self.public_names = set()
        self.in_public_class = False
        self.in_controller_class = False
        self.in_fstring = False
        self.in_class_body = False
        self.collected_methods = _obf_70 or {}
        self.odoo_reserved = {_decrypt_str('72'), _decrypt_str('73'), _decrypt_str('74'), _decrypt_str('75'), _decrypt_str('76'), _decrypt_str('77'), _decrypt_str('78'), _decrypt_str('79'), _decrypt_str('80'), _decrypt_str('81'), _decrypt_str('82'), _decrypt_str('83'), _decrypt_str('84'), _decrypt_str('85'), _decrypt_str('86'), _decrypt_str('87'), _decrypt_str('88'), _decrypt_str('89'), _decrypt_str('90'), _decrypt_str('91'), _decrypt_str('92'), _decrypt_str('93'), _decrypt_str('94'), _decrypt_str('95'), _decrypt_str('96'), _decrypt_str('97'), _decrypt_str('98'), 'env', 'id', 'ids', _decrypt_str('99'), '_cr', _decrypt_str('100'), _decrypt_str('101'), _decrypt_str('102'), _decrypt_str('103'), _decrypt_str('104'), _decrypt_str('105'), _decrypt_str('106'), _decrypt_str('107'), _decrypt_str('108'), _decrypt_str('109'), _decrypt_str('110'), _decrypt_str('111'), _decrypt_str('112'), _decrypt_str('113'), 'api', _decrypt_str('114'), _decrypt_str('115'), _decrypt_str('116'), '_', _decrypt_str('117'), _decrypt_str('118'), _decrypt_str('119'), _decrypt_str('120'), _decrypt_str('121'), _decrypt_str('122'), _decrypt_str('123'), 'PY2', 'PY3'}
        self.odoo_method_patterns = [_decrypt_str('124'), _decrypt_str('125'), _decrypt_str('126'), _decrypt_str('127'), _decrypt_str('128'), _decrypt_str('129'), _decrypt_str('130'), _decrypt_str('131'), _decrypt_str('132'), _decrypt_str('133'), _decrypt_str('134'), _decrypt_str('135'), _decrypt_str('136'), _decrypt_str('137'), _decrypt_str('138'), _decrypt_str('139'), _decrypt_str('140'), _decrypt_str('141'), _decrypt_str('142'), _decrypt_str('143'), _decrypt_str('144'), _decrypt_str('145'), _decrypt_str('146'), _decrypt_str('147')]
        self.odoo_field_names = _obf_69 or set()
        for _obf_72, _obf_73 in self.collected_methods.items():
            if not _obf_73:
                _obf_74 = False
                for _obf_75 in self.odoo_method_patterns:
                    if _obf_75 in _obf_72:
                        _obf_74 = True
                        break
                if _obf_72 in self.odoo_reserved:
                    _obf_74 = True
                if not _obf_74:
                    self.func_map[_obf_72] = self._fn_11()

    def generate_var_name(self):
        _decrypt_str('148')
        # Generate confusing names that look like legitimate code
        confusing_patterns = [
            lambda n: f'O0O0O{n}O0O',  # Mix of O and 0
            lambda n: f'l1l1l{n}l1l',  # Mix of l and 1
            lambda n: f'__{n}__',      # Double underscore
            lambda n: f'I1I1I{n}I1I',  # Mix of I and 1
            lambda n: f'_x{n}_y{n}_z{n}',  # Multi-part names
            lambda n: f'var_{hex(n)[2:]}_{hex(n*7)[2:]}',  # Hex-based
        ]
        pattern = random.choice(confusing_patterns)
        _obf_76 = pattern(self.var_count)
        self.var_count += 1
        return _obf_76

    def generate_func_name(self):
        _decrypt_str('149')
        # Generate confusing function names
        confusing_patterns = [
            lambda n: f'func_O0O{n}O0O',
            lambda n: f'method_l1l{n}l1l',
            lambda n: f'__{hex(n)[2:]}_{hex(n*3)[2:]}__',
            lambda n: f'fn_I1I{n}I1I',
            lambda n: f'_exec_{n}_{n*2}',
            lambda n: f'handler_{chr(65+n%26)}{n}',
        ]
        pattern = random.choice(confusing_patterns)
        _obf_77 = pattern(self.func_count)
        self.func_count += 1
        return _obf_77

    def generate_class_name(self):
        """Generate obfuscated class name"""
        _obf_78 = f'_cls_{self.class_count}'
        self.class_count += 1
        return _obf_78

    def add_control_flow_obfuscation(self, node):
        """Add control flow obfuscation to make reverse engineering harder"""
        # Add dummy conditional branches that never execute
        dummy_conditions = [
            ast.Compare(
                left=ast.Constant(value=1),
                ops=[ast.Eq()],
                comparators=[ast.Constant(value=0)]
            ),
            ast.Compare(
                left=ast.Constant(value=True),
                ops=[ast.Is()],
                comparators=[ast.Constant(value=False)]
            ),
            ast.Compare(
                left=ast.Constant(value="dummy"),
                ops=[ast.Eq()],
                comparators=[ast.Constant(value="never_match")]
            )
        ]
        
        # Create dummy if statement that never executes
        dummy_if = ast.If(
            test=random.choice(dummy_conditions),
            body=[
                ast.Expr(value=ast.Call(
                    func=ast.Name(id='print', ctx=ast.Load()),
                    args=[ast.Constant(value="This will never print")],
                    keywords=[]
                )),
                ast.Pass()
            ],
            orelse=[]
        )
        
        return dummy_if

    def visit_FunctionDef(self, node):
        """Add junk code to function definitions"""
        # Add dummy code at the beginning of functions
        if len(node.body) > 0 and random.random() < 0.3:  # 30% chance
            junk_code = self.add_control_flow_obfuscation(node)
            node.body.insert(0, junk_code)
        
        # Continue with normal processing
        self.generic_visit(node)
        return node

    def visit_Assign(self, node):
        """Preserve Odoo model attributes when assigning in class body (not in methods)"""
        if self.in_class_body:
            for _obf_79 in node.targets:
                if isinstance(_obf_79, ast.Name):
                    if _obf_79.id in self.odoo_reserved:
                        self.generic_visit(node.value)
                        return node
        if self.module_level_depth == 0:
            _obf_80 = [_decrypt_str('150'), _decrypt_str('151'), _decrypt_str('152'), 'log']
            _obf_81 = [_decrypt_str('153'), _decrypt_str('154'), _decrypt_str('155'), _decrypt_str('156'), _decrypt_str('157'), _decrypt_str('158'), _decrypt_str('159'), _decrypt_str('160')]
            for _obf_79 in node.targets:
                if isinstance(_obf_79, ast.Name):
                    _obf_82 = any((_obf_79.id.endswith(_obf_83) for _obf_83 in _obf_81))
                    if _obf_79.id.isupper() or _obf_79.id in _obf_80 or _obf_82 or (_obf_79.id in self.odoo_reserved):
                        self.generic_visit(node.value)
                        return node
        self.generic_visit(node)
        return node

    def visit_Name(self, node):
        _decrypt_str('161')
        if node.id in (_decrypt_str('162'), 'cls'):
            return node
        if node.id in self.var_map:
            pass
        elif node.id in self.odoo_field_names:
            return node
        if node.id.isupper():
            return node
        _obf_84 = [_decrypt_str('163'), _decrypt_str('164'), _decrypt_str('165'), 'log']
        _obf_85 = [_decrypt_str('166'), _decrypt_str('167'), _decrypt_str('168'), _decrypt_str('169'), _decrypt_str('170'), _decrypt_str('171'), _decrypt_str('172'), _decrypt_str('173')]
        _obf_86 = any((node.id.endswith(_obf_87) for _obf_87 in _obf_85))
        if self.module_level_depth == 0 and node.id not in self.var_map:
            if node.id in _obf_84 or _obf_86:
                return node
        if isinstance(node.ctx, ast.Store):
            if self.in_class_body and node.id in self.odoo_reserved:
                return node
            if self.module_level_depth == 0:
                _obf_85 = [_decrypt_str('174'), _decrypt_str('175'), _decrypt_str('176'), _decrypt_str('177'), _decrypt_str('178'), _decrypt_str('179'), _decrypt_str('180'), _decrypt_str('181')]
                _obf_86 = any((node.id.endswith(_obf_88) for _obf_88 in _obf_85))
                if node.id.isupper() or node.id in _obf_84 or _obf_86:
                    return node
            if node.id not in self.var_map:
                self.var_map[node.id] = self.generate_var_name()
            node.id = self.var_map[node.id]
        elif isinstance(node.ctx, ast.Load):
            if node.id in self.var_map:
                node.id = self.var_map[node.id]
            elif node.id in self.func_map:
                node.id = self.func_map[node.id]
            elif node.id in self.class_map:
                node.id = self.class_map[node.id]
            elif node.id.isupper() or (node.id in _obf_84 and self.module_level_depth == 0):
                return node
            elif node.id in self.odoo_reserved:
                return node
        return node

    def visit_Call(self, node):
        """Preserve keyword argument names in method calls - they must match method signatures"""
        for _obf_89 in node.keywords:
            if _obf_89.value:
                _obf_89.value = self.visit(_obf_89.value)
        node.func = self.visit(node.func)
        node.args = [self.visit(_obf_90) for _obf_90 in node.args]
        return node

    def visit_Attribute(self, node):
        _decrypt_str('182')
        if hasattr(node, _decrypt_str('183')):
            _obf_91 = False
            if isinstance(node.value, ast.Call):
                if isinstance(node.value.func, ast.Name) and node.value.func.id == _decrypt_str('184'):
                    _obf_91 = True
            if _obf_91:
                pass
            elif node.attr in self.odoo_reserved:
                pass
            elif node.attr in self.func_map:
                node.attr = self.func_map[node.attr]
            elif node.attr not in [_decrypt_str('185'), _decrypt_str('186'), _decrypt_str('187'), _decrypt_str('188')]:
                pass
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node):
        """Obfuscate function names (skip special methods and public API)"""
        _obf_92 = True
        if node.name.startswith('__') and node.name.endswith('__'):
            _obf_92 = False
        if node.name in self.odoo_reserved:
            _obf_92 = False
        for _obf_93 in self.odoo_method_patterns:
            if _obf_93 in node.name:
                _obf_92 = False
                break
        if self.preserve_public_api and self.module_level_depth == 0:
            if not node.name.startswith('_'):
                _obf_92 = False
                self.public_names.add(node.name)
        if self.preserve_public_api and self.in_public_class:
            if not node.name.startswith('_'):
                _obf_92 = False
        if _obf_92:
            if node.name not in self.func_map:
                self.func_map[node.name] = self.generate_func_name()
            node.name = self.func_map[node.name]
        elif node.name in self.func_map:
            del self.func_map[node.name]
        _obf_94 = self.var_map.copy()
        self.var_map = {}
        _obf_95 = not node.name.startswith('_')

        def process_param(arg_node):
            _decrypt_str('189')
            if arg_node is None:
                return
            if arg_node.arg in (_decrypt_str('190'), 'cls'):
                return
            if self.in_controller_class:
                self.var_map[arg_node.arg] = arg_node.arg
                return
            if is_public_method:
                self.var_map[arg_node.arg] = arg_node.arg
                return
            _obf_96 = arg_node.arg
            if _obf_96 not in self.var_map:
                self.var_map[_obf_96] = self.generate_var_name()
            arg_node.arg = self.var_map[_obf_96]
        for _obf_97 in node.args.args:
            process_param(_obf_97)
        if node.args.vararg:
            process_param(node.args.vararg)
        if node.args.kwarg:
            process_param(node.args.kwarg)
        for _obf_97 in node.args.kwonlyargs:
            process_param(_obf_97)
        if hasattr(node.args, _decrypt_str('191')):
            for _obf_97 in node.args.posonlyargs:
                process_param(_obf_97)
        _obf_98 = self.in_class_body
        self.in_class_body = False
        self.module_level_depth += 1
        node.decorator_list = [self.visit(_obf_99) for _obf_99 in node.decorator_list]
        node.body = [self.visit(_obf_100) for _obf_100 in node.body]
        if node.returns:
            node.returns = self.visit(node.returns)
        self.module_level_depth -= 1
        self.in_class_body = _obf_98
        self.var_map = _obf_94
        return node

    def visit_ClassDef(self, node):
        """Obfuscate class names (preserve public API classes)"""
        _obf_101 = True
        _obf_102 = False
        _obf_103 = False
        for _obf_104 in node.bases:
            if isinstance(_obf_104, ast.Attribute):
                if _obf_104.attr == _decrypt_str('192'):
                    _obf_103 = True
            elif isinstance(_obf_104, ast.Name):
                if _decrypt_str('193') in _obf_104.id:
                    _obf_103 = True
        if self.preserve_public_api and self.module_level_depth == 0:
            if not node.name.startswith('_'):
                _obf_101 = False
                _obf_102 = True
                self.public_names.add(node.name)
        if _obf_101:
            if node.name not in self.class_map:
                self.class_map[node.name] = self.generate_class_name()
            node.name = self.class_map[node.name]
        _obf_105 = self.in_public_class
        _obf_106 = self.in_controller_class
        _obf_107 = self.in_class_body
        if _obf_102:
            self.in_public_class = True
        if _obf_103:
            self.in_controller_class = True
        self.in_class_body = True
        self.module_level_depth += 1
        self.generic_visit(node)
        self.module_level_depth -= 1
        self.in_public_class = _obf_105
        self.in_controller_class = _obf_106
        self.in_class_body = _obf_107
        return node

    def visit_Constant(self, node):
        """Advanced string encryption with multiple layers"""
        if self.in_fstring:
            return node
        if isinstance(node.value, str) and len(node.value) > 3:
            _obf_108 = ['import', 'def ', 'class ', 'if ', 'for ', 'while ', 'try ', 'with ', 'from ', 'lambda ', 'return ', 'yield ', 'raise ', 'break', 'continue', 'pass', 'assert ', 'global ', 'nonlocal ', 'except ', 'finally ', 'elif ', 'else:', ' and ', ' or ', ' not ', ' is ', ' in ', 'True', 'False', 'None']
            _obf_109 = ['\n', '\t', '\r', '(', ')', '[', ']', '{', '}', '=', '+', '-', '*', '/', '//', '%', '==', '!=', '<', '>', '<=', '>=', '+=', '-=', '*=', '/=', '//=', '%=', '&', '|', '^', '~', '<<', '>>', '->', ':', ';', ',', '.']
            _obf_110 = sum((1 for _obf_111 in _obf_109 if _obf_111 in node.value))
            _obf_112 = any((_obf_113 in node.value for _obf_113 in _obf_108))
            _obf_114 = _obf_110 > 5
            _obf_115 = '\n' in node.value or '\r' in node.value or '\t' in node.value
            _obf_116 = len(node.value) > 200
            if _obf_112 or _obf_114 or _obf_115 or _obf_116:
                return node
            
            # Multi-layer encryption
            string_index = len(self.strings)
            
            # Layer 1: XOR with index-based key
            xor_key = (string_index % 256) ^ 0x42
            xor_encrypted = ''.join(chr(ord(c) ^ xor_key) for c in node.value)
            
            # Layer 2: Base64 encoding
            base64_encrypted = base64.b64encode(xor_encrypted.encode()).decode()
            
            # Layer 3: Add obfuscation markers
            _obf_117 = f'__ENCRYPTED__{base64_encrypted}__ENCRYPTED__'
            self.strings.append(_obf_117)
            
            # Create more complex call with dummy operations
            dummy_calc = ast.BinOp(
                left=ast.Constant(value=string_index),
                op=ast.Add(),
                right=ast.BinOp(
                    left=ast.Constant(value=0),
                    op=ast.Mult(),
                    right=ast.Constant(value=1)
                )
            )
            
            return ast.Call(
                func=ast.Name(id=_decrypt_str('194'), ctx=ast.Load()), 
                args=[dummy_calc], 
                keywords=[]
            )
        return node

    def visit_BinOp(self, node):
        _decrypt_str('195')
        if isinstance(node.op, ast.Add) and isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
            if isinstance(node.left.value, (int, float)) and isinstance(node.right.value, (int, float)):
                _obf_118 = ast.BinOp(left=ast.BinOp(left=node.left, op=ast.Mult(), right=ast.Constant(value=2)), op=ast.Add(), right=ast.BinOp(left=node.right, op=ast.Mult(), right=ast.Constant(value=2)))
                _obf_119 = ast.BinOp(left=_obf_118, op=ast.FloorDiv(), right=ast.Constant(value=2))
                return _obf_119
        self.generic_visit(node)
        return node

    def visit_JoinedStr(self, node):
        _decrypt_str('196')
        _obf_120 = self.in_fstring
        self.in_fstring = True
        self.generic_visit(node)
        self.in_fstring = _obf_120
        return node

    def visit_ListComp(self, node):
        _decrypt_str('197')
        return self._fn_24(node)

    def visit_DictComp(self, node):
        _decrypt_str('198')
        return self._fn_24(node)

    def visit_SetComp(self, node):
        _decrypt_str('199')
        return self._fn_24(node)

    def visit_GeneratorExp(self, node):
        _decrypt_str('200')
        return self._fn_24(node)

    def _fn_24(self, _obf_121):
        """Common logic for all comprehension types"""
        _obf_122 = self.var_map.copy()
        for _obf_123 in _obf_121.generators:
            if isinstance(_obf_123.target, ast.Name):
                if _obf_123.target.id not in self.var_map:
                    self.var_map[_obf_123.target.id] = self.generate_var_name()
                _obf_123.target.id = self.var_map[_obf_123.target.id]
            else:
                self.visit(_obf_123.target)
            _obf_123.iter = self.visit(_obf_123.iter)
            _obf_123.ifs = [self.visit(_obf_124) for _obf_124 in _obf_123.ifs]
        if isinstance(_obf_121, ast.DictComp):
            _obf_121.key = self.visit(_obf_121.key)
            _obf_121.value = self.visit(_obf_121.value)
        elif isinstance(_obf_121, (ast.ListComp, ast.SetComp, ast.GeneratorExp)):
            _obf_121.elt = self.visit(_obf_121.elt)
        self.var_map = _obf_122
        return _obf_121

def generate_runtime(machine_id=None, license_key=None):
    """Generate runtime decryption and license verification functions"""
    _obf_125 = ''
    if license_key:
        _obf_125 = f'''\n# License verification\n_LICENSE_KEY = "{license_key}"\n\ndef _get_machine_id():\n    """Generate machine identifier"""\n    import hashlib\n    import platform\n    import uuid\n    import subprocess\n\n    components = []\n    try:\n        cpu_info = platform.processor()\n        if cpu_info:\n            components.append(f"cpu:{{cpu_info}}")\n    except:\n        pass\n\n    try:\n        machine = platform.machine()\n        if machine:\n            components.append(f"arch:{{machine}}")\n    except:\n        pass\n\n    try:\n        mac = ':'.join(['{{:02x}}'.format((uuid.getnode() >> elements) & 0xff)\n                       for elements in range(0, 2*6, 2)][::-1])\n        components.append(f"mac:{{mac}}")\n    except:\n        pass\n\n    try:\n        result = subprocess.run(['lsblk', '-o', 'SERIAL', '-n', '-d'],\n                              capture_output=True, text=True, timeout=5)\n        if result.returncode == 0 and result.stdout.strip():\n            disk_serial = result.stdout.strip().split('\\n')[0]\n            if disk_serial:\n                components.append(f"disk:{{disk_serial}}")\n    except:\n        pass\n\n    combined = '|'.join(components)\n    machine_id = hashlib.sha256(combined.encode()).hexdigest()[:32]\n    return machine_id\n\ndef _verify_license_key(license_key):\n    """Verify license validity"""\n    import hashlib\n    import time\n\n    try:\n        parts = license_key.split(':')\n        if len(parts) != 3:\n            return False\n\n        machine_id = parts[0]\n        expiration = int(parts[1])\n        signature = parts[2]\n\n        current_time = int(time.time())\n        if current_time > expiration:\n            return False\n\n        expected_signature = hashlib.sha256(f"secret_salt:{{machine_id}}:{{expiration}}".encode()).hexdigest()[:16]\n        if signature != expected_signature:\n            return False\n\n        current_machine_id = _get_machine_id()\n        if machine_id != current_machine_id:\n            return False\n\n        return True\n    except:\n        return False\n\ndef _check_license():\n    """Verify license on startup"""\n    if not _verify_license_key(_LICENSE_KEY):\n        print("ERROR: Invalid or expired license!")\n        print("This software is licensed to run on a different machine.")\n        import sys\n        sys.exit(1)\n\n# Check license immediately\n_check_license()\n'''
    _obf_126 = f'''\nimport ast\n\n# Override ast.literal_eval IMMEDIATELY to handle encrypted strings gracefully\n_original_literal_eval = ast.literal_eval\n\ndef _safe_literal_eval(node_or_string):\n    """Safe version of ast.literal_eval that handles encrypted strings"""\n    try:\n        return _original_literal_eval(node_or_string)\n    except (ValueError, SyntaxError) as e:\n        # If literal_eval fails, check if it's due to encrypted strings\n        if isinstance(node_or_string, str):\n            # Try to detect if this might be a decrypted string that contains code\n            if any(keyword in node_or_string for keyword in ['import ', 'def ', 'class ', 'if ', 'for ']):\n                # This looks like Python code, not a literal. Return a safe default.\n                # You might want to adjust this based on your use case.\n                return None\n        # Re-raise the original exception for other cases\n        raise e\n\n# Replace the original function immediately\nast.literal_eval = _safe_literal_eval\n\nimport base64\nimport sys\n\n_STRINGS = []  # Will be populated by obfuscator\n\ndef _decrypt_str(index):\n    """Decrypt string at given index"""\n    encrypted = _STRINGS[int(index)]\n    # Handle the new encrypted format\n    if encrypted.startswith('__ENCRYPTED__') and encrypted.endswith('__ENCRYPTED__'):\n        encrypted = encrypted[13:-13]  # Remove the markers\n    try:\n        return base64.b64decode(encrypted).decode()\n    except Exception:\n        # If decryption fails, return empty string to prevent crashes\n        return ""\n\n{_obf_125}\n# Obfuscated code will be inserted here\n'''
    return _obf_126

def obfuscate_directory(input_dir, output_dir, bind_machine=False, expiration_days=365, preserve_api=True, project_url=None):
    """Obfuscate all Python files in a directory recursively"""
    print(f'🔍 Scanning directory: {input_dir}')
    print(f'📁 Output directory: {output_dir}')
    print()
    _obf_127 = Path(input_dir)
    _obf_128 = Path(output_dir)
    if not _obf_127.exists():
        print(f'❌ Input directory not found: {input_dir}')
        return False
    if not _obf_127.is_dir():
        print(f'❌ Input path is not a directory: {input_dir}')
        return False
    create_backup(_obf_128)
    _obf_128.mkdir(parents=True, exist_ok=True)
    _obf_129 = []
    for _obf_130, _obf_131, _obf_132 in os.walk(_obf_127):
        _obf_131[:] = [_obf_133 for _obf_133 in _obf_131 if not _obf_133.startswith(_decrypt_str('201'))]
        for _obf_134 in _obf_132:
            _obf_135 = Path(_obf_130) / _obf_134
            _obf_136 = _obf_135.relative_to(_obf_127)
            _obf_129.append((_obf_135, _obf_136))
    if not _obf_129:
        print('❌ No files found in the directory')
        return False
    _obf_137 = [(_obf_138, _obf_139) for _obf_138, _obf_139 in _obf_129 if _obf_138.suffix == '.py']
    _obf_140 = [(_obf_141, _obf_142) for _obf_141, _obf_142 in _obf_129 if _obf_141.suffix != '.py']
    print(f'📋 Found {len(_obf_129)} total files:')
    print(f'   • {len(_obf_137)} Python files to obfuscate')
    print(f'   • {len(_obf_140)} other files to copy')
    if _obf_137:
        print(_decrypt_str('202'))
        for _obf_143, _obf_136 in _obf_137:
            print(f'      • {_obf_136}')
    if _obf_140:
        print(_decrypt_str('203'))
        for _obf_143, _obf_136 in _obf_140:
            print(f'      • {_obf_136}')
    print()
    _obf_144 = None
    _obf_145 = None
    if bind_machine:
        print('🔒 Generating machine binding license for project...')
        _obf_144 = get_machine_id()
        _obf_145, _obf_146 = generate_license_key(_obf_144, expiration_days)
        print(f'📋 Machine ID: {_obf_144}')
        print(f'🔑 License Key: {_obf_145}')
        print(f'⏰ Expires: {time.ctime(_obf_146)}')
        print()
        _obf_147 = _obf_128 / _decrypt_str('204')
        with open(_obf_147, 'w', encoding=_decrypt_str('205')) as _obf_148:
            _obf_148.write(f'Machine ID: {_obf_144}\n')
            _obf_148.write(f'License Key: {_obf_145}\n')
            _obf_148.write(f'Expires: {time.ctime(_obf_146)}\n')
            _obf_148.write(f'Protected: {time.ctime(time.time())}\n')
            if project_url:
                _obf_148.write(f'Project URL: {project_url}\n')
        print(f'💾 Project license saved to: {_obf_147}')
        if project_url:
            print(f'🔗 Project URL: {project_url}')
        print()
    _obf_149 = []
    _obf_150 = []
    for _obf_135, _obf_136 in _obf_137:
        _obf_151 = _obf_128 / _obf_136
        _obf_151.parent.mkdir(parents=True, exist_ok=True)
        print(f'🔧 Obfuscating: {_obf_136}')
        try:
            _obf_152 = _fn_27(_obf_135, _obf_151, _obf_144, _obf_145, preserve_api)
            if _obf_152:
                _obf_149.append(_obf_136)
                print(f'   ✅ {_obf_136}')
            else:
                print(f'   ❌ Failed: {_obf_136}')
        except Exception as e:
            print(f'   ❌ Error: {_obf_136} - {e}')
    for _obf_135, _obf_136 in _obf_140:
        _obf_151 = _obf_128 / _obf_136
        _obf_151.parent.mkdir(parents=True, exist_ok=True)
        print(f'📄 Copying: {_obf_136}')
        try:
            shutil.copy2(_obf_135, _obf_151)
            _obf_150.append(_obf_136)
            print(f'   ✅ {_obf_136}')
        except Exception as e:
            print(f'   ❌ Error: {_obf_136} - {e}')
    print()
    print(f'🎉 Directory processing complete!')
    print(f'   📊 Python files obfuscated: {len(_obf_149)}/{len(_obf_137)}')
    print(f'   📄 Other files copied: {len(_obf_150)}/{len(_obf_140)}')
    print(f'   📦 Total files processed: {len(_obf_149) + len(_obf_150)}/{len(_obf_129)}')
    if bind_machine:
        print(f'   🔒 Machine binding: ENABLED (ID: {_obf_144[:16]}...)')
        print(f'   ⏰ License expires: {time.ctime(_obf_146)}')
    else:
        print(f'   🔓 Machine binding: DISABLED')
    return True

def obfuscate_file_single(input_file, output_file, machine_id=None, license_key=None, preserve_api=True):
    """Obfuscate a single file with pre-computed license info"""
    try:
        with open(input_file, 'r', encoding=_decrypt_str('206')) as _obf_153:
            _obf_154 = _obf_153.read()
        _obf_155 = _decrypt_str('207') in _obf_154 and _decrypt_str('208') in _obf_154 and (_decrypt_str('209') in _obf_154)
        if _obf_155:
            with open(output_file, 'w', encoding=_decrypt_str('210')) as _obf_153:
                _obf_153.write(_obf_154)
            return True
        _obf_156, _obf_157 = extract_future_imports(_obf_154)
        _obf_157 = strip_existing_runtime_code(_obf_157)
        if 'from __future__ import' in _obf_156 and 'from __future__ import' in _obf_157:
            _obf_158 = _obf_157.splitlines()
            _obf_158 = [_obf_159 for _obf_159 in _obf_158 if 'from __future__ import' not in _obf_159]
            _obf_157 = '\n'.join(_obf_158)
        _obf_160 = Path(input_file)
        _obf_161 = _obf_160.name == _decrypt_str('211') or _obf_160.name == _decrypt_str('212')
        if _obf_161:
            _obf_162 = _obf_157
        else:
            _obf_163 = ast.parse(_obf_157, filename=str(input_file))
            _obf_164 = NameCollector()
            _obf_164.visit(_obf_163)
            _obf_165 = Obfuscator(odoo_field_names=_obf_164.field_names, collected_methods=_obf_164.method_names, preserve_public_api=preserve_api)
            _obf_166 = _obf_165.visit(_obf_163)
            _obf_167 = repr(_obf_165.strings)
            _obf_168 = generate_runtime(machine_id, license_key)
            _obf_168 = _obf_168.replace(_decrypt_str('213'), f'_STRINGS = {_obf_167}')
            try:
                _obf_169 = ast.unparse(_obf_166)
                _obf_170 = _obf_169.splitlines()
                _obf_170 = [_obf_171 for _obf_171 in _obf_170 if 'from __future__ import' not in _obf_171]
                _obf_169 = '\n'.join(_obf_170)
                _obf_172 = _obf_168.replace(_decrypt_str('214'), _obf_169)
            except AttributeError:
                _obf_172 = _obf_168.replace(_decrypt_str('215'), '# Obfuscated AST (requires Python 3.9+ for ast.unparse)\n' + _obf_157)
            if _obf_156:
                _obf_162 = _obf_156 + '\n' + _obf_172
            else:
                _obf_162 = _obf_172
        with open(output_file, 'w', encoding=_decrypt_str('216')) as _obf_153:
            _obf_153.write(_obf_162)
        return True
    except Exception as e:
        print(f'   Error obfuscating {input_file}: {e}')
        return False

def obfuscate_file(input_file, output_file, bind_machine=False, expiration_days=365, preserve_api=True, project_url=None):
    """Obfuscate a single Python file with optional machine binding"""
    _obf_173 = Path(output_file)
    create_backup(_obf_173)
    print(f'Obfuscating {input_file} -> {output_file}')
    _obf_174 = None
    _obf_175 = None
    if bind_machine:
        print(_decrypt_str('217'))
        _obf_174 = get_machine_id()
        _obf_175, _obf_176 = generate_license_key(_obf_174, expiration_days)
        print(f'📋 Machine ID: {_obf_174}')
        print(f'🔑 License Key: {_obf_175}')
        print(f'⏰ Expires: {time.ctime(_obf_176)}')
        _obf_177 = output_file + _decrypt_str('218')
        with open(_obf_177, 'w', encoding=_decrypt_str('219')) as _obf_178:
            _obf_178.write(f'Machine ID: {_obf_174}\n')
            _obf_178.write(f'License Key: {_obf_175}\n')
            _obf_178.write(f'Expires: {time.ctime(_obf_176)}\n')
            if project_url:
                _obf_178.write(f'Project URL: {project_url}\n')
        print(f'💾 License saved to: {_obf_177}')
        if project_url:
            print(f'🔗 Project URL: {project_url}')
    _obf_179 = Path(input_file)
    _obf_180 = _obf_179.name == _decrypt_str('220') or _obf_179.name == _decrypt_str('221')
    with open(input_file, 'r', encoding=_decrypt_str('222')) as _obf_178:
        _obf_181 = _obf_178.read()
    if _obf_180:
        _obf_182 = _obf_181
    else:
        _obf_183 = ast.parse(_obf_181, filename=input_file)
        _obf_184 = NameCollector()
        _obf_184.visit(_obf_183)
        _obf_185 = Obfuscator(odoo_field_names=_obf_184.field_names, collected_methods=_obf_184.method_names, preserve_public_api=preserve_api)
        _obf_186 = _obf_185.visit(_obf_183)
        _obf_187 = repr(_obf_185.strings)
        _obf_188 = generate_runtime(_obf_174, _obf_175)
        _obf_188 = _obf_188.replace(_decrypt_str('223'), f'_STRINGS = {_obf_187}')
        try:
            _obf_189 = ast.unparse(_obf_186)
            _obf_182 = _obf_188.replace(_decrypt_str('224'), _obf_189)
        except Exception as e:
            print(f'⚠️  AST unparsing failed ({e}), using fallback')
            _obf_182 = _obf_188.replace(_decrypt_str('225'), '# Obfuscated AST (unparsing failed)\n' + _obf_181)
    _obf_173 = Path(output_file)
    _obf_173.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding=_decrypt_str('226')) as _obf_178:
        _obf_178.write(_obf_182)
    if _obf_180:
        print(f'✅ Manifest file copied without obfuscation (Odoo compatibility)')
    else:
        print(f'✅ Obfuscated {len(_obf_185.var_map)} variables')
        print(f'✅ Encrypted {len(_obf_185.strings)} strings')
        if _obf_185.public_names:
            print(f'✅ Preserved {len(_obf_185.public_names)} public API names (importable)')
        if bind_machine:
            print(f'✅ Machine binding enabled (ID: {_obf_174[:16]}...)')
if __name__ == _decrypt_str('227'):
    import argparse
    _obf_190 = argparse.ArgumentParser(description='PyProtect - Python Obfuscator with Machine ID Binding')
    _obf_190.add_argument('-i', _decrypt_str('228'), help='Input Python file or directory (not needed with -m)')
    _obf_190.add_argument('-o', _decrypt_str('229'), default=str(get_default_output_path()), help='Output obfuscated file or directory (default: PyProtect/dist/filename or PyProtect/dist/inputname/)')
    _obf_190.add_argument('-d', _decrypt_str('231'), action=_decrypt_str('230'), help='Deploy mode: backup original and replace in-place (ignores -o)')
    _obf_190.add_argument('-r', _decrypt_str('232'), help='Restore from backup: specify backup path (e.g., module.backup_20251209_125530)')
    _obf_190.add_argument('-u', _decrypt_str('233'), help='Project URL to embed in license file (e.g., https://github.com/user/repo)')
    _obf_190.add_argument('-m', _decrypt_str('235'), action=_decrypt_str('234'), help='Display current machine ID and exit')
    _obf_190.add_argument('-c', _decrypt_str('236'), nargs='?', const='.', help='Check license validity in directory (default: current dir)')
    _obf_190.add_argument('-b', _decrypt_str('239'), action=_decrypt_str('237'), help=_decrypt_str('238'))
    _obf_190.add_argument('-e', _decrypt_str('240'), type=int, default=365, help='License expiration in days (default: 365)')
    _obf_190.add_argument(_decrypt_str('242'), action=_decrypt_str('241'), help='Obfuscate all names including public API (may break imports)')
    _obf_191 = _obf_190.parse_args()
    if _obf_191.restore:
        _obf_192 = restore_from_backup(_obf_191.restore)
        sys.exit(0 if _obf_192 else 1)
    if _obf_191.machine_id:
        _obf_193 = get_machine_id()
        print(_decrypt_str('243'))
        print('=' * 50)
        print(f'Machine ID: {_obf_193}')
        print(f'Length: {len(_obf_193)} characters')
        print()
        print('This ID will be used for machine binding.')
        print('Copy this ID if you need to manually configure licensing.')
        sys.exit(0)
    if _obf_191.check_license:
        check_license_status(_obf_191.check_license)
        sys.exit(0)
    if not _obf_191.input:
        print('❌ Error: Input file or directory is required (use -i flag)')
        print("Run 'python3 pyprotect.py --help' for usage information")
        sys.exit(1)
    _obf_194 = Path(_obf_191.input)
    if not _obf_194.exists():
        print(f'❌ Input path not found: {_obf_191.input}')
        sys.exit(1)
    _obf_195 = time.strftime(_decrypt_str('244'))
    if _obf_194.is_dir():
        _obf_196 = _obf_194.parent / f'{_obf_194.name}.backup_{_obf_195}'
    else:
        _obf_196 = _obf_194.parent / f'{_obf_194.stem}.backup_{_obf_195}{_obf_194.suffix}'
    print(f'📦 Creating backup of input: {_obf_196.name}')
    try:
        if _obf_194.is_dir():
            shutil.copytree(str(_obf_194), str(_obf_196))
        else:
            shutil.copy2(str(_obf_194), str(_obf_196))
        print(f'✅ Input backed up to: {_obf_196}')
        print()
    except Exception as e:
        print(f'⚠️  Warning: Could not create input backup: {e}')
        print(_decrypt_str('245'))
        print()
    _obf_195 = time.strftime(_decrypt_str('246'))
    if _obf_191.deploy:
        print('🚀 Deploy mode: Will backup and replace original')
        if _obf_194.is_dir():
            _obf_197 = _obf_194.parent / f'{_obf_194.name}.backup_{_obf_195}'
        else:
            _obf_197 = _obf_194.parent / f'{_obf_194.stem}.backup_{_obf_195}{_obf_194.suffix}'
        _obf_198 = get_default_output_path()
        if _obf_194.is_dir():
            _obf_199 = _obf_198 / _obf_194.name
        else:
            _obf_199 = _obf_198 / _obf_194.name
        print(f'📦 Backup will be created at: {_obf_197}')
        print(f'🎯 Protected code will replace: {_obf_194}')
        print()
    else:
        _obf_198 = get_default_output_path()
        _obf_200 = Path(_obf_191.output).absolute()
        if _obf_194.is_dir():
            _obf_199 = _obf_200 / _obf_194.name
        else:
            _obf_199 = _obf_200 / _obf_194.name
    try:
        _obf_201 = not _obf_191.no_preserve_api
        if _obf_194.is_dir():
            print(_decrypt_str('247'))
            print('=' * 50)
            if _obf_201:
                print(_decrypt_str('248'))
            else:
                print(_decrypt_str('249'))
            print()
            _obf_192 = obfuscate_directory(str(_obf_194), str(_obf_199), bind_machine=_obf_191.bind_machine, expiration_days=_obf_191.expiration, preserve_api=_obf_201, project_url=_obf_191.url)
            if _obf_192:
                print('\n✅ Directory obfuscation complete!')
                if _obf_191.deploy:
                    print('\n' + '=' * 60)
                    print('🚀 Deploy Mode: Ready to backup and replace')
                    print('=' * 60)
                    print(f'📂 Original: {_obf_194}')
                    print(f'📦 Backup will be: {_obf_197}')
                    print(f'✨ Protected code at: {_obf_199}')
                    print()
                    _obf_202 = input('⚠️  Proceed with backup and replacement? (y/n): ').strip().lower()
                    if _obf_202 in ['y', 'yes']:
                        print('\n🔄 Deploying...')
                        try:
                            if _obf_197.exists():
                                print(f'⚠️  Backup path already exists: {_obf_197}')
                                print(_decrypt_str('250'))
                                if _obf_197.is_dir():
                                    shutil.rmtree(str(_obf_197))
                                else:
                                    _obf_197.unlink()
                                print(f'   ✅ Removed existing backup')
                            shutil.move(str(_obf_194), str(_obf_197))
                            print(f'✅ Original backed up to: {_obf_197}')
                            shutil.move(str(_obf_199), str(_obf_194))
                            print(f'✅ Protected version deployed to: {_obf_194}')
                            print(f'\n💡 To restore: mv {_obf_197} {_obf_194}')
                        except Exception as e:
                            print(f'\n❌ Deploy failed: {e}')
                            print(f'⚠️  Protected files are still at: {_obf_199}')
                            import traceback
                            traceback.print_exc()
                            sys.exit(1)
                    else:
                        print('\n🛑 Deploy cancelled by user')
                        print(f'📁 Protected files remain at: {_obf_199}')
                        print(f'📁 Original untouched at: {_obf_194}')
                        print('\n💡 To deploy manually:')
                        print(f'   mv {_obf_194} {_obf_197}')
                        print(f'   mv {_obf_199} {_obf_194}')
                if _obf_191.bind_machine:
                    print('\n⚠️  WARNING: All code is now bound to the current machine!')
                    print(f"   Only machines with Machine ID '{get_machine_id()[:16]}...' can run it.")
                    print(f'   License expires in {_obf_191.expiration} days.')
            else:
                print('\n❌ Directory obfuscation failed!')
                sys.exit(1)
        else:
            print(_decrypt_str('251'))
            print('=' * 50)
            if _obf_201:
                print(_decrypt_str('252'))
            else:
                print(_decrypt_str('253'))
            print()
            obfuscate_file(str(_obf_194), str(_obf_199), bind_machine=_obf_191.bind_machine, expiration_days=_obf_191.expiration, preserve_api=_obf_201, project_url=_obf_191.url)
            print(f'\n✅ File obfuscation complete: {_obf_199}')
            if _obf_191.deploy:
                print('\n' + '=' * 60)
                print('🚀 Deploy Mode: Ready to backup and replace')
                print('=' * 60)
                print(f'📄 Original file: {_obf_194}')
                print(f'📦 Backup will be: {_obf_197}')
                print(f'✨ Protected file at: {_obf_199}')
                print()
                _obf_202 = input('⚠️  Proceed with backup and replacement? (y/n): ').strip().lower()
                if _obf_202 in ['y', 'yes']:
                    print('\n🔄 Deploying...')
                    try:
                        if _obf_197.exists():
                            print(f'⚠️  Backup path already exists: {_obf_197}')
                            print(_decrypt_str('254'))
                            if _obf_197.is_dir():
                                shutil.rmtree(str(_obf_197))
                            else:
                                _obf_197.unlink()
                            print(f'   ✅ Removed existing backup')
                        shutil.move(str(_obf_194), str(_obf_197))
                        print(f'✅ Original backed up to: {_obf_197}')
                        shutil.move(str(_obf_199), str(_obf_194))
                        print(f'✅ Protected version deployed to: {_obf_194}')
                        print(f'\n💡 To restore: mv {_obf_197} {_obf_194}')
                    except Exception as e:
                        print(f'\n❌ Deploy failed: {e}')
                        print(f'⚠️  Protected file is still at: {_obf_199}')
                        import traceback
                        traceback.print_exc()
                        sys.exit(1)
                else:
                    print('\n🛑 Deploy cancelled by user')
                    print(f'📁 Protected file remains at: {_obf_199}')
                    print(f'📁 Original untouched at: {_obf_194}')
                    print('\n💡 To deploy manually:')
                    print(f'   mv {_obf_194} {_obf_197}')
                    print(f'   mv {_obf_199} {_obf_194}')
            if _obf_191.bind_machine:
                print('\n⚠️  WARNING: This code is now bound to the current machine!')
                print(f"   Only machines with Machine ID '{get_machine_id()[:16]}...' can run it.")
                print(f'   License expires in {_obf_191.expiration} days.')
    except Exception as e:
        print(f'❌ Obfuscation failed: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)
