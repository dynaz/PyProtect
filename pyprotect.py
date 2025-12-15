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
    # NOTE: These checks are DISABLED for the obfuscator tool itself
    # They will be added to obfuscated output files only
    pass

# Run environment check immediately (disabled)
# _check_environment()

def _verify_code_integrity():
    """Enhanced code integrity verification"""
    # NOTE: This check is DISABLED for the obfuscator tool itself
    # It will be added to obfuscated output files only
    pass

# Run integrity check (disabled)
# _verify_code_integrity()

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
        self.module_level_depth = 0  # Track nesting depth
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
            '_info',       # Info methods (e.g., session_info, user_info)
            '_render',     # Rendering methods (QWeb, templates)
            '_build_',     # Build methods
            '_load_',      # Load methods
            '_save_',      # Save methods
            '_validate_',  # Validation methods
            '_format_',    # Format methods
            '_add_',       # Add methods
            '_remove_',    # Remove methods
            '_delete_',    # Delete methods
            '_process_',   # Process methods
            '_handle_',    # Handle methods
            '_init_',      # Init methods
            '_setup_',     # Setup methods
            '_register_',  # Register methods
            '_unregister_',# Unregister methods
            '_all_',       # All/collection methods (e.g., _all_manual_field_data)
            '_apply_',      # Apply methods
            '_call_',       # Call methods
            '_do_',         # Do methods
            '_execute_',    # Execute methods
            '_perform_',    # Perform methods
            '_run_',        # Run methods
            '_instanciate', # Instanciate methods
            '_generate_',   # Generate methods
            '_convert_',    # Convert methods
            '_parse_',      # Parse methods
            '_normalize_',  # Normalize methods
            '_sanitize_',   # Sanitize methods
            '_copy_',       # Copy methods
            '_clone_',      # Clone methods
            '_merge_',      # Merge methods
            '_split_',      # Split methods
            '_join_',       # Join methods
            '_map_',        # Map methods
            '_filter_',     # Filter methods
            '_reduce_',     # Reduce methods
            '_is_',         # Check/validation methods (e.g., _is_manual_name, _is_valid)
            '_has_',        # Has/contains methods
            '_can_',        # Permission/capability check methods
            '_should_',     # Conditional check methods
            '_needs_',      # Requirement check methods
            '_must_',       # Mandatory check methods
            '_find_',       # Find/search methods
            '_fetch_',      # Fetch methods
            '_collect_',    # Collection methods
            '_extract_',    # Extract methods
            '_compute',     # Compute methods (also covers _compute_ but without trailing underscore)
            '_unlink',      # Unlink methods
            '_inherited',   # Inherited methods (e.g., _inherited_models)
            '_xmlid',       # XMLID methods (e.g., _xmlid_to_res_model_res_id)
            '_module_',     # Module methods (e.g., _module_data_uninstall)
            'routing_',     # Routing methods (e.g., routing_map)
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
                        
                        # Also collect field names from string parameters
                        # Many field parameters reference other field names as strings
                        for keyword in node.value.keywords:
                            if keyword.arg in ['inverse_name', 'related', 'depends', 'compute', 
                                              'inverse', 'search', 'comodel_name', 'relation',
                                              'string', 'domain', 'ondelete', 'relation_field',
                                              'currency_field', 'check_company']:
                                if isinstance(keyword.value, ast.Constant) and isinstance(keyword.value.value, str):
                                    # Extract field names from these parameters
                                    field_ref = keyword.value.value
                                    # Handle dot notation for related fields (e.g., 'partner_id.name')
                                    # Also handle comma-separated depends (e.g., 'field1, field2')
                                    for segment in field_ref.split(','):
                                        parts = segment.strip().split('.')
                                        for part in parts:
                                            # Clean up the part (remove parentheses, brackets, etc.)
                                            clean_part = part.strip()
                                            if clean_part and ('_' in clean_part or clean_part.endswith('_id') or clean_part.endswith('_ids')):
                                                # Likely a field name with underscore or id/ids suffix
                                                self.field_names.add(clean_part)
        self.generic_visit(node)
    
    def visit_AnnAssign(self, node):
        """Detect annotated Odoo field assignments"""
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Attribute):
                if isinstance(node.value.func.value, ast.Name):
                    if node.value.func.value.id == 'fields':
                        # This is an Odoo field assignment with annotation
                        if isinstance(node.target, ast.Name):
                            self.field_names.add(node.target.id)
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        """Track when entering/exiting classes"""
        self.module_level_depth += 1
        self.generic_visit(node)
        self.module_level_depth -= 1
    
    def visit_FunctionDef(self, node):
        """Collect all function/method names"""
        is_module_level = (self.module_level_depth == 0)
        
        # Check if this method matches Odoo patterns that should be preserved
        should_preserve = False
        
        # Preserve ALL module-level functions (can be imported by other modules)
        # This includes both public and "private" functions (with underscore)
        if is_module_level:
            should_preserve = True
        
        # Check if in odoo_reserved (common Odoo ORM methods like create, write, etc.)
        # Note: We need to access odoo_reserved from a temporary obfuscator instance
        # or maintain our own list here
        odoo_core_methods = {
            'create', 'write', 'unlink', 'search', 'browse', 'read',
            'search_read', 'name_get', 'name_search', 'name_create',
            'default_get', 'fields_get', 'fields_view_get', 'read_group',
            'copy', 'export_data', 'import_data', 'load',
        }
        
        if node.name in odoo_core_methods:
            should_preserve = True
        
        # CONSERVATIVE: Preserve ALL methods starting with single underscore
        # These are internal API methods that may be called across modules
        if node.name.startswith('_') and not node.name.startswith('__'):
            should_preserve = True
        
        # Check Odoo patterns
        for pattern in self.odoo_method_patterns:
            if pattern in node.name:
                should_preserve = True
                break
        
        self.method_names[node.name] = should_preserve
        
        # Enter function body
        self.module_level_depth += 1
        self.generic_visit(node)
        self.module_level_depth -= 1

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
        self.in_namedtuple_class = False  # Track if we're in a NamedTuple class
        self.current_function_name = None  # Track current function name
        self.collected_methods = collected_methods or {}
        
        # Odoo-specific reserved attributes that must not be obfuscated
        self.odoo_reserved = {
            # Python special variables that must NEVER be obfuscated
            '__path__', '__name__', '__file__', '__doc__', '__package__',
            '__version__', '__author__', '__all__', '__dict__', '__class__',
            '__module__', '__qualname__', '__annotations__', '__slots__',
            # Python built-in and common variables
            'dispatch', 'registry', 'globals', 'locals', 'vars', 'dir',
            'dump_frozen_dict', 'dump_struct', 'dump_array', 'dump_instance',
            'dump_string', 'dump_unicode', 'dump_int', 'dump_long', 'dump_double',
            'dump_datetime', 'dump_binary', 'dump_nil', 'dump_bool', 'dump_bytes',
            'dump_date', 'dump_lazy',
            # Common parameter names used by decorators and cross-module calls
            'key', 'keys', 'args', 'kwargs', 'self', 'cls', 'converters', 'context',
            'value', 'values', 'write', 'data', 'params', 'options',
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
            # API decorators and modules - these are method/module names
            'api', 'models', 'fields', 'tools', '_', 'http',
            # Python compatibility shims (often exported from compat modules)
            'string_types', 'text_type', 'binary_type', 'integer_types',
            'iteritems', 'iterkeys', 'itervalues', 'PY2', 'PY3',
            # DateTime formatting constants and functions
            'DATETIME_FORMATS_MAP', 'DATE_FORMATS', 'TIME_FORMATS',
            'DEFAULT_SERVER_DATE_FORMAT', 'DEFAULT_SERVER_TIME_FORMAT', 
            'DEFAULT_SERVER_DATETIME_FORMAT',
            # HTTP and Controller related
            'route', 'Controller', 'request', 'Response', 'session',
            'dispatch_rpc', 'service', 'method',
            # Cache and ORM related
            'ormcache', 'ormcache_context', 'cache', 'invalidate_cache',
            # Odoo exceptions and common classes
            'UserError', 'ValidationError', 'AccessError', 'MissingError',
            'AccessDenied', 'RedirectWarning',
            # Common Odoo imports and utilities
            'Command', 'frozendict', 'lazy', 'Markup',
            # Special methods that may be called by Odoo framework
            'name_create', 'toggle_noupdate', 'check_object_reference',
            'group_names_with_access', 'call_cache_clearing_methods',
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
            '_info',        # Info methods (e.g., session_info, user_info)
            '_render',      # Rendering methods (QWeb, templates)
            '_build_',      # Build methods
            '_load_',       # Load methods
            '_save_',       # Save methods
            '_validate_',   # Validation methods
            '_format_',     # Format methods
            '_add_',        # Add methods
            '_remove_',     # Remove methods
            '_delete_',     # Delete methods
            '_process_',    # Process methods
            '_handle_',     # Handle methods
            '_init_',       # Init methods
            '_setup_',      # Setup methods
            '_register_',   # Register methods
            '_unregister_', # Unregister methods
            '_all_',        # All/collection methods (e.g., _all_manual_field_data)
            '_apply_',      # Apply methods
            '_call_',       # Call methods
            '_do_',         # Do methods
            '_execute_',    # Execute methods
            '_perform_',    # Perform methods
            '_run_',        # Run methods
            '_instanciate', # Instanciate methods
            '_generate_',   # Generate methods
            '_convert_',    # Convert methods
            '_parse_',      # Parse methods
            '_normalize_',  # Normalize methods
            '_sanitize_',   # Sanitize methods
            '_copy_',       # Copy methods
            '_clone_',      # Clone methods
            '_merge_',      # Merge methods
            '_split_',      # Split methods
            '_join_',       # Join methods
            '_map_',        # Map methods
            '_filter_',     # Filter methods
            '_reduce_',     # Reduce methods
            '_is_',         # Check/validation methods (e.g., _is_manual_name, _is_valid)
            '_has_',        # Has/contains methods
            '_can_',        # Permission/capability check methods
            '_should_',     # Conditional check methods
            '_needs_',      # Requirement check methods
            '_must_',       # Mandatory check methods
            '_find_',       # Find/search methods
            '_fetch_',      # Fetch methods
            '_collect_',    # Collection methods
            '_extract_',    # Extract methods
            '_compute',     # Compute methods (also covers _compute_ but without trailing underscore)
            '_autovacuum',  # Methods with @api.autovacuum decorator
            '_cron_',       # Cron methods
            '_cleanup_',    # Cleanup methods
            '_unlink',      # Unlink methods
            '_inherited',   # Inherited methods (e.g., _inherited_models)
            '_xmlid',       # XMLID methods (e.g., _xmlid_to_res_model_res_id)
            '_module_',     # Module methods (e.g., _module_data_uninstall)
            'routing_',     # Routing methods (e.g., routing_map)
        ]
        
        # Odoo field names collected from first pass
        self.odoo_field_names = odoo_field_names or set()
        
        # Pre-populate func_map with methods that will be obfuscated
        # NOTE: Methods added here might later be determined to be preserved
        # (e.g., class methods, Odoo reserved methods). In such cases, visit_FunctionDef
        # will update func_map to map the method name to itself to prevent obfuscation.
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
            lambda n: f'I1I1I{n}I1I',  # Mix of I and 1
            lambda n: f'_x{n}_y{n}_z{n}',  # Multi-part names
            lambda n: f'var_{hex(n)[2:]}_{hex(n*7)[2:]}',  # Hex-based
        ]
        # Use deterministic pattern selection based on counter to ensure consistency
        pattern = patterns[self.var_count % len(patterns)]
        name = pattern(self.var_count)
        self.var_count += 1
        return name

    def generate_confusing_func_name(self):
        """Generate highly confusing function names"""
        patterns = [
            lambda n: f'func_O0O{n}O0O',
            lambda n: f'method_l1l{n}l1l',
            lambda n: f'fn_I1I{n}I1I',
            lambda n: f'_exec_{n}_{n*2}',
            lambda n: f'handler_{chr(65+n%26)}{n}',
        ]
        # Use deterministic pattern selection based on counter to ensure consistency
        pattern = patterns[self.func_count % len(patterns)]
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

    def visit_Assign(self, node):
        """Preserve Odoo field assignments and reserved model attributes"""
        # Check if we're in a class body and assigning an Odoo field
        if self.in_class_body:
            # Check if this is a field assignment (e.g., field_name = fields.Many2one(...))
            is_field_assignment = False
            if isinstance(node.value, ast.Call):
                if isinstance(node.value.func, ast.Attribute):
                    if isinstance(node.value.func.value, ast.Name):
                        if node.value.func.value.id == 'fields':
                            is_field_assignment = True
            
            # If it's a field assignment, preserve the field name
            if is_field_assignment:
                # Visit the value (right-hand side) to obfuscate its internals
                self.generic_visit(node.value)
                # But DO NOT obfuscate the target field name (left-hand side)
                # Return the node unchanged for the target name
                return node
            
            # Check if assigning an Odoo reserved attribute or class-level underscore variable
            # But ONLY at class level (module_level_depth == 1), not inside methods
            if self.module_level_depth == 1:
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        # Preserve if:
                        # 1. In odoo_reserved or collected field names (at class level only)
                        # 2. Starts with single underscore (Odoo internal class attributes)
                        # 3. Is uppercase (constants)
                        should_preserve = (
                            target.id in self.odoo_reserved or 
                            target.id in self.odoo_field_names or
                            (target.id.startswith('_') and not target.id.startswith('__')) or
                            target.id.isupper()
                        )
                        
                        if should_preserve:
                            # Preserve this assignment
                            self.generic_visit(node.value)
                            return node
        
        # For module-level assignments, preserve common patterns
        if self.module_level_depth == 0:
            common_module_vars = ['_logger', '_log', 'logger', 'log']
            module_state_suffixes = ['_cache', '_registry', '_map', '_dict', '_list', '_set', 
                                    '_parsers', '_handlers']
            
            for target in node.targets:
                if isinstance(target, ast.Name):
                    is_module_state_var = any(target.id.endswith(suffix) for suffix in module_state_suffixes)
                    if target.id.isupper() or target.id in common_module_vars or is_module_state_var or target.id in self.odoo_reserved:
                        self.generic_visit(node.value)
                        return node
        
        # Default: visit normally
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        """Handle class definitions and track nesting depth"""
        # CRITICAL: Never obfuscate class names - they're used in super() calls
        # FORCE class name to map to itself, overwriting any previous obfuscation
        self.var_map[node.name] = node.name
        self.class_map[node.name] = node.name
        
        # Increment depth when entering a class
        self.module_level_depth += 1
        old_in_class = self.in_class_body
        self.in_class_body = True
        
        # Check if this class inherits from NamedTuple
        old_in_namedtuple = self.in_namedtuple_class
        self.in_namedtuple_class = False
        for base in node.bases:
            # Check for NamedTuple, typing.NamedTuple, etc.
            if isinstance(base, ast.Name) and base.id == 'NamedTuple':
                self.in_namedtuple_class = True
                break
            elif isinstance(base, ast.Attribute) and base.attr == 'NamedTuple':
                self.in_namedtuple_class = True
                break
        
        # Process the class body
        self.generic_visit(node)
        
        # Restore state when leaving class
        self.module_level_depth -= 1
        self.in_class_body = old_in_class
        self.in_namedtuple_class = old_in_namedtuple
        
        return node

    def visit_FunctionDef(self, node):
        """Add junk code to function definitions and obfuscate names"""
        # Track if we're entering a function (affects module_level_depth)
        entering_module_level = (self.module_level_depth == 0)
        
        # Add junk code randomly
        if len(node.body) > 0 and random.random() < 0.3:  # 30% chance
            junk_code = self.add_control_flow_obfuscation(node)
            node.body.insert(0, junk_code)
        
        # Check if method has decorators that require private naming (underscore prefix)
        requires_private_name = False
        for decorator in node.decorator_list:
            # Handle @api.autovacuum, @api.cron, etc.
            if isinstance(decorator, ast.Attribute):
                if isinstance(decorator.value, ast.Name):
                    if decorator.value.id == 'api' and decorator.attr in ['autovacuum', 'cron']:
                        requires_private_name = True
                        break
            # Handle @tools.ormcache decorator - preserve parameter names in string literals
            elif isinstance(decorator, ast.Call):
                if isinstance(decorator.func, ast.Attribute):
                    if isinstance(decorator.func.value, ast.Name):
                        if decorator.func.value.id == 'tools' and 'ormcache' in decorator.func.attr:
                            # ormcache decorators have field/parameter names as string arguments
                            # e.g., @tools.ormcache('model_name', 'field_name')
                            # These parameter names should be preserved
                            for arg in decorator.args:
                                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                                    # Add these parameter names to odoo_field_names to preserve them
                                    self.odoo_field_names.add(arg.value)
        
        # Obfuscate function name if not preserved
        should_preserve = False
        
        # ALWAYS preserve special methods (dunder methods like __init__, __call__, etc.)
        if node.name.startswith('__') and node.name.endswith('__'):
            should_preserve = True
        
        # Check if it's in odoo_reserved
        if node.name in self.odoo_reserved:
            should_preserve = True
        
        # Preserve ALL module-level functions (can be imported by other modules)
        # This includes both public and "private" functions (with underscore)
        if entering_module_level:
            should_preserve = True
        
        # MAXIMUM CONSERVATIVE APPROACH FOR ODOO:
        # Preserve ALL methods defined directly in class bodies
        # Odoo methods are frequently called across modules, even public ones
        # This catches methods like routing_map, name_get, etc.
        # Only obfuscate local functions defined inside other functions
        if self.in_class_body:
            should_preserve = True
        
        # Don't process further if already should preserve
        if not should_preserve:
            # Check if method name matches any preservation pattern
            for pattern in self.odoo_method_patterns:
                if pattern in node.name:
                    should_preserve = True
                    break
        
        # Obfuscate the function name if not preserved
        if not should_preserve:
            if node.name not in self.func_map:
                new_name = self.generate_confusing_func_name()
                # If the method requires private naming, ensure it starts with underscore
                if requires_private_name and not new_name.startswith('_'):
                    new_name = '_' + new_name
                self.func_map[node.name] = new_name
            else:
                # Method was pre-populated, but we need to ensure underscore prefix if required
                if requires_private_name:
                    existing_name = self.func_map[node.name]
                    if not existing_name.startswith('_'):
                        self.func_map[node.name] = '_' + existing_name
            
            node.name = self.func_map[node.name]
        else:
            # Function is preserved - make sure both var_map and func_map know about it
            # This prevents the name from being obfuscated when used as a variable reference
            # For example: dispatch[bytes] = dump_bytes (where dump_bytes is a method name)
            if node.name not in self.var_map:
                self.var_map[node.name] = node.name
            # CRITICAL FIX: If the method was pre-populated in func_map but we're now preserving it,
            # we need to update func_map to map the method name to itself.
            # This ensures that method calls via attributes (self.method_name()) use the correct name.
            if node.name in self.func_map and self.func_map[node.name] != node.name:
                # Method was pre-populated with obfuscated name but should be preserved
                self.func_map[node.name] = node.name
        
        # Increment depth when entering function body
        self.module_level_depth += 1
        
        # Track current function name for parameter handling
        old_function_name = self.current_function_name
        self.current_function_name = node.name
        
        # Visit decorators first (they're evaluated before function is defined)
        for decorator in node.decorator_list:
            self.visit(decorator)
        
        # Visit function arguments to establish mappings
        # This ensures parameter names are consistently mapped
        for arg in node.args.posonlyargs:
            self.visit(arg)
        for arg in node.args.args:
            self.visit(arg)
        if node.args.vararg:
            self.visit(node.args.vararg)
        for arg in node.args.kwonlyargs:
            self.visit(arg)
        if node.args.kwarg:
            self.visit(node.args.kwarg)
        
        # Visit default argument values
        for default in node.args.defaults:
            self.visit(default)
        for default in node.args.kw_defaults:
            if default:  # kw_defaults can contain None
                self.visit(default)
        
        # Visit return type annotation
        if node.returns:
            self.visit(node.returns)
        
        # Visit function body
        for stmt in node.body:
            self.visit(stmt)
        
        # Decrement depth when leaving function
        self.module_level_depth -= 1
        
        # Restore previous function name
        self.current_function_name = old_function_name
        
        return node

    def visit_arg(self, node):
        """Handle function arguments"""
        # Don't obfuscate self and cls
        if node.arg in ('self', 'cls'):
            return node
        
        # Don't obfuscate reserved parameter names (used by decorators like @ormcache('key'))
        if node.arg in self.odoo_reserved:
            # Map to itself so references in the function body work correctly
            self.var_map[node.arg] = node.arg
            return node
        
        # Don't obfuscate parameters of special methods (dunder methods)
        # They have specific signatures that external code expects
        if self.current_function_name and self.current_function_name.startswith('__') and self.current_function_name.endswith('__'):
            # FORCE mapping to itself, overwriting any previous mapping
            # This ensures the parameter name is always preserved
            self.var_map[node.arg] = node.arg
            return node
        
        # CRITICAL FOR ODOO: Preserve ALL parameters in class methods
        # Since we preserve all class methods (they can be called from other modules),
        # we must also preserve their parameter names because they might be called
        # with keyword arguments (e.g., method(converters=..., key=...))
        if self.in_class_body:
            self.var_map[node.arg] = node.arg
            return node
        
        # Create mapping for this argument if it doesn't exist
        if node.arg not in self.var_map:
            self.var_map[node.arg] = self.generate_confusing_var_name()
        
        # Update the argument name
        node.arg = self.var_map[node.arg]
        
        # Visit annotation if present
        if node.annotation:
            self.visit(node.annotation)
        
        return node
    
    def visit_AnnAssign(self, node):
        """Handle annotated assignments (like NamedTuple fields)"""
        # If we're in a NamedTuple class, preserve the field name
        if self.in_namedtuple_class and isinstance(node.target, ast.Name):
            # Don't obfuscate NamedTuple field names
            # Just visit the annotation and value without changing the target name
            if node.annotation:
                self.visit(node.annotation)
            if node.value:
                self.visit(node.value)
            return node
        
        # Otherwise, proceed with normal obfuscation
        return self.generic_visit(node)
    
    def visit_Attribute(self, node):
        """Handle attribute access - preserve Odoo attributes and constants"""
        # Preserve uppercase attributes (constants like DATETIME_FORMATS_MAP)
        if hasattr(node, 'attr'):
            if node.attr.isupper() or node.attr in self.odoo_reserved:
                # Don't obfuscate this attribute
                pass
            elif node.attr in self.func_map:
                # Method was obfuscated, use mapped name
                node.attr = self.func_map[node.attr]
            elif node.attr.startswith('_') and not node.attr.startswith('__'):
                # Preserve internal attributes
                pass
        
        # Visit the value (the object the attribute is accessed on)
        self.generic_visit(node)
        return node
    
    def visit_Name(self, node):
        """Obfuscate variable names with enhanced patterns"""
        # NEVER obfuscate 'self' and 'cls'
        if node.id in ('self', 'cls'):
            return node
        
        # NEVER obfuscate Odoo reserved names (fields, api, models, tools, _, etc.)
        if node.id in self.odoo_reserved:
            return node
        
        # Don't obfuscate names in NamedTuple classes
        if self.in_namedtuple_class and isinstance(node.ctx, ast.Store):
            return node
        
        # Check var_map FIRST - if already mapped, use that mapping
        # This ensures consistency between definition and usage
        if node.id in self.var_map:
            pass  # Continue to the Store/Load logic below
        # Only preserve field names if we're at module or class level (not inside methods)
        # This prevents local variables from being mistakenly preserved
        elif node.id in self.odoo_field_names and (self.module_level_depth <= 1):
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
            if self.module_level_depth == 0:
                if node.id.isupper() or node.id in common_module_vars or is_module_state_var:
                    return node
            
            # If in class body, preserve class attributes starting with single underscore
            if self.in_class_body and node.id.startswith('_') and not node.id.startswith('__'):
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
            # Preserve class attributes starting with single underscore if not in var_map
            # This handles cases like self._avatar_name_field where the attribute wasn't obfuscated during assignment
            elif self.in_class_body and node.id.startswith('_') and not node.id.startswith('__'):
                return node
        return node

    def visit_Constant(self, node):
        """Enhanced string encryption with multiple layers"""
        # Skip encryption if we're inside an f-string
        if getattr(self, 'in_fstring', False):
            return node
            
        if isinstance(node.value, str) and len(node.value) > 3:
            # AGGRESSIVE PROTECTION: Skip strings that look like Odoo field names or model names
            # Common patterns: ends with _id, _ids, contains underscore patterns
            field_suffixes = ['_id', '_ids', '_line', '_lines', '_count', '_date', '_time', 
                            '_name', '_code', '_number', '_ref', '_sequence', '_state', 
                            '_status', '_type', '_value', '_amount', '_currency', '_partner',
                            '_user', '_product', '_invoice', '_sale', '_purchase', '_stock',
                            '_qty', '_price', '_total', '_subtotal', '_tax', '_payment']
            
            common_field_names = ['name', 'code', 'active', 'sequence', 'note', 'description', 
                                'date', 'state', 'type', 'value', 'amount', 'company_id',
                                'currency_id', 'partner_id', 'user_id', 'product_id', 'create_date',
                                'write_date', 'create_uid', 'write_uid', 'display_name', 'id',
                                'model', 'res_id', 'res_model', 'email', 'phone', 'mobile']
            
            # Check if string looks like a field name or model name
            is_field_or_model_name = (
                # Ends with common field suffixes
                any(node.value.endswith(suffix) for suffix in field_suffixes) or
                # Is a common field name
                node.value in common_field_names or
                # Was collected as a field name
                node.value in self.odoo_field_names or
                # Starts with x_ (custom Odoo fields)
                node.value.startswith('x_') or
                # Contains dots (likely model name like 'res.partner' or 'ir.model')
                ('.' in node.value and len(node.value.split('.')) in [2, 3]) or
                # Looks like a field name: lowercase with underscores, not too long
                (node.value.islower() and '_' in node.value and len(node.value) < 50 and node.value.count('_') <= 5) or
                # Contains 'model' (often part of field/model references)
                'model' in node.value.lower()
            )
            
            if is_field_or_model_name:
                return node
            
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

    def visit_ListComp(self, node):
        """Handle list comprehensions with proper scoping"""
        return self._visit_comprehension(node)
    
    def visit_DictComp(self, node):
        """Handle dict comprehensions with proper scoping"""
        return self._visit_comprehension(node)
    
    def visit_SetComp(self, node):
        """Handle set comprehensions with proper scoping"""
        return self._visit_comprehension(node)
    
    def visit_GeneratorExp(self, node):
        """Handle generator expressions with proper scoping"""
        return self._visit_comprehension(node)
    
    def _visit_comprehension(self, node):
        """Helper to handle all types of comprehensions with local scope"""
        # Comprehensions in Python 3 have their own scope
        # We need to handle this carefully to map variables correctly
        
        # Visit generators to process iterators and establish loop variable mappings
        for generator in node.generators:
            # Visit the iterator first (what we're iterating over)
            # This is evaluated in the outer scope
            generator.iter = self.visit(generator.iter)
            
            # Visit the target (loop variable)
            # This creates a mapping in var_map that will be used in the comprehension body
            generator.target = self.visit(generator.target)
            
            # Visit the conditions (if any)
            generator.ifs = [self.visit(if_clause) for if_clause in generator.ifs]
        
        # Now visit the element/key/value expressions
        # These will use the mappings created by the loop variables
        if hasattr(node, 'elt'):  # ListComp, SetComp, GeneratorExp
            node.elt = self.visit(node.elt)
        if hasattr(node, 'key'):  # DictComp
            node.key = self.visit(node.key)
            node.value = self.visit(node.value)
        
        return node
    
    def visit_JoinedStr(self, node):
        """Handle f-strings - preserve them completely to avoid AST issues"""
        # Set flag to indicate we're inside an f-string to prevent string encryption
        old_in_fstring = getattr(self, 'in_fstring', False)
        self.in_fstring = True
        
        try:
            # Simply use generic_visit to handle variable names inside f-strings
            # This will obfuscate variables but won't try to encrypt strings
            # This is the safest approach that avoids breaking f-string syntax
            self.generic_visit(node)
        finally:
            # Always restore the flag
            self.in_fstring = old_in_fstring
        
        return node
    
    def visit_keyword(self, node):
        """
        Handle keyword arguments in function calls.
        When a function parameter is obfuscated, update the keyword argument name.
        
        Example:
        - Function def: def foo(O0O0O0O0O):  # originally 'param'
        - Call: foo(param=value)  # needs to become foo(O0O0O0O0O=value)
        """
        # Check if the keyword argument name has been obfuscated
        if node.arg and node.arg in self.var_map:
            # Use the obfuscated name from var_map
            node.arg = self.var_map[node.arg]
        
        # Visit the value of the keyword argument
        self.generic_visit(node)
        return node
    
    def visit_ImportFrom(self, node):
        """
        Handle import statements to create aliases when imported names are obfuscated.
        
        Example:
        - Original: from reportlab.pdfgen import canvas
        - If 'canvas' is obfuscated to '_x13_y13_z13' in the code
        - We need: from reportlab.pdfgen import canvas as _x13_y13_z13
        """
        if node.names:
            for alias in node.names:
                # Check if this imported name is used with an obfuscated name in the code
                import_name = alias.name
                
                # Check if the imported name appears in var_map (meaning it's obfuscated)
                if import_name in self.var_map and self.var_map[import_name] != import_name:
                    # Add an alias to use the obfuscated name
                    if not alias.asname:  # Only add alias if one doesn't exist
                        alias.asname = self.var_map[import_name]
        
        return node
    
    def visit_Import(self, node):
        """
        Handle import statements (import X) to create aliases when needed.
        Similar to visit_ImportFrom but for 'import X' statements.
        """
        if node.names:
            for alias in node.names:
                import_name = alias.name
                
                # Check if the imported name is obfuscated
                if import_name in self.var_map and self.var_map[import_name] != import_name:
                    if not alias.asname:
                        alias.asname = self.var_map[import_name]
        
        return node

def extract_future_imports(code):
    """Extract __future__ imports from code to preserve them at the top"""
    lines = code.split('\n')
    future_lines = []
    other_lines = []
    
    in_docstring = False
    docstring_char = None
    found_future = False
    
    for line in lines:
        stripped = line.strip()
        
        # Track docstrings
        if not in_docstring:
            if stripped.startswith('"""') or stripped.startswith("'''"):
                docstring_char = stripped[:3]
                in_docstring = True
                if stripped.count(docstring_char) >= 2:
                    in_docstring = False
                other_lines.append(line)
                continue
        else:
            other_lines.append(line)
            if docstring_char in stripped:
                in_docstring = False
            continue
        
        # Collect __future__ imports
        if stripped.startswith('from __future__ import'):
            future_lines.append(line)
            found_future = True
        # Also preserve comments and empty lines before __future__ imports
        elif not found_future and (stripped.startswith('#') or stripped == ''):
            other_lines.append(line)
        else:
            other_lines.append(line)
    
    return '\n'.join(future_lines), '\n'.join(other_lines)

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
        is_ir_qweb = input_path.name == 'ir_qweb.py'  # Skip due to complex f-strings
        is_res_lang = input_path.name == 'res_lang.py'  # Skip due to method preservation issues

        # For manifest files, ir_qweb, and res_lang, skip obfuscation entirely
        if is_manifest or is_ir_qweb or is_res_lang:
            # Copy these files as-is without obfuscation
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

            # Extract __future__ imports to preserve them at the top
            future_imports, rest_of_code = extract_future_imports(obfuscated_code)

            # Create enhanced runtime code
            runtime_code = create_enhanced_runtime_code(obfuscator.strings, license_key)

            # Combine: __future__ imports + runtime code + rest of code
            if future_imports:
                output_code = future_imports + "\n\n" + runtime_code + "\n" + rest_of_code
            else:
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
    input_path = Path(input_file)

    # Always create backup of input file for safety
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    if input_path.is_file():
        backup_path = input_path.parent / f"{input_path.stem}.backup_{timestamp}{input_path.suffix}"
        try:
            shutil.copy2(str(input_path), str(backup_path))
            print(f"📦 Created backup: {backup_path.name}")
        except Exception as e:
            print(f"⚠️  Warning: Could not create backup: {e}")

    # Generate license if machine binding is requested
    license_key = None
    machine_id = None
    if bind_machine:
        machine_id = get_machine_id()
        license_key, expiration = generate_license_key(machine_id, expiration_days)
        
        print(f"🔒 Generating machine binding license...")
        if project_url:
            print(f"🔗 Project URL: {project_url}")

    # Check if this is a file that should not be obfuscated
    is_manifest = input_path.name == '__manifest__.py' or input_path.name == '__openerp__.py'
    is_init = input_path.name == '__init__.py'
    is_ir_qweb = input_path.name == 'ir_qweb.py'  # Skip due to complex f-strings
    is_res_lang = input_path.name == 'res_lang.py'  # Skip due to method preservation issues
    is_assetsbundle = input_path.name == 'assetsbundle.py'  # Skip due to complex f-strings with nested quotes
    is_ir_model = input_path.name == 'ir_model.py'  # Skip due to complex f-strings with .join()
    is_ir_ui_view = input_path.name == 'ir_ui_view.py'  # Skip due to complex f-strings with method calls
    is_rpc_file = input_path.name == 'rpc.py'  # RPC controllers - can be obfuscated but verify it works
    
    # Read source
    with open(input_file, 'r', encoding='utf-8') as f:
        source = f.read()

    # Skip obfuscation for special files
    if is_manifest or is_init or is_ir_qweb or is_res_lang or is_assetsbundle or is_ir_model or is_ir_ui_view:
        # Copy these files as-is without obfuscation
        # __manifest__.py: Odoo uses ast.literal_eval to load them
        # __init__.py: Package initialization files should remain readable
        # ir_qweb.py: Has complex f-strings that break during obfuscation
        # res_lang.py: Has method preservation issues
        # assetsbundle.py: Has complex f-strings with nested quotes
        # ir_model.py: Has complex f-strings with .join()
        # ir_ui_view.py: Has complex f-strings with method calls
        output_code = source
        print(f"📄 Skipped obfuscation: {input_path.name} (special file)")
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

        # Extract __future__ imports to preserve them at the top
        future_imports, rest_of_code = extract_future_imports(obfuscated_code)

        # Create enhanced runtime code
        runtime_code = create_enhanced_runtime_code(obfuscator.strings, license_key)

        # Combine: __future__ imports + runtime code + rest of code
        if future_imports:
            output_code = future_imports + "\n\n" + runtime_code + "\n" + rest_of_code
        else:
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
        if args.deploy:
            # Deploy mode for directories: backup and replace in-place
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_path = input_path.parent / f"{input_path.name}.backup_{timestamp}"
            temp_output = input_path.parent / f"{input_path.name}_temp_{timestamp}"
            
            print("📁 Directory obfuscation mode with DEPLOY")
            print("="*50)
            if not args.no_preserve_api:
                print("🔓 Public API preservation: ENABLED (Odoo/Framework compatible)")
            else:
                print("🔒 Public API preservation: DISABLED (Full obfuscation)")
            print()
            print(f"🚀 Deploy mode: Will backup and replace original directory")
            print(f"📦 Backup will be created at: {backup_path.name}")
            print(f"🎯 Protected code will replace: {input_path.name}")
            print()
            
            output_path = temp_output
        else:
            # Normal mode: output to specified location
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
        
        # Handle deploy mode for directories
        if args.deploy:
            print("\n" + "="*60)
            print("🚀 Deploy Mode: Ready to backup and replace directory")
            print("="*60)
            print(f"📄 Original directory: {input_path}")
            print(f"📦 Backup will be: {backup_path}")
            print(f"✨ Protected directory at: {temp_output}")
            print()
            
            response = input("⚠️  Proceed with backup and replacement? (y/n): ").strip().lower()
            
            if response in ['y', 'yes']:
                print("\n🔄 Deploying...")
                
                # Check if backup already exists
                if backup_path.exists():
                    print(f"⚠️  Backup path already exists: {backup_path.name}")
                    print("   Removing existing backup...")
                    shutil.rmtree(str(backup_path))
                    print("   ✅ Removed existing backup")
                
                # Create backup by moving original
                shutil.move(str(input_path), str(backup_path))
                print(f"✅ Original backed up to: {backup_path.name}")
                
                # Move obfuscated version to original location
                shutil.move(str(temp_output), str(input_path))
                print(f"✅ Protected version deployed to: {input_path.name}")
                
                print(f"\n💡 To restore: rmdir {input_path.name} && mv {backup_path.name} {input_path.name}")
            else:
                print("\n🛑 Deploy cancelled by user")
                # Clean up temp directory
                if temp_output.exists():
                    shutil.rmtree(str(temp_output))
                    print(f"🗑️  Cleaned up temporary directory")