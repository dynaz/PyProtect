#!/usr/bin/env python3
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

def get_default_output_path():
    """Get the default output path in PyProtect/dist directory"""
    script_dir = Path(__file__).parent.absolute()
    return script_dir / "dist"

def create_backup(output_path):
    """Create a backup of existing output before overwriting"""
    if output_path.exists():
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_name = f"{output_path.name}_backup_{timestamp}"

        if output_path.is_dir():
            backup_path = output_path.parent / backup_name
            try:
                shutil.copytree(str(output_path), str(backup_path))
                print(f"📦 Created backup: {backup_path}")
            except Exception as e:
                print(f"⚠️  Warning: Could not create directory backup: {e}")
        else:
            backup_path = output_path.parent / backup_name
            try:
                shutil.copy2(str(output_path), str(backup_path))
                print(f"📦 Created backup: {backup_path}")
            except Exception as e:
                print(f"⚠️  Warning: Could not create file backup: {e}")

def get_machine_id():
    """Generate a unique machine identifier based on hardware"""
    components = []

    try:
        # CPU info
        cpu_info = platform.processor()
        if cpu_info:
            components.append(f"cpu:{cpu_info}")
    except:
        pass

    try:
        # Machine name
        machine = platform.machine()
        if machine:
            components.append(f"arch:{machine}")
    except:
        pass

    try:
        # MAC address
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                       for elements in range(0, 2*6, 2)][::-1])
        components.append(f"mac:{mac}")
    except:
        pass

    try:
        # Disk serial (Linux)
        result = subprocess.run(['lsblk', '-o', 'SERIAL', '-n', '-d'],
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout.strip():
            disk_serial = result.stdout.strip().split('\n')[0]
            if disk_serial:
                components.append(f"disk:{disk_serial}")
    except:
        pass

    # Combine all components
    combined = '|'.join(components)

    # Generate consistent hash
    machine_id = hashlib.sha256(combined.encode()).hexdigest()[:32]

    return machine_id

def check_license_status(directory):
    """Check license status in the specified directory"""
    print("🔍 Checking License Status:")
    print("="*50)

    license_dir = Path(directory)

    if not license_dir.exists():
        print(f"❌ Directory not found: {directory}")
        return

    # Look for license files
    license_files = []
    license_files.extend(license_dir.glob("*.license"))
    license_files.extend(license_dir.glob("project.license"))

    if not license_files:
        print(f"❌ No license files found in: {directory}")
        print("Looked for: *.license, project.license")
        return

    print(f"Found {len(license_files)} license file(s):")
    current_machine_id = get_machine_id()

    for license_file in license_files:
        print(f"\n📄 License File: {license_file.name}")
        print("-" * 30)

        try:
            with open(license_file, 'r') as f:
                content = f.read().strip()

            lines = content.split('\n')
            license_info = {}

            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    license_info[key.strip()] = value.strip()

            # Extract license data
            machine_id = license_info.get('Machine ID', 'Unknown')
            license_key = license_info.get('License Key', 'Unknown')
            expires_str = license_info.get('Expires', 'Unknown')
            protected_date = license_info.get('Protected', 'Unknown')

            print(f"Machine ID: {machine_id}")
            print(f"License Key: {license_key}")
            print(f"Expires: {expires_str}")
            print(f"Protected: {protected_date}")

            # Validate license
            if license_key and license_key != 'Unknown':
                is_valid, message = verify_license_key(license_key)
                status = "✅ VALID" if is_valid else "❌ INVALID"
                print(f"Status: {status} - {message}")

                # Additional checks
                if machine_id == current_machine_id:
                    print("✅ Machine ID matches current machine")
                else:
                    print("⚠️  Machine ID does not match current machine")
                    print(f"   License Machine: {machine_id}")
                    print(f"   Current Machine: {current_machine_id}")

            else:
                print("❌ Invalid license key format")

        except Exception as e:
            print(f"❌ Error reading license file: {e}")

    print("\n" + "="*50)
    print("💡 Tip: Use 'python3 pyprotect.py -m' to see your current machine ID")

def generate_license_key(machine_id, expiration_days=365):
    """Generate a license key for the machine"""
    expiration = int(time.time()) + (expiration_days * 24 * 60 * 60)

    # Create license data
    license_data = f"{machine_id}:{expiration}"

    # Sign with a simple hash
    signature = hashlib.sha256(f"secret_salt:{license_data}".encode()).hexdigest()[:16]

    license_key = f"{license_data}:{signature}"

    return license_key, expiration

def verify_license_key(license_key):
    """Verify if license is valid for current machine"""
    try:
        parts = license_key.split(':')
        if len(parts) != 3:
            return False, "Invalid license format"

        machine_id = parts[0]
        expiration = int(parts[1])
        signature = parts[2]

        # Check expiration
        current_time = int(time.time())
        if current_time > expiration:
            return False, "License expired"

        # Verify signature
        expected_signature = hashlib.sha256(f"secret_salt:{machine_id}:{expiration}".encode()).hexdigest()[:16]
        if signature != expected_signature:
            return False, "Invalid license signature"

        # Check machine ID
        current_machine_id = get_machine_id()
        if machine_id != current_machine_id:
            return False, "License not valid for this machine"

        return True, "License valid"

    except Exception as e:
        return False, f"License verification error: {e}"

class Obfuscator(ast.NodeTransformer):
    """AST-based obfuscator"""

    def __init__(self):
        self.var_count = 0
        self.var_map = {}
        self.strings = []

    def generate_var_name(self):
        """Generate obfuscated variable name"""
        name = f"_obf_{self.var_count}"
        self.var_count += 1
        return name

    def visit_Name(self, node):
        """Obfuscate variable names"""
        if isinstance(node.ctx, ast.Store):
            if node.id not in self.var_map:
                self.var_map[node.id] = self.generate_var_name()
            node.id = self.var_map[node.id]
        elif isinstance(node.ctx, ast.Load):
            if node.id in self.var_map:
                node.id = self.var_map[node.id]
        return node

    def visit_Constant(self, node):
        """Encrypt string literals"""
        if isinstance(node.value, str) and len(node.value) > 3:  # Only encrypt longer strings
            encrypted = base64.b64encode(node.value.encode()).decode()
            self.strings.append(encrypted)
            # Replace with decryption call
            return ast.Call(
                func=ast.Name(id='_decrypt_str', ctx=ast.Load()),
                args=[ast.Constant(value=str(len(self.strings)-1))],
                keywords=[]
            )
        return node

def generate_runtime(machine_id=None, license_key=None):
    """Generate runtime decryption and license verification functions"""
    license_check = ""
    if license_key:
        license_check = f'''
    # License verification
    _LICENSE_KEY = "{license_key}"

def _get_machine_id():
    """Generate machine identifier"""
    import hashlib
    import platform
    import uuid
    import subprocess

    components = []
    try:
        cpu_info = platform.processor()
        if cpu_info:
            components.append(f"cpu:{{cpu_info}}")
    except:
        pass

    try:
        machine = platform.machine()
        if machine:
            components.append(f"arch:{{machine}}")
    except:
        pass

    try:
        mac = ':'.join(['{{:02x}}'.format((uuid.getnode() >> elements) & 0xff)
                       for elements in range(0, 2*6, 2)][::-1])
        components.append(f"mac:{{mac}}")
    except:
        pass

    try:
        result = subprocess.run(['lsblk', '-o', 'SERIAL', '-n', '-d'],
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout.strip():
            disk_serial = result.stdout.strip().split('\\n')[0]
            if disk_serial:
                components.append(f"disk:{{disk_serial}}")
    except:
        pass

    combined = '|'.join(components)
    machine_id = hashlib.sha256(combined.encode()).hexdigest()[:32]
    return machine_id

def _verify_license_key(license_key):
    """Verify license validity"""
    import hashlib
    import time

    try:
        parts = license_key.split(':')
        if len(parts) != 3:
            return False

        machine_id = parts[0]
        expiration = int(parts[1])
        signature = parts[2]

        current_time = int(time.time())
        if current_time > expiration:
            return False

        expected_signature = hashlib.sha256(f"secret_salt:{{machine_id}}:{{expiration}}".encode()).hexdigest()[:16]
        if signature != expected_signature:
            return False

        current_machine_id = _get_machine_id()
        if machine_id != current_machine_id:
            return False

        return True
    except:
        return False

def _check_license():
    """Verify license on startup"""
    if not _verify_license_key(_LICENSE_KEY):
        print("ERROR: Invalid or expired license!")
        print("This software is licensed to run on a different machine.")
        import sys
        sys.exit(1)

# Check license immediately
_check_license()
'''

    runtime_code = f'''
import base64
import sys

_STRINGS = []  # Will be populated by obfuscator

def _decrypt_str(index):
    """Decrypt string at given index"""
    encrypted = _STRINGS[int(index)]
    return base64.b64decode(encrypted).decode()

{license_check}
# Obfuscated code will be inserted here
'''

    return runtime_code

def obfuscate_directory(input_dir, output_dir, bind_machine=False, expiration_days=365):
    """Obfuscate all Python files in a directory recursively"""
    print(f"🔍 Scanning directory: {input_dir}")
    print(f"📁 Output directory: {output_dir}")
    print()

    input_path = Path(input_dir)
    output_path = Path(output_dir)

    if not input_path.exists():
        print(f"❌ Input directory not found: {input_dir}")
        return False

    if not input_path.is_dir():
        print(f"❌ Input path is not a directory: {input_dir}")
        return False

    # Create backup if output already exists
    create_backup(output_path)

    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)

    # Find all files (not just Python files)
    all_files = []
    for root, dirs, files in os.walk(input_path):
        # Skip __pycache__ directories
        dirs[:] = [d for d in dirs if not d.startswith('__pycache__')]
        for file in files:
            file_path = Path(root) / file
            rel_path = file_path.relative_to(input_path)
            all_files.append((file_path, rel_path))

    if not all_files:
        print("❌ No files found in the directory")
        return False

    # Separate Python and non-Python files
    python_files = [(fp, rp) for fp, rp in all_files if fp.suffix == '.py']
    non_python_files = [(fp, rp) for fp, rp in all_files if fp.suffix != '.py']

    print(f"📋 Found {len(all_files)} total files:")
    print(f"   • {len(python_files)} Python files to obfuscate")
    print(f"   • {len(non_python_files)} other files to copy")
    if python_files:
        print("   📝 Python files:")
        for _, rel_path in python_files:
            print(f"      • {rel_path}")
    if non_python_files:
        print("   📄 Other files:")
        for _, rel_path in non_python_files:
            print(f"      • {rel_path}")
    print()

    # Generate machine ID and license once for the whole project
    machine_id = None
    license_key = None

    if bind_machine:
        print("🔒 Generating machine binding license for project...")
        machine_id = get_machine_id()
        license_key, expiration = generate_license_key(machine_id, expiration_days)

        print(f"📋 Machine ID: {machine_id}")
        print(f"🔑 License Key: {license_key}")
        print(f"⏰ Expires: {time.ctime(expiration)}")
        print()

        # Save license info
        license_file = output_path / "project.license"
        with open(license_file, 'w') as f:
            f.write(f"Machine ID: {machine_id}\n")
            f.write(f"License Key: {license_key}\n")
            f.write(f"Expires: {time.ctime(expiration)}\n")
            f.write(f"Protected: {time.ctime(time.time())}\n")
        print(f"💾 Project license saved to: {license_file}")
        print()

    # Process all files
    processed_files = []
    copied_files = []

    # Process Python files (obfuscate)
    for file_path, rel_path in python_files:
        output_file = output_path / rel_path

        # Create output subdirectory if needed
        output_file.parent.mkdir(parents=True, exist_ok=True)

        print(f"🔧 Obfuscating: {rel_path}")

        try:
            # Use the same machine_id and license_key for all files in the project
            success = obfuscate_file_single(file_path, output_file, machine_id, license_key)
            if success:
                processed_files.append(rel_path)
                print(f"   ✅ {rel_path}")
            else:
                print(f"   ❌ Failed: {rel_path}")
        except Exception as e:
            print(f"   ❌ Error: {rel_path} - {e}")

    # Process non-Python files (copy as-is)
    for file_path, rel_path in non_python_files:
        output_file = output_path / rel_path

        # Create output subdirectory if needed
        output_file.parent.mkdir(parents=True, exist_ok=True)

        print(f"📄 Copying: {rel_path}")

        try:
            shutil.copy2(file_path, output_file)
            copied_files.append(rel_path)
            print(f"   ✅ {rel_path}")
        except Exception as e:
            print(f"   ❌ Error: {rel_path} - {e}")

    print()
    print(f"🎉 Directory processing complete!")
    print(f"   📊 Python files obfuscated: {len(processed_files)}/{len(python_files)}")
    print(f"   📄 Other files copied: {len(copied_files)}/{len(non_python_files)}")
    print(f"   📦 Total files processed: {len(processed_files) + len(copied_files)}/{len(all_files)}")

    if bind_machine:
        print(f"   🔒 Machine binding: ENABLED (ID: {machine_id[:16]}...)")
        print(f"   ⏰ License expires: {time.ctime(expiration)}")
    else:
        print(f"   🔓 Machine binding: DISABLED")

    return True

def obfuscate_file_single(input_file, output_file, machine_id=None, license_key=None):
    """Obfuscate a single file with pre-computed license info"""
    try:
        # Read source
        with open(input_file, 'r', encoding='utf-8') as f:
            source = f.read()

        # Parse AST
        tree = ast.parse(source, filename=str(input_file))

        # Apply obfuscation
        obfuscator = Obfuscator()
        obfuscated_tree = obfuscator.visit(tree)

        # Generate runtime code with strings and license
        strings_repr = repr(obfuscator.strings)
        runtime_code = generate_runtime(machine_id, license_key)

        # Replace the placeholder in runtime code
        runtime_code = runtime_code.replace('_STRINGS = []', f'_STRINGS = {strings_repr}')

        # Convert AST back to source
        try:
            # Use ast.unparse if available (Python 3.9+)
            obfuscated_source = ast.unparse(obfuscated_tree)
            output_code = runtime_code.replace('# Obfuscated code will be inserted here', obfuscated_source)
        except AttributeError:
            # Fallback for older Python versions
            output_code = runtime_code.replace('# Obfuscated code will be inserted here',
                                             "# Obfuscated AST (requires Python 3.9+ for ast.unparse)\n" + source)

        # Write output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_code)

        return True

    except Exception as e:
        print(f"   Error obfuscating {input_file}: {e}")
        return False

def obfuscate_file(input_file, output_file, bind_machine=False, expiration_days=365):
    """Obfuscate a single Python file with optional machine binding"""
    output_path = Path(output_file)

    # Create backup if output already exists
    create_backup(output_path)

    print(f"Obfuscating {input_file} -> {output_file}")

    # Generate license if binding is requested
    machine_id = None
    license_key = None

    if bind_machine:
        print("🔒 Generating machine binding license...")
        machine_id = get_machine_id()
        license_key, expiration = generate_license_key(machine_id, expiration_days)

        print(f"📋 Machine ID: {machine_id}")
        print(f"🔑 License Key: {license_key}")
        print(f"⏰ Expires: {time.ctime(expiration)}")

        # Save license info
        license_file = output_file + '.license'
        with open(license_file, 'w') as f:
            f.write(f"Machine ID: {machine_id}\n")
            f.write(f"License Key: {license_key}\n")
            f.write(f"Expires: {time.ctime(expiration)}\n")
        print(f"💾 License saved to: {license_file}")

    # Read source
    with open(input_file, 'r') as f:
        source = f.read()

    # Parse AST
    tree = ast.parse(source, filename=input_file)

    # Apply obfuscation
    obfuscator = Obfuscator()
    obfuscated_tree = obfuscator.visit(tree)

    # Generate runtime code with strings and license
    strings_repr = repr(obfuscator.strings)
    runtime_code = generate_runtime(machine_id, license_key)

    # Replace the placeholder in runtime code
    runtime_code = runtime_code.replace('_STRINGS = []', f'_STRINGS = {strings_repr}')

    # Convert AST back to source using built-in ast.unparse (Python 3.9+)
    try:
        # Use ast.unparse if available (Python 3.9+)
        obfuscated_source = ast.unparse(obfuscated_tree)
        output_code = runtime_code.replace('# Obfuscated code will be inserted here', obfuscated_source)
    except AttributeError:
        # Fallback for older Python versions
        output_code = runtime_code.replace('# Obfuscated code will be inserted here',
                                         "# Obfuscated AST (requires Python 3.9+ for ast.unparse)\n" + source)

    # Ensure output directory exists
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_code)

    print(f"✅ Obfuscated {len(obfuscator.var_map)} variables")
    print(f"✅ Encrypted {len(obfuscator.strings)} strings")
    if bind_machine:
        print(f"✅ Machine binding enabled (ID: {machine_id[:16]}...)")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PyProtect - Python Obfuscator with Machine ID Binding")
    parser.add_argument("-i", "--input",
                       help="Input Python file or directory (not needed with -m)")
    parser.add_argument("-o", "--output", default=str(get_default_output_path()),
                       help="Output obfuscated file or directory (default: PyProtect/dist/filename or PyProtect/dist/inputname/)")
    parser.add_argument("-m", "--machine-id", action="store_true",
                       help="Display current machine ID and exit")
    parser.add_argument("-c", "--check-license", nargs='?', const=".",
                       help="Check license validity in directory (default: current dir)")
    parser.add_argument("--bind-machine", action="store_true",
                       help="Bind obfuscated code to current machine")
    parser.add_argument("--expiration", type=int, default=365,
                       help="License expiration in days (default: 365)")

    args = parser.parse_args()

    # Handle machine ID display
    if args.machine_id:
        machine_id = get_machine_id()
        print("🔍 Current Machine ID:")
        print("="*50)
        print(f"Machine ID: {machine_id}")
        print(f"Length: {len(machine_id)} characters")
        print()
        print("This ID will be used for machine binding.")
        print("Copy this ID if you need to manually configure licensing.")
        sys.exit(0)

    # Handle license checking
    if args.check_license:
        check_license_status(args.check_license)
        sys.exit(0)

    # Validate input is provided when not using machine-id flag
    if not args.input:
        print("❌ Error: Input file or directory is required (use -i flag)")
        print("Run 'python3 pyprotect.py --help' for usage information")
        sys.exit(1)

    input_path = Path(args.input)

    if not input_path.exists():
        print(f"❌ Input path not found: {args.input}")
        sys.exit(1)

    # Determine output path
    default_dist_path = get_default_output_path()
    resolved_output = Path(args.output).absolute()

    if input_path.is_dir():
        # Directory input -> always create input_dirname subdirectory
        output_path = resolved_output / input_path.name
    else:
        # File input -> create filename in output directory
        output_path = resolved_output / input_path.name

    try:
        if input_path.is_dir():
            # Directory mode
            print("🏗️  Directory obfuscation mode")
            print("="*50)
            success = obfuscate_directory(
                str(input_path), str(output_path),
                bind_machine=args.bind_machine,
                expiration_days=args.expiration
            )

            if success:
                print("\n✅ Directory obfuscation complete!")
                if args.bind_machine:
                    print("\n⚠️  WARNING: All code is now bound to the current machine!")
                    print(f"   Only machines with Machine ID '{get_machine_id()[:16]}...' can run it.")
                    print(f"   License expires in {args.expiration} days.")
            else:
                print("\n❌ Directory obfuscation failed!")
                sys.exit(1)

        else:
            # Single file mode
            print("📄 Single file obfuscation mode")
            print("="*50)
            obfuscate_file(str(input_path), str(output_path),
                          bind_machine=args.bind_machine,
                          expiration_days=args.expiration)
            print(f"\n✅ File obfuscation complete: {output_path}")

            if args.bind_machine:
                print("\n⚠️  WARNING: This code is now bound to the current machine!")
                print(f"   Only machines with Machine ID '{get_machine_id()[:16]}...' can run it.")
                print(f"   License expires in {args.expiration} days.")

    except Exception as e:
        print(f"❌ Obfuscation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

