"""
SUMO-Forge Setup Script
========================

Use this script to set up SUMO-Forge for development or production.
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def check_python_version():
    """Check if Python version is compatible."""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Python 3.8 or higher is required")
        return False
    print("✅ Python version is compatible")
    return True


def create_virtual_environment():
    """Create a virtual environment."""
    print_header("Creating Virtual Environment")
    
    if Path("venv").exists():
        print("⏭️  Virtual environment already exists, skipping...")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: Failed to create virtual environment: {e}")
        return False


def install_dependencies():
    """Install required dependencies."""
    print_header("Installing Dependencies")
    
    # Determine pip executable
    if sys.platform == "win32":
        pip_path = Path("venv/Scripts/pip.exe")
    else:
        pip_path = Path("venv/bin/pip")
    
    if not pip_path.exists():
        print("⚠️  Virtual environment not found, using system pip")
        pip_cmd = "pip"
    else:
        pip_cmd = str(pip_path)
    
    try:
        # Upgrade pip
        print("Upgrading pip...")
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True)
        
        # Install requirements
        print("Installing requirements...")
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: Failed to install dependencies: {e}")
        return False


def create_directories():
    """Create necessary directories."""
    print_header("Creating Directories")
    
    directories = ["outputs", "templates/networks"]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created/verified: {directory}")
    
    return True


def create_env_file():
    """Create .env file from .env.example if it doesn't exist."""
    print_header("Setting up Environment Variables")
    
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if env_path.exists():
        print("⏭️  .env file already exists, skipping...")
        return True
    
    if env_example_path.exists():
        import shutil
        shutil.copy(env_example_path, env_path)
        print("✅ Created .env file from .env.example")
        print("⚠️  Remember to update .env with your actual API keys!")
    else:
        print("⚠️  .env.example not found, skipping...")
    
    return True


def verify_installation():
    """Verify that everything is set up correctly."""
    print_header("Verifying Installation")
    
    required_files = [
        "app.py",
        "requirements.txt",
        "src/__init__.py",
        "src/core/__init__.py",
        "src/network/__init__.py"
    ]
    
    all_ok = True
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING!")
            all_ok = False
    
    return all_ok


def print_next_steps():
    """Print next steps for the user."""
    print_header("Setup Complete!")
    
    if sys.platform == "win32":
        activate_cmd = "venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"
    
    print("Next steps:")
    print(f"  1. Activate virtual environment: {activate_cmd}")
    print("  2. Update .env file with your API keys (if needed)")
    print("  3. Run the application: streamlit run app.py")
    print("\nFor deployment instructions, see DEPLOYMENT.md")
    print("\n🎉 Happy coding!\n")


def main():
    """Main setup function."""
    print("\n")
    print("╔" + "═"*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  🚗 SimpleSUMO Setup Script".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "═"*58 + "╝")
    
    steps = [
        ("Checking Python version", check_python_version),
        ("Creating virtual environment", create_virtual_environment),
        ("Installing dependencies", install_dependencies),
        ("Creating directories", create_directories),
        ("Setting up environment", create_env_file),
        ("Verifying installation", verify_installation),
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at: {step_name}")
            print("Please fix the errors and run setup.py again.")
            sys.exit(1)
    
    print_next_steps()


if __name__ == "__main__":
    main()
