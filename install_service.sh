#!/bin/bash

# Nexus Userbot - Systemd Service Installer

echo "🚀 Installing Nexus systemd service..."

if [ "$EUID" -ne 0 ]; then 
    echo "❌ Run as root: sudo bash install_service.sh"
    exit 1
fi

# Stop existing service
systemctl stop nexus 2>/dev/null

# Copy service file
cp nexus.service /etc/systemd/system/nexus.service

# Reload systemd
systemctl daemon-reload

# Enable autostart
systemctl enable nexus.service

echo "✅ Service installed!"
echo ""
echo "📋 Commands:"
echo "  systemctl start nexus    - Start"
echo "  systemctl stop nexus     - Stop"
echo "  systemctl restart nexus  - Restart"
echo "  systemctl status nexus   - Status"
echo "  journalctl -u nexus -f   - Logs"
echo ""
read -p "Start Nexus now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    systemctl start nexus
    sleep 2
    systemctl status nexus
fi
