"""
PyProtect - Advanced Python Code Obfuscator with Machine ID Binding

A comprehensive Python code obfuscation tool with hardware binding,
designed to protect Python applications from reverse engineering.
"""

__version__ = "2.1.2"
__author__ = "PyProtect Team"

from .main import (
    get_machine_id,
    check_license_status,
    obfuscate_file,
    obfuscate_directory,
)

# Export CLI entry point
from .cli import main as cli_main

__all__ = [
    "get_machine_id",
    "check_license_status",
    "obfuscate_file",
    "obfuscate_directory",
    "cli_main",
]

