#!/usr/bin/env python3
"""
PyProtect Enhanced CLI Entry Point
Command-line interface for PyProtect Enhanced obfuscation tool with advanced features
"""

import sys
import time
from pathlib import Path
from .main import (
    get_machine_id,
    check_license_status,
    obfuscate_file,
    obfuscate_directory,
    get_default_output_path,
    restore_from_backup,
)


def main():
    """Enhanced CLI entry point with all advanced features"""
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
        print("Run 'pyprotect --help' for usage information")
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
            import shutil
            
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
                    
                    print(f"\n💡 To restore: pyprotect -r {backup_path.name}")
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
        
        success = obfuscate_directory(
            str(input_path),
            str(output_path),
            bind_machine=args.bind_machine,
            expiration_days=args.expiration,
            preserve_api=not args.no_preserve_api,
            project_url=args.url
        )
        
        if success:
            print(f"\n✅ Directory obfuscation complete: {output_path}")
        else:
            print(f"\n❌ Directory obfuscation failed")
            sys.exit(1)


if __name__ == "__main__":
    main()