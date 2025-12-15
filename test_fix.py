#!/usr/bin/env python3
"""
Test script to verify the PyProtect fix for method call/definition mismatches
"""

import tempfile
import os
from pathlib import Path

# Test case: A simple class with methods that should be preserved
TEST_CODE = '''
class TestClass:
    def __init__(self):
        self.value = 0
    
    def hash_md5(self):
        """This method should be preserved (class method)"""
        return "hash"
    
    def check_jasper_file(self):
        """This method should be preserved (class method)"""
        return "checked"
    
    def write_file_to_field(self, path):
        """This method should be preserved (class method)"""
        return f"written: {path}"
    
    def clean_up_temp(self, tmpdir):
        """This method should be preserved (class method)"""
        return f"cleaned: {tmpdir}"
    
    def active(self):
        """This method should be preserved (class method)"""
        hash_obj = self.hash_md5()
        return hash_obj
    
    def reset_password(self):
        """This method should be preserved (class method)"""
        return self.active()
    
    def show_report(self, report_name=False):
        """This method should be preserved (class method)"""
        self.check_jasper_file()
        try:
            tmpdir = "/tmp/test"
            tmpf = "/tmp/test/file"
            self.write_file_to_field(tmpf)
        finally:
            self.clean_up_temp(tmpdir)
        return "report shown"

class JasperPy:
    def __init__(self):
        self._command = ""
    
    @property
    def command(self):
        """Property that should be preserved"""
        return self._command
    
    def execute(self, run_as_user=False):
        """This method should be preserved"""
        if run_as_user:
            self._command = "su -u " + run_as_user + " -c \\"" + self.command + "\\""
        return self.command
'''

def test_obfuscation():
    """Test that the obfuscation preserves method names correctly"""
    print("🧪 Testing PyProtect fix for method call/definition mismatches...")
    print()
    
    # Create temporary directory for test
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test_input.py"
        output_file = Path(tmpdir) / "test_output.py"
        
        # Write test code
        with open(test_file, 'w') as f:
            f.write(TEST_CODE)
        
        print(f"📝 Created test file: {test_file}")
        
        # Run pyprotect
        import subprocess
        script_dir = Path(__file__).parent
        pyprotect_script = script_dir / "pyprotect.py"
        
        cmd = [
            "python3",
            str(pyprotect_script),
            "-i", str(test_file),
            "-o", str(output_file)
        ]
        
        print(f"🔧 Running PyProtect...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ PyProtect failed:")
            print(result.stderr)
            return False
        
        print(f"✅ PyProtect completed successfully")
        print()
        
        # Read obfuscated code
        with open(output_file, 'r') as f:
            obfuscated_code = f.read()
        
        # Check for issues
        issues = []
        
        # Check 1: Method definitions should be preserved (class methods)
        if 'def hash_md5' not in obfuscated_code:
            issues.append("❌ Method 'hash_md5' was obfuscated (should be preserved)")
        else:
            print("✅ Method 'hash_md5' preserved")
        
        if 'def check_jasper_file' not in obfuscated_code:
            issues.append("❌ Method 'check_jasper_file' was obfuscated (should be preserved)")
        else:
            print("✅ Method 'check_jasper_file' preserved")
        
        if 'def write_file_to_field' not in obfuscated_code:
            issues.append("❌ Method 'write_file_to_field' was obfuscated (should be preserved)")
        else:
            print("✅ Method 'write_file_to_field' preserved")
        
        if 'def clean_up_temp' not in obfuscated_code:
            issues.append("❌ Method 'clean_up_temp' was obfuscated (should be preserved)")
        else:
            print("✅ Method 'clean_up_temp' preserved")
        
        if 'def active' not in obfuscated_code:
            issues.append("❌ Method 'active' was obfuscated (should be preserved)")
        else:
            print("✅ Method 'active' preserved")
        
        if 'def reset_password' not in obfuscated_code:
            issues.append("❌ Method 'reset_password' was obfuscated (should be preserved)")
        else:
            print("✅ Method 'reset_password' preserved")
        
        if 'def show_report' not in obfuscated_code:
            issues.append("❌ Method 'show_report' was obfuscated (should be preserved)")
        else:
            print("✅ Method 'show_report' preserved")
        
        if 'def execute' not in obfuscated_code:
            issues.append("❌ Method 'execute' was obfuscated (should be preserved)")
        else:
            print("✅ Method 'execute' preserved")
        
        print()
        
        # Check 2: Method calls should match definitions
        import re
        
        # Find obfuscated method calls (like self.fn_I1I2I1I())
        obf_calls = re.findall(r'self\.(fn_|handler_|_exec_|func_|method_)[A-Za-z0-9_]+\(', obfuscated_code)
        if obf_calls:
            issues.append(f"❌ Found obfuscated method calls that don't match definitions: {set(obf_calls)}")
            print(f"❌ Found {len(obf_calls)} obfuscated method calls:")
            for call in set(obf_calls):
                print(f"   • {call}")
        else:
            print("✅ No mismatched obfuscated method calls found")
        
        print()
        
        # Check 3: Verify the code can be executed
        print("🔍 Attempting to execute obfuscated code...")
        try:
            exec_globals = {}
            exec(obfuscated_code, exec_globals)
            
            # Try to instantiate and use the classes
            TestClass = exec_globals['TestClass']
            obj = TestClass()
            
            # Test method calls
            result1 = obj.hash_md5()
            assert result1 == "hash", f"hash_md5() returned {result1}, expected 'hash'"
            print("   ✅ hash_md5() works")
            
            result2 = obj.active()
            assert result2 == "hash", f"active() returned {result2}, expected 'hash'"
            print("   ✅ active() works")
            
            result3 = obj.reset_password()
            assert result3 == "hash", f"reset_password() returned {result3}, expected 'hash'"
            print("   ✅ reset_password() works")
            
            result4 = obj.show_report()
            assert result4 == "report shown", f"show_report() returned {result4}, expected 'report shown'"
            print("   ✅ show_report() works")
            
            JasperPy = exec_globals['JasperPy']
            jasper = JasperPy()
            result5 = jasper.execute()
            assert result5 == "", f"execute() returned {result5}, expected ''"
            print("   ✅ execute() works")
            
            print()
            print("✅ All execution tests passed!")
            
        except Exception as e:
            issues.append(f"❌ Execution failed: {e}")
            print(f"   ❌ Execution failed: {e}")
            import traceback
            traceback.print_exc()
        
        print()
        print("=" * 60)
        
        if issues:
            print("❌ TEST FAILED")
            print()
            print("Issues found:")
            for issue in issues:
                print(f"  {issue}")
            return False
        else:
            print("✅ TEST PASSED - All checks successful!")
            return True

if __name__ == "__main__":
    success = test_obfuscation()
    exit(0 if success else 1)

