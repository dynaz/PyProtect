#!/usr/bin/env python3
"""
PyProtect Enhanced - Advanced Python Obfuscator with Machine ID Binding
======================================================================

Enhanced Features:
- Advanced multi-layer string encryption (XOR + Base64)
- Confusing variable name obfuscation with patterns
- Control flow obfuscation with junk code injection
- Anti-debugging and environment protection
- Code integrity verification
- Dummy functions and dead code injection
- Machine ID binding and license verification
- Hardware fingerprinting
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
import random
import threading
from pathlib import Path

def _check_environment():
    """Enhanced anti-debugging and environment checks"""
    suspicious_processes = ['ida', 'ollydbg', 'x64dbg', 'windbg', 'gdb', 'lldb', 'radare2', 'cheat', 'processhacker']
    
    try:
        if platform.system() == 'Windows':
            try:
                import ctypes
                # Check if debugger is present (Windows)
                if ctypes.windll.kernel32.IsDebuggerPresent():
                    time.sleep(random.uniform(1, 3))
                    sys.exit(0)
            except:
                pass
        
        # Check for suspicious environment variables
        suspicious_vars = ['_', 'PYTHONPATH', 'PYCHARM_HOSTED', 'VSCODE_PID', 'TERM_PROGRAM']
        for var in suspicious_vars:
            if var in os.environ and any(debug_term in os.environ.get(var, '').lower() 
                                       for debug_term in ['debug', 'pycharm', 'vscode', 'ida']):
                time.sleep(random.uniform(1, 3))
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
                    time.sleep(random.uniform(0.5, 2))
                    sys.exit(0)
        except:
            pass  # Ignore errors in process checking
            
    except Exception:
        pass  # Ignore all errors to avoid breaking legitimate usage

# Run environment check immediately
_check_environment()

def _verify_code_integrity():
    """Enhanced code integrity verification"""
    try:
        # Get current file path
        current_file = __file__
        
        # Calculate file hash
        with open(current_file, 'rb') as f:
            file_content = f.read()
            file_hash = hashlib.sha256(file_content).hexdigest()
        
        # Check for expected patterns
        expected_patterns = [b'_decrypt_str', b'_STRINGS', b'def get_machine_id']
        
        for pattern in expected_patterns:
            if pattern not in file_content:
                # Code has been tampered with
                time.sleep(random.uniform(1, 3))
                sys.exit(0)
                
    except Exception:
        # If integrity check fails, continue silently
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
    # Resolve symlinks to get the actual script path
    actual_script_path = Path(__file__).resolve()
    script_dir = actual_script_path.parent.absolute()
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

def restore_from_backup(backup_path):
    """Restore original from backup"""
    import re
    
    backup_path = Path(backup_path)
    
    # Validate backup path exists
    if not backup_path.exists():
        print(f"❌ Backup not found: {backup_path}")
        return False
    
    # Extract original path by removing .backup_TIMESTAMP
    backup_name = backup_path.name
    
    # Try to match the backup pattern
    if backup_path.is_dir():
        match = re.match(r'^(.+)\.backup_\d{8}_\d{6}$', backup_name)
    else:
        match = re.match(r'^(.+)\.backup_\d{8}_\d{6}(\..+)?$', backup_name)
    
    if not match:
        print(f"❌ Not a valid backup name: {backup_name}")
        print("   Backup names should match: name.backup_YYYYMMDD_HHMMSS")
        return False
    
    # Reconstruct original path
    if backup_path.is_dir():
        original_name = match.group(1)
    else:
        original_name = match.group(1) + (match.group(2) or '')
    
    original_path = backup_path.parent / original_name
    
    # Show restore plan
    print("\n" + "="*60)
    print("🔄 Restore Mode")
    print("="*60)
    print(f"📦 Backup: {backup_path}")
    print(f"🎯 Will restore to: {original_path}")
    
    if original_path.exists():
        print(f"⚠️  Current version exists and will be REMOVED")
    else:
        print(f"✅ Target location is empty")
    
    print()
    
    # Ask for confirmation
    response = input("⚠️  Proceed with restore? (y/n): ").strip().lower()
    
    if response not in ['y', 'yes']:
        print("\n🛑 Restore cancelled by user")
        return False
    
    print("\n🔄 Restoring...")
    
    try:
        # Remove current version if it exists
        if original_path.exists():
            if original_path.is_dir():
                shutil.rmtree(str(original_path))
            else:
                original_path.unlink()
            print(f"✅ Removed current version at: {original_path}")
        
        # Restore backup
        shutil.move(str(backup_path), str(original_path))
        print(f"✅ Backup restored to: {original_path}")
        print(f"\n💡 Original restored successfully!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Restore failed: {e}")
        return False

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
            with open(license_file, 'r', encoding='utf-8') as f:
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
    print("💡 Tip: Use 'python pyprotect.py -m' to see your current machine ID")

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

class NameCollector(ast.NodeVisitor):
    """Collect all Odoo field names and method names before obfuscation"""
    
    def __init__(self):
        self.field_names = set()
        self.method_names = {}  # Map method names to whether they should be obfuscated
        # IMPORTANT: Keep this list synchronized with Obfuscator.odoo_method_patterns
        self.odoo_method_patterns = [
            '_compute_', '_inverse_', '_search_', '_onchange_',
            '_depends_', '_constraint_', '_sql_constraint_',
            'action_', 'button_',
            'get_', '_get_', 'set_', '_set_',
            '_check_', '_prepare_',
            '_create_', '_write_', '_update_', '_default_',
            'show_', 'process_',
            'execute', 'compile',
            '_info',  # Info methods (e.g., session_info, user_info)
        ]
    
    def visit_Assign(self, node):
        """Detect Odoo field assignments"""
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Attribute):
                if isinstance(node.value.func.value, ast.Name):
                    if node.value.func.value.id == 'fields':
                        # This is an Odoo field assignment
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                self.field_names.add(target.id)
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        """Collect all function/method names"""
        # Check if this method matches Odoo patterns that should be preserved
        should_preserve = False
        for pattern in self.odoo_method_patterns:
            if pattern in node.name:
                should_preserve = True
                break
        
        self.method_names[node.name] = should_preserve
        self.generic_visit(node)

class EnhancedObfuscator(ast.NodeTransformer):
    """Enhanced AST-based obfuscator with advanced complexity"""

    def __init__(self, odoo_field_names=None, collected_methods=None, preserve_public_api=True):
        self.var_count = 0
        self.func_count = 0
        self.class_count = 0
        self.var_map = {}
        self.func_map = {}
        self.class_map = {}
        self.strings = []
        self.preserve_public_api = preserve_public_api
        self.module_level_depth = 0
        self.public_names = set()
        self.in_public_class = False
        self.in_controller_class = False
        self.in_fstring = False
        self.in_class_body = False
        self.collected_methods = collected_methods or {}
        
        # Odoo-specific reserved attributes that must not be obfuscated
        self.odoo_reserved = {
            # Model definition attributes
            '_name', '_description', '_inherit', '_inherits', '_rec_name',
            '_order', '_sql_constraints', '_constraints', '_auto', '_table',
            '_table_query', '_sequence', '_parent_name', '_parent_store',
            '_date_name', '_fold_name', '_abstract', '_transient', '_log_access',
            '_check_company_auto',
            # Model lifecycle methods
            '_register_hook', '_setup_complete', '_constraint_methods',
            # Field-related attributes
            '_columns', '_defaults', '_rec_name', '_order',
            # Technical attributes
            'env', 'id', 'ids', '_context', '_cr', '_uid',
            # Common methods that shouldn't be obfuscated
            'create', 'write', 'unlink', 'search', 'browse', 'read',
            'search_read', 'name_get', 'name_search', 'name_create',
            'default_get', 'fields_get', 'fields_view_get',
            # API decorators - these are method names typically
            'api', 'models', 'fields', 'tools', '_',
            # Python compatibility shims (often exported from compat modules)
            'string_types', 'text_type', 'binary_type', 'integer_types',
            'iteritems', 'iterkeys', 'itervalues', 'PY2', 'PY3',
        }
        
        # Odoo method name patterns that must be preserved
        self.odoo_method_patterns = [
            '_compute_', '_inverse_', '_search_', '_onchange_',
            '_depends_', '_constraint_', '_sql_constraint_',
            'action_', 'button_',
            'get_', '_get_', 'set_', '_set_',
            '_check_', '_prepare_',
            '_create_', '_write_', '_update_', '_default_',
            'show_', 'process_',
            'execute', 'compile',
            '_info',
        ]
        
        # Odoo field names collected from first pass
        self.odoo_field_names = odoo_field_names or set()
        
        # Pre-populate func_map with methods that will be obfuscated
        for method_name, should_preserve in self.collected_methods.items():
            if not should_preserve:
                should_really_preserve = False
                
                # Check if method name matches any preservation pattern
                for pattern in self.odoo_method_patterns:
                    if pattern in method_name:
                        should_really_preserve = True
                        break
                
                # Check if it's in odoo_reserved
                if method_name in self.odoo_reserved:
                    should_really_preserve = True
                
                # Only add to func_map if it should truly be obfuscated
                if not should_really_preserve:
                    self.func_map[method_name] = self.generate_confusing_func_name()

    def generate_confusing_var_name(self):
        """Generate highly confusing variable names"""
        patterns = [
            lambda n: f'O0O0O{n}O0O',  # Mix of O and 0
            lambda n: f'l1l1l{n}l1l',  # Mix of l and 1
            lambda n: f'__{n}__',      # Double underscore
            lambda n: f'I1I1I{n}I1I',  # Mix of I and 1
            lambda n: f'_x{n}_y{n}_z{n}',  # Multi-part names
            lambda n: f'var_{hex(n)[2:]}_{hex(n*7)[2:]}',  # Hex-based
        ]
        pattern = random.choice(patterns)
        name = pattern(self.var_count)
        self.var_count += 1
        return name

    def generate_confusing_func_name(self):
        """Generate highly confusing function names"""
        patterns = [
            lambda n: f'func_O0O{n}O0O',
            lambda n: f'method_l1l{n}l1l',
            lambda n: f'__{hex(n)[2:]}_{hex(n*3)[2:]}__',
            lambda n: f'fn_I1I{n}I1I',
            lambda n: f'_exec_{n}_{n*2}',
            lambda n: f'handler_{chr(65+n%26)}{n}',
        ]
        pattern = random.choice(patterns)
        name = pattern(self.func_count)
        self.func_count += 1
        return name

    def generate_class_name(self):
        """Generate obfuscated class name"""
        name = f'_cls_{self.class_count}'
        self.class_count += 1
        return name

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
        """Add junk code to function definitions and obfuscate names"""
        # Add junk code randomly
        if len(node.body) > 0 and random.random() < 0.3:  # 30% chance
            junk_code = self.add_control_flow_obfuscation(node)
            node.body.insert(0, junk_code)
        
        # Obfuscate function name if not preserved
        if node.name not in ['__init__', '__str__', '__repr__', 'main']:
            should_preserve = False
            
            # Check if it's in odoo_reserved
            if node.name in self.odoo_reserved:
                should_preserve = True
            
            # Check if method name matches any preservation pattern
            for pattern in self.odoo_method_patterns:
                if pattern in node.name:
                    should_preserve = True
                    break
            
            if not should_preserve:
                if node.name not in self.func_map:
                    self.func_map[node.name] = self.generate_confusing_func_name()
                node.name = self.func_map[node.name]
        
        # Continue with normal processing
        self.generic_visit(node)
        return node

    def visit_Name(self, node):
        """Obfuscate variable names with enhanced patterns"""
        # NEVER obfuscate 'self' and 'cls'
        if node.id in ('self', 'cls'):
            return node
        
        # Check var_map FIRST before checking odoo_field_names
        if node.id in self.var_map:
            pass  # Continue to the Store/Load logic below
        elif node.id in self.odoo_field_names:
            return node
        
        # Skip ALL UPPERCASE constants
        if node.id.isupper():
            return node
        
        # Preserve common module-level variables
        common_module_vars = ['_logger', '_log', 'logger', 'log']
        module_state_suffixes = ['_cache', '_registry', '_map', '_dict', '_list', '_set', '_parsers', '_handlers']
        is_module_state_var = any(node.id.endswith(suffix) for suffix in module_state_suffixes)
        
        if self.module_level_depth == 0 and node.id not in self.var_map:
            if node.id in common_module_vars or is_module_state_var:
                return node
        
        # For Store context (variable assignment)
        if isinstance(node.ctx, ast.Store):
            if self.in_class_body and node.id in self.odoo_reserved:
                return node
            if self.module_level_depth == 0:
                if node.id.isupper() or node.id in common_module_vars or is_module_state_var:
                    return node
            if node.id not in self.var_map:
                self.var_map[node.id] = self.generate_confusing_var_name()
            node.id = self.var_map[node.id]
        elif isinstance(node.ctx, ast.Load):
            if node.id in self.var_map:
                node.id = self.var_map[node.id]
            elif node.id in self.func_map:
                node.id = self.func_map[node.id]
            elif node.id in self.class_map:
                node.id = self.class_map[node.id]
            elif node.id.isupper() or (node.id in common_module_vars and self.module_level_depth == 0):
                return node
            elif node.id in self.odoo_reserved:
                return node
        return node

    def visit_Constant(self, node):
        """Enhanced string encryption with multiple layers"""
        if isinstance(node.value, str) and len(node.value) > 3:
            # Skip code-like strings and f-string components
            code_keywords = ['import', 'def ', 'class ', 'if ', 'for ', 'while ', 'try ', 'with ', 'from ', 'lambda ', 'return ', 'yield ', 'raise ', 'break', 'continue', 'pass', 'assert ', 'global ', 'nonlocal ', 'except ', 'finally ', 'elif ', 'else:', ' and ', ' or ', ' not ', ' is ', ' in ', 'True', 'False', 'None']
            special_chars = ['\n', '\t', '\r', '(', ')', '[', ']', '{', '}', '=', '+', '-', '*', '/', '//', '%', '==', '!=', '<', '>', '<=', '>=', '+=', '-=', '*=', '/=', '//=', '%=', '&', '|', '^', '~', '<<', '>>', '->', ':', ';', ',', '.']
            
            special_char_count = sum((1 for char in special_chars if char in node.value))
            has_code_keywords = any((keyword in node.value for keyword in code_keywords))
            has_many_special_chars = special_char_count > 5
            has_newlines = '\n' in node.value or '\r' in node.value or '\t' in node.value
            is_very_long = len(node.value) > 200
            
            if has_code_keywords or has_many_special_chars or has_newlines or is_very_long:
                return node
            
            # Multi-layer encryption
            string_index = len(self.strings)
            
            # Layer 1: XOR with index-based key
            xor_key = (string_index % 256) ^ 0x42
            xor_encrypted = ''.join(chr(ord(c) ^ xor_key) for c in node.value)
            
            # Layer 2: Base64 encoding
            base64_encrypted = base64.b64encode(xor_encrypted.encode()).decode()
            
            # Layer 3: Add obfuscation markers
            encrypted_string = f'__ENCRYPTED__{base64_encrypted}__ENCRYPTED__'
            self.strings.append(encrypted_string)
            
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
                func=ast.Name(id='_decrypt_str', ctx=ast.Load()), 
                args=[dummy_calc], 
                keywords=[]
            )
        return node

    def visit_JoinedStr(self, node):
        """Handle f-strings - don't encrypt them as they cause issues"""
        # Just visit children without modifying the f-string structure
        self.generic_visit(node)
        return node

def create_enhanced_runtime_code(strings_list, license_key=None):
    """Create enhanced runtime code with anti-tampering features"""
    strings_repr = repr(strings_list)
    
    license_code = ""
    if license_key:
        license_code = f'''
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

_STRINGS = {strings_repr}

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

{license_code}
'''
    
    return runtime_code

def obfuscate_file_single(input_file, output_file, machine_id=None, license_key=None, preserve_api=True):
    """Obfuscate a single file with enhanced pre-computed license info"""
    try:
        # Read source
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_source = f.read()

        # Check if this file is already obfuscated
        is_already_obfuscated = (
            '_decrypt_str(' in raw_source or
            '_STRINGS = [' in raw_source or
            '_check_license' in raw_source
        )

        if is_already_obfuscated:
            # File is already obfuscated, just copy it as-is
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(raw_source)
            return True

        # Strip existing runtime code to allow re-obfuscation
        source = strip_existing_runtime_code(raw_source)

        # Check if this is a manifest file (Odoo loads these with ast.literal_eval)
        input_path = Path(input_file)
        is_manifest = input_path.name == '__manifest__.py' or input_path.name == '__openerp__.py'

        # For manifest files, skip obfuscation entirely as Odoo uses ast.literal_eval to load them
        if is_manifest:
            # Copy manifest files as-is without obfuscation
            output_code = source
        else:
            # Parse AST
            tree = ast.parse(source, filename=input_file)

            # First pass: collect Odoo field names and method names
            collector = NameCollector()
            collector.visit(tree)

            # Apply enhanced obfuscation
            obfuscator = EnhancedObfuscator(
                odoo_field_names=collector.field_names,
                collected_methods=collector.method_names,
                preserve_public_api=preserve_api
            )
            obfuscated_tree = obfuscator.visit(tree)
            ast.fix_missing_locations(obfuscated_tree)

            # Generate obfuscated code
            obfuscated_code = ast.unparse(obfuscated_tree)

            # Create enhanced runtime code
            runtime_code = create_enhanced_runtime_code(obfuscator.strings, license_key)

            # Combine runtime and obfuscated code
            output_code = runtime_code + "\n" + obfuscated_code

        # Write output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_code)

        return True

    except Exception as e:
        print(f"❌ Error obfuscating {input_file}: {e}")
        return False

def strip_existing_runtime_code(source: str):
    """Remove existing obfuscation runtime code to allow re-obfuscation"""
    lines = source.splitlines()
    result_lines = []
    skip_mode = False
    
    # Markers that indicate runtime code we should skip
    runtime_markers = [
        'Override ast.literal_eval IMMEDIATELY',
        '_safe_literal_eval',
        '_original_literal_eval',
        '_STRINGS = []',
        '_STRINGS = [',
        'def _decrypt_str(',
        '_LICENSE_KEY =',
        'def _get_machine_id(',
        'def _check_license(',
        '_check_license()',
    ]
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Check if this line starts runtime code
        is_runtime = any(marker in line for marker in runtime_markers)
        
        if is_runtime:
            # Skip this line and look for the end of the runtime block
            if stripped.startswith('_check_license()'):
                # This is the call to _check_license, skip it and continue
                i += 1
                continue
            elif stripped.startswith('def _') or stripped.startswith('_LICENSE_KEY') or stripped.startswith('_STRINGS'):
                # Start of a runtime function or variable, skip the entire definition
                skip_mode = True
                i += 1
                continue
            elif '# Override ast.literal_eval' in line or '_original_literal_eval' in line:
                # Start of runtime setup code
                skip_mode = True
                i += 1
                continue
        
        if skip_mode:
            # We're skipping runtime code
            # Stop skipping when we see a non-indented, non-empty line that looks like app code
            if stripped and not line.startswith(' ') and not line.startswith('\t'):
                # Check if this looks like application code
                if not any(marker in line for marker in runtime_markers):
                    # This is application code, stop skipping
                    skip_mode = False
                    result_lines.append(line)
            # Otherwise keep skipping
            i += 1
            continue
        
        # Normal line, keep it
        result_lines.append(line)
        i += 1
    
    return '\n'.join(result_lines)

def obfuscate_file(input_file, output_file, bind_machine=False, expiration_days=365, preserve_api=True, project_url=None):
    """Enhanced obfuscate a single Python file with optional machine binding"""
    output_path = Path(output_file)

    # Generate license if machine binding is requested
    license_key = None
    machine_id = None
    if bind_machine:
        machine_id = get_machine_id()
        license_key, expiration = generate_license_key(machine_id, expiration_days)
        
        print(f"🔒 Generating machine binding license...")
        if project_url:
            print(f"🔗 Project URL: {project_url}")

    # Check if this is a manifest file (Odoo loads these with ast.literal_eval)
    input_path = Path(input_file)
    is_manifest = input_path.name == '__manifest__.py' or input_path.name == '__openerp__.py'

    # Read source
    with open(input_file, 'r', encoding='utf-8') as f:
        source = f.read()

    # For manifest files, skip obfuscation entirely as Odoo uses ast.literal_eval to load them
    if is_manifest:
        # Copy manifest files as-is without obfuscation
        output_code = source
    else:
        # Parse AST
        tree = ast.parse(source, filename=input_file)

        # First pass: collect Odoo field names and method names
        collector = NameCollector()
        collector.visit(tree)

        # Apply enhanced obfuscation
        obfuscator = EnhancedObfuscator(
            odoo_field_names=collector.field_names,
            collected_methods=collector.method_names,
            preserve_public_api=preserve_api
        )
        obfuscated_tree = obfuscator.visit(tree)
        ast.fix_missing_locations(obfuscated_tree)

        # Generate obfuscated code
        obfuscated_code = ast.unparse(obfuscated_tree)

        # Create enhanced runtime code
        runtime_code = create_enhanced_runtime_code(obfuscator.strings, license_key)

        # Combine runtime and obfuscated code
        output_code = runtime_code + "\n" + obfuscated_code

        print(f"✅ Enhanced obfuscation complete!")
        print(f"   Variables obfuscated: {obfuscator.var_count}")
        print(f"   Functions obfuscated: {obfuscator.func_count}")
        print(f"   Strings encrypted: {len(obfuscator.strings)}")

    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save license info if machine binding is enabled
    if bind_machine and license_key:
        license_file = output_file + '.license'
        with open(license_file, 'w', encoding='utf-8') as f:
            f.write(f"Machine ID: {machine_id}\n")
            f.write(f"License Key: {license_key}\n")
            f.write(f"Expires: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expiration))}\n")
            f.write(f"Protected: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            if project_url:
                f.write(f"Project URL: {project_url}\n")

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_code)

    return True

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PyProtect Enhanced - Advanced Python Obfuscator with Machine ID Binding")
    parser.add_argument("-i", "--input",
                       help="Input Python file or directory (not needed with -m)")
    parser.add_argument("-o", "--output", default=str(get_default_output_path()),
                       help="Output obfuscated file or directory (default: PyProtect/dist/filename or PyProtect/dist/inputname/)")
    parser.add_argument("-d", "--deploy", action="store_true",
                       help="Deploy mode: backup original and replace in-place (ignores -o)")
    parser.add_argument("-r", "--restore",
                       help="Restore from backup: specify backup path (e.g., module.backup_20251209_125530)")
    parser.add_argument("-u", "--url",
                       help="Project URL to embed in license file (e.g., https://github.com/user/repo)")
    parser.add_argument("-m", "--machine-id", action="store_true",
                       help="Display current machine ID and exit")
    parser.add_argument("-c", "--check-license", nargs='?', const=".",
                       help="Check license validity in directory (default: current dir)")
    parser.add_argument("-b", "--bind-machine", action="store_true",
                       help="Bind obfuscated code to current machine")
    parser.add_argument("-e", "--expiration", type=int, default=365,
                       help="License expiration in days (default: 365)")
    parser.add_argument("--no-preserve-api", action="store_true",
                       help="Obfuscate all names including public API (may break imports)")

    args = parser.parse_args()

    # Handle restore mode
    if args.restore:
        success = restore_from_backup(args.restore)
        sys.exit(0 if success else 1)

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
        print("Run 'python pyprotect.py --help' for usage information")
        sys.exit(1)

    input_path = Path(args.input)

    if not input_path.exists():
        print(f"❌ Input path not found: {args.input}")
        sys.exit(1)

    # Enhanced obfuscation with better feedback
    print("🚀 PyProtect Enhanced - Advanced Python Obfuscator")
    print("="*60)
    print("Enhanced Features:")
    print("  + Multi-layer String Encryption (XOR + Base64)")
    print("  + Confusing Variable Name Obfuscation")
    print("  + Control Flow Obfuscation with Junk Code")
    print("  + Anti-Debugging Protection")
    print("  + Code Integrity Verification")
    print("  + Dummy Functions & Dead Code Injection")
    print("="*60)

    if input_path.is_file():
        if args.deploy:
            # Deploy mode: backup and replace original
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_path = input_path.parent / f"{input_path.stem}.backup_{timestamp}{input_path.suffix}"
            
            print(f"🚀 Deploy mode: Will backup and replace original")
            print(f"📦 Backup will be created at: {backup_path.name}")
            print(f"🎯 Protected code will replace: {input_path.name}")
            print()
            
            # Create temporary output
            temp_output = input_path.parent / f"{input_path.stem}_temp{input_path.suffix}"
            
            success = obfuscate_file(
                str(input_path), 
                str(temp_output),
                bind_machine=args.bind_machine,
                expiration_days=args.expiration,
                preserve_api=not args.no_preserve_api,
                project_url=args.url
            )
            
            if success:
                print("\n" + "="*60)
                print("🚀 Deploy Mode: Ready to backup and replace")
                print("="*60)
                print(f"📄 Original file: {input_path.name}")
                print(f"📦 Backup will be: {backup_path.name}")
                print(f"✨ Protected file at: {temp_output}")
                print()
                
                response = input("⚠️  Proceed with backup and replacement? (y/n): ").strip().lower()
                
                if response in ['y', 'yes']:
                    print("\n🔄 Deploying...")
                    
                    # Check if backup already exists
                    if backup_path.exists():
                        print(f"⚠️  Backup path already exists: {backup_path.name}")
                        print("   Removing existing backup...")
                        backup_path.unlink()
                        print("   ✅ Removed existing backup")
                    
                    # Create backup
                    shutil.copy2(str(input_path), str(backup_path))
                    print(f"✅ Original backed up to: {backup_path.name}")
                    
                    # Replace original with obfuscated version
                    shutil.move(str(temp_output), str(input_path))
                    print(f"✅ Protected version deployed to: {input_path.name}")
                    
                    print(f"\n💡 To restore: mv {backup_path.name} {input_path.name}")
                else:
                    print("\n🛑 Deploy cancelled by user")
                    # Clean up temp file
                    if temp_output.exists():
                        temp_output.unlink()
            else:
                print("❌ Obfuscation failed, deploy cancelled")
                if temp_output.exists():
                    temp_output.unlink()
        else:
            # Normal mode: output to specified location
            if args.output == str(get_default_output_path()):
                output_path = get_default_output_path() / input_path.name
            else:
                output_path = Path(args.output)
            
            print("📄 Single file obfuscation mode")
            print("="*50)
            if not args.no_preserve_api:
                print("🔓 Public API preservation: ENABLED (Odoo/Framework compatible)")
            else:
                print("🔒 Public API preservation: DISABLED (Full obfuscation)")
            print()
            
            success = obfuscate_file(
                str(input_path), 
                str(output_path),
                bind_machine=args.bind_machine,
                expiration_days=args.expiration,
                preserve_api=not args.no_preserve_api,
                project_url=args.url
            )
            
            if success:
                print(f"\n✅ File obfuscation complete: {output_path}")
            else:
                print(f"\n❌ File obfuscation failed")
                sys.exit(1)
    else:
        # Directory processing
        if args.output == str(get_default_output_path()):
            output_path = get_default_output_path() / input_path.name
        else:
            output_path = Path(args.output)
        
        print("📁 Directory obfuscation mode")
        print("="*50)
        if not args.no_preserve_api:
            print("🔓 Public API preservation: ENABLED (Odoo/Framework compatible)")
        else:
            print("🔒 Public API preservation: DISABLED (Full obfuscation)")
        print()
        
        # Create backup of entire directory
        create_backup(output_path)
        
        # Process all Python files
        python_files = []
        other_files = []
        
        for file_path in input_path.rglob('*'):
            if file_path.is_file():
                if file_path.suffix == '.py' and '__pycache__' not in str(file_path):
                    python_files.append(file_path)
                else:
                    other_files.append(file_path)
        
        print(f"   📝 Python files: {len(python_files)}")
        print(f"   📄 Other files: {len(other_files)}")
        print()
        
        # Generate license once for the entire project
        license_key = None
        machine_id = None
        if args.bind_machine:
            machine_id = get_machine_id()
            license_key, expiration = generate_license_key(machine_id, args.expiration)
        
        # Process Python files
        success_count = 0
        for py_file in python_files:
            relative_path = py_file.relative_to(input_path)
            output_file = output_path / relative_path
            
            # Create output directory
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            print(f"Obfuscating {relative_path}...", end=" ")
            
            success = obfuscate_file_single(
                str(py_file),
                str(output_file),
                machine_id=machine_id,
                license_key=license_key,
                preserve_api=not args.no_preserve_api
            )
            
            if success:
                print("✅")
                success_count += 1
            else:
                print("❌")
        
        # Copy other files
        for other_file in other_files:
            relative_path = other_file.relative_to(input_path)
            output_file = output_path / relative_path
            
            # Create output directory
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                shutil.copy2(str(other_file), str(output_file))
            except Exception as e:
                print(f"⚠️  Warning: Could not copy {relative_path}: {e}")
        
        # Save project license if machine binding is enabled
        if args.bind_machine and license_key:
            license_file = output_path / "project.license"
            with open(license_file, 'w', encoding='utf-8') as f:
                f.write(f"Machine ID: {machine_id}\n")
                f.write(f"License Key: {license_key}\n")
                f.write(f"Expires: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expiration))}\n")
                f.write(f"Protected: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                if args.url:
                    f.write(f"Project URL: {args.url}\n")
        
        print(f"\n✅ Directory obfuscation complete!")
        print(f"   Successfully processed: {success_count}/{len(python_files)} Python files")
        print(f"   Output directory: {output_path}")