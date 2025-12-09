#!/usr/bin/env python3
"""
PyProtect CLI Entry Point
Command-line interface for PyProtect obfuscation tool
"""

import sys
from pathlib import Path
from .main import (
    get_machine_id,
    check_license_status,
    obfuscate_file,
    obfuscate_directory,
    get_default_output_path,
)


def main():
    """Main CLI entry point"""
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
    parser.add_argument("-b", "--bind-machine", action="store_true",
                       help="Bind obfuscated code to current machine")
    parser.add_argument("-e", "--expiration", type=int, default=365,
                       help="License expiration in days (default: 365)")
    parser.add_argument("--no-preserve-api", action="store_true",
                       help="Obfuscate all names including public API (may break imports)")
    parser.add_argument("-r", "--redirect", metavar="URL",
                       help="Enable Odoo redirect handling (preserves redirect-related fields and parameters)")

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
        print("Run 'pyprotect --help' for usage information")
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
        # Determine if we should preserve public API (default: True, unless --no-preserve-api)
        preserve_api = not args.no_preserve_api
        
        if input_path.is_dir():
            # Directory mode
            print("🏗️  Directory obfuscation mode")
            print("="*50)
            if preserve_api:
                print("🔓 Public API preservation: ENABLED (Odoo/Framework compatible)")
            else:
                print("🔒 Public API preservation: DISABLED (Full obfuscation)")
            print()
            success = obfuscate_directory(
                str(input_path), str(output_path),
                bind_machine=args.bind_machine,
                expiration_days=args.expiration,
                preserve_api=preserve_api
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
            if preserve_api:
                print("🔓 Public API preservation: ENABLED (Odoo/Framework compatible)")
            else:
                print("🔒 Public API preservation: DISABLED (Full obfuscation)")
            print()
            obfuscate_file(str(input_path), str(output_path),
                          bind_machine=args.bind_machine,
                          expiration_days=args.expiration,
                          preserve_api=preserve_api)
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


if __name__ == "__main__":
    main()

