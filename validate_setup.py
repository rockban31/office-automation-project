#!/usr/bin/env python3
"""
Project setup validation script.

This script validates that the project structure is correct
without requiring external dependencies.
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and print status."""
    exists = Path(filepath).exists()
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {filepath}")
    return exists

def check_directory_exists(dirpath, description):
    """Check if a directory exists and print status."""
    exists = Path(dirpath).is_dir()
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {dirpath}")
    return exists

def main():
    """Main validation function."""
    print("=== Office Automation Project Validation ===")
    print()
    
    all_good = True
    
    # Check required files
    print("Checking required files:")
    files_to_check = [
        ("README.md", "Project documentation"),
        ("requirements.txt", "Python dependencies"),
        ("setup.py", "Setup script"),
        (".env", "Environment configuration"),
        (".env.example", "Environment template"),
        (".gitignore", "Git ignore rules"),
        ("LICENSE", "License file"),
    ]
    
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_good = False
    
    print()
    
    # Check directory structure
    print("Checking directory structure:")
    directories_to_check = [
        ("src", "Source code"),
        ("src/auth", "Authentication module"),
        ("src/config", "Configuration module"),
        ("src/monitoring", "Monitoring module"),
        ("src/troubleshooting", "Troubleshooting module"),
        ("src/alerts", "Alerts module"),
        ("src/dashboard", "Dashboard module"),
        ("tests", "Test files"),
        ("examples", "Example scripts"),
        ("logs", "Log files"),
        ("data", "Data files"),
        ("docs", "Documentation"),
        ("config", "Configuration files"),
    ]
    
    for dirpath, description in directories_to_check:
        if not check_directory_exists(dirpath, description):
            all_good = False
    
    print()
    
    # Check key Python files
    print("Checking key Python files:")
    python_files_to_check = [
        ("src/__init__.py", "Main package init"),
        ("src/auth/__init__.py", "Auth package init"),
        ("src/auth/mist_auth.py", "Mist authentication"),
        ("src/config/__init__.py", "Config package init"),
        ("src/config/auth_config.py", "Auth configuration"),
        ("tests/test_auth.py", "Authentication tests"),
        ("examples/auth_example.py", "Auth example script"),
    ]
    
    for filepath, description in python_files_to_check:
        if not check_file_exists(filepath, description):
            all_good = False
    
    print()
    
    # Check Python version
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("✗ Python 3.8+ required")
        all_good = False
    else:
        print("✓ Python version is compatible")
    
    print()
    
    # Final status
    if all_good:
        print("🎉 Project structure validation PASSED!")
        print()
        print("Next steps:")
        print("1. Update .env file with your Mist API credentials")
        print("2. Run: python setup.py (to create virtual environment and install dependencies)")
        print("3. Activate virtual environment: venv\\Scripts\\activate (Windows) or source venv/bin/activate (Linux/Mac)")
        print("4. Test: python examples/auth_example.py")
    else:
        print("❌ Project structure validation FAILED!")
        print("Some required files or directories are missing.")
        print("Run the setup script to fix issues: python setup.py")
    
    return all_good

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
