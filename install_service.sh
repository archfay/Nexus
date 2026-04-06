#!/bin/bash

# Nexus Userbot - Systemd Service Installer
# This script installs Nexus as a system service

echo "🚀 Installing Nexus as systemd service..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

# Copy service file
cp nexus.service /etc/systemd/system/nexus.service

# Reload systemd
systemctl daemon-reload

# Enable service (autostart on boot)
systemctl enable nexus.service

echo "✅ Service installed successfully!"
echo ""
echo "📋 Available commands:"
echo "  sudo systemctl start nexus    - Start Nexus"
echo "  sudo systemctl stop nexus     - Stop Nexus"
echo "  sudo systemctl restart nexus  - Restart Nexus"
echo "  sudo systemctl status nexus   - Check status"
echo "  sudo journalctl -u nexus -f   - View logs"
echo ""
echo "🔄 Starting Nexus..."
systemctl start nexus

echo "✅ Done! Nexus is now running in background"
