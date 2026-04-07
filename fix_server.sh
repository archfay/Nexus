#!/bin/bash

echo "🔧 Fixing Nexus for Python 3.13..."

cd /root/Nexus

# Stop service
systemctl stop nexus

# Pull latest changes
git pull

# Remove old venv and create new one
rm -rf venv
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install dependencies one by one to catch errors
echo "Installing core dependencies..."
pip install heroku-tl-new>=2.0.0
pip install Pillow>=10.0.0
pip install orjson>=3.9.0
pip install aiohttp==3.11.18
pip install aiohttp_jinja2>=1.5.0
pip install jinja2>=3.1.0
pip install aiogram>=3.26.0
pip install setuptools==69.0.0
pip install GitPython>=3.1.0
pip install emoji>=2.0.0
pip install grapheme
pip install requests>=2.31.0
pip install meval
pip install psutil>=5.9.0
pip install beautifulsoup4>=4.12.0
pip install lxml>=4.9.0

echo "Installing optional dependencies..."
pip install pet-pet-gif || echo "Warning: pet-pet-gif failed, skipping"

# Start service
systemctl start nexus

# Show status
sleep 3
systemctl status nexus

echo ""
echo "✅ Done! Check logs with: journalctl -u nexus -f"
echo "Test commands: .ping and .info"
