#!/usr/bin/env python3
"""
Setup script for installing Python dependencies.
Run this on the Raspberry Pi to install required packages.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Boiler Alarm Monitoring System")
    print("=" * 50)
    
    # Update package lists
    if not run_command("sudo apt update", "Updating package lists"):
        sys.exit(1)
    
    # Install Python 3 and pip if not already installed
    run_command("sudo apt install -y python3 python3-pip", "Installing Python 3 and pip")
    
    # Install system dependencies for GPIO
    run_command("sudo apt install -y python3-rpi.gpio", "Installing RPi.GPIO system package")
    
    # Install Python packages
    packages = [
        "RPi.GPIO",  # GPIO control
        "python-dotenv",  # Environment variable loading
    ]
    
    for package in packages:
        if not run_command(f"pip3 install {package}", f"Installing {package}"):
            print(f"⚠️  Warning: Failed to install {package}")
    
    # Create logs directory
    logs_dir = "/home/pi/boiler-alarm/logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir, exist_ok=True)
        print("📁 Created logs directory")
    
    # Set up environment file
    env_example = "/home/pi/boiler-alarm/config/.env.example"
    env_file = "/home/pi/boiler-alarm/.env"
    
    if os.path.exists(env_example) and not os.path.exists(env_file):
        run_command(f"cp {env_example} {env_file}", "Creating .env file from example")
        print("⚠️  Please edit .env file with your email credentials!")
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file with your email settings")
    print("2. Test the system: python3 utils.py test-email")
    print("3. Install as service: sudo systemd/install_service.sh")
    print("4. Start monitoring: sudo systemctl start boiler-alarm")

if __name__ == "__main__":
    main()