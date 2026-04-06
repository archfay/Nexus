#!/bin/bash

echo "🔧 Fixing Nexus dependencies and restarting..."

cd /root/Nexus

# Stop service
systemctl stop nexus

# Pull latest changes
git pull

# Activate venv
source venv/bin/activate

# Install/update all dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall --no-cache-dir

# Start service
systemctl start nexus

# Show status
sleep 3
systemctl status nexus

echo ""
echo "✅ Done! Check logs with: journalctl -u nexus -f"
