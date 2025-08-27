# Script to install all required packages
import subprocess
import sys
import os

def install_requirements():
    print("Installing requirements...")
    try:
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        requirements_path = os.path.join(current_dir, "..", "requirements.txt")
        
        print(f"Looking for requirements at: {requirements_path}")
        
        # Check if file exists
        if not os.path.exists(requirements_path):
            print("❌ requirements.txt not found! Please make sure it's in the main project folder.")
            return
        
        # Install from requirements.txt
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        print("✅ All packages installed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    install_requirements()