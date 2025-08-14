#!/usr/bin/env python3
"""
Setup script for Office Automation Project.

This script helps initialize the development environment and install dependencies.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, check=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(command, shell=True, check=check, 
                              capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error output: {e.stderr}")
        return None

def create_virtual_environment():
    """Create a Python virtual environment."""
    print("Creating virtual environment...")
    
    venv_path = Path("venv")
    if venv_path.exists():
        print("Virtual environment already exists.")
        return True
    
    # Wrap sys.executable in quotes to handle spaces in path
    result = run_command(f'"{sys.executable}" -m venv venv')
    if result is None:
        print("Failed to create virtual environment.")
        return False
    
    print("Virtual environment created successfully.")
    return True

def get_pip_command():
    """Get the appropriate pip command for the current platform."""
    if platform.system() == "Windows":
        return "venv\\Scripts\\pip.exe"
    else:
        return "venv/bin/pip"

def install_dependencies():
    """Install Python dependencies."""
    print("Installing dependencies...")
    
    pip_cmd = get_pip_command()
    
    # Upgrade pip first
    result = run_command(f"{pip_cmd} install --upgrade pip")
    if result is None:
        print("Failed to upgrade pip.")
        return False

    # Detect if a proxy is needed from environment variables
    proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
    proxy_arg = f'--proxy={proxy} ' if proxy else ''

    # Remove hardcoded proxy and cert options, use only if needed
    pip_install_cmd = (
        f'{pip_cmd} install -r requirements.txt '
        f'{proxy_arg}'
        '--trusted-host pypi.org '
        '--trusted-host files.pythonhosted.org '
        '--trusted-host pypi.python.org '
        '--disable-pip-version-check '
        '--no-cache-dir '
        '--timeout 100'
    )

    result = run_command(pip_install_cmd)
    if result is None:
        print("Failed to install dependencies.")
        if proxy:
            print("Check your proxy settings or network connection.")
        else:
            print("If you are behind a proxy, set the HTTP_PROXY/HTTPS_PROXY environment variable and try again.")
        return False

    print("Dependencies installed successfully.")
    return True

def create_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        "data",
        "logs", 
        "docs",
        "src/monitoring",
        "src/troubleshooting", 
        "src/alerts",
        "src/dashboard"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("All directories created.")

def check_env_file():
    """Check if .env file exists and create from template if not."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        print("Creating .env file from template...")
        with open(env_example) as src, open(env_file, 'w') as dst:
            dst.write(src.read())
        print("Created .env file. Please update it with your actual configuration.")
    elif env_file.exists():
        print(".env file already exists.")
    else:
        print("Warning: Neither .env nor .env.example files found.")

def run_tests():
    """Run basic tests to verify setup."""
    print("Running tests...")
    
    # Check if we can import the main module
    try:
        sys.path.insert(0, "src")
        from auth import MistAuth
        print("✓ Main modules can be imported successfully.")
    except ImportError as e:
        print(f"✗ Failed to import modules: {e}")
        return False
    
    # Run pytest if available
    pip_cmd = get_pip_command()
    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python.exe"
    else:
        python_cmd = "venv/bin/python"
    
    result = run_command(f"{python_cmd} -m pytest tests/ -v", check=False)
    if result and result.returncode == 0:
        print("✓ All tests passed.")
    else:
        print("Some tests failed or pytest not available.")
    
    return True

def main():
    """Main setup function."""
    print("=== Office Automation Project Setup ===")
    print()
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        sys.exit(1)
    
    print(f"Python version: {sys.version}")
    print()
    
    # Create directories
    create_directories()
    
    # Check/create .env file
    check_env_file()
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Run tests
    run_tests()
    
    print()
    print("=== Setup Complete ===")
    print()
    print("Next steps:")
    print("1. Update the .env file with your Mist API credentials")
    print("2. Activate the virtual environment:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("3. Run the example: python examples/auth_example.py")
    print()

if __name__ == "__main__":
    main()
