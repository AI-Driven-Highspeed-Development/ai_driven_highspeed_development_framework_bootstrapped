#!/usr/bin/env python3
"""
Install Requirements - Automatically finds and installs all requirements.txt files in the project

This script searches for all requirements.txt files in the project directory and its subdirectories,
then installs the packages listed in each file using pip.
"""

import subprocess
import sys
import os
from pathlib import Path


def find_and_install_requirements():
    """
    Find all requirements.txt files and install packages from them.
    Equivalent to: find . -name "requirements.txt" -type f -exec pip install -r '{}' ';'
    """
    print("🔍 Searching for requirements.txt files...")
    
    # Find all requirements.txt files
    requirements_files = []
    current_dir = Path(".")
    
    for req_file in current_dir.rglob("requirements.txt"):
        if req_file.is_file():
            requirements_files.append(req_file)
    
    if not requirements_files:
        print("⚠️  No requirements.txt files found in the project")
        return True
    
    print(f"📋 Found {len(requirements_files)} requirements.txt files:")
    for req_file in requirements_files:
        print(f"   • {req_file}")
    
    print("\n📦 Installing packages from all requirements files...")
    
    success_count = 0
    failed_files = []
    
    for req_file in requirements_files:
        print(f"\n🔄 Processing {req_file}...")
        
        try:
            # Install requirements from this file
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(req_file)],
                capture_output=True,
                text=True,
                check=True
            )
            
            print(f"✅ Successfully installed packages from {req_file}")
            if result.stdout.strip():
                # Show a summary instead of full output
                lines = result.stdout.strip().split('\n')
                installed_lines = [line for line in lines if 'Successfully installed' in line]
                if installed_lines:
                    print(f"   {installed_lines[-1]}")
            
            success_count += 1
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install packages from {req_file}")
            if e.stderr:
                print(f"   Error: {e.stderr.strip()}")
            failed_files.append(req_file)
        
        except Exception as e:
            print(f"❌ Unexpected error processing {req_file}: {e}")
            failed_files.append(req_file)
    
    # Summary
    print(f"\n📊 Installation Summary:")
    print(f"✅ Successfully processed: {success_count}/{len(requirements_files)} files")
    
    if failed_files:
        print(f"❌ Failed files:")
        for failed_file in failed_files:
            print(f"   • {failed_file}")
        return False
    else:
        print("🎉 All requirements files processed successfully!")
        return True


def main():
    """Main function for standalone execution."""
    print("🚀 ADHD Framework - Requirements Installer")
    print("=" * 50)
    
    try:
        success = find_and_install_requirements()
        if success:
            print("\n✅ Requirements installation completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Some requirements failed to install. Check the output above.")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n⚠️  Installation cancelled by user")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()