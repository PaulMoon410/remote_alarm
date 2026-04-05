#!/bin/bash

# Boiler Alarm Service Installation Script
# This script installs the boiler alarm monitoring service on Raspberry Pi

set -e

echo "🔧 Installing Boiler Alarm Monitoring Service..."

# Configuration
SERVICE_NAME="boiler-alarm"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
PROJECT_DIR="/home/pi/boiler-alarm"
USER="pi"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

# Create project directory if it doesn't exist
if [ ! -d "$PROJECT_DIR" ]; then
    echo "📁 Creating project directory..."
    mkdir -p "$PROJECT_DIR"
    chown "$USER:$USER" "$PROJECT_DIR"
fi

# Copy service file
echo "📋 Installing systemd service file..."
cp "$(dirname "$0")/boiler-alarm.service" "$SERVICE_FILE"

# Update service file with correct paths
sed -i "s|/home/pi/boiler-alarm|$PROJECT_DIR|g" "$SERVICE_FILE"

# Reload systemd
echo "🔄 Reloading systemd..."
systemctl daemon-reload

# Enable service (but don't start yet)
echo "✅ Enabling service..."
systemctl enable "$SERVICE_NAME"

echo "🎉 Installation complete!"
echo ""
echo "Next steps:"
echo "1. Copy your project files to $PROJECT_DIR"
echo "2. Configure your .env file with email settings"
echo "3. Test the service: sudo systemctl start $SERVICE_NAME"
echo "4. Check status: sudo systemctl status $SERVICE_NAME"
echo "5. View logs: sudo journalctl -f -u $SERVICE_NAME"
echo ""
echo "To start the service automatically:"
echo "sudo systemctl start $SERVICE_NAME"