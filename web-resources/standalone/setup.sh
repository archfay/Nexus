#!/bin/bash

echo "🚀 Nexus Website - Standalone Setup"
echo "===================================="

cd "$(dirname "$0")/.."

if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "📥 Installing dependencies..."
pip install -r standalone/requirements.txt

echo "✅ Setup complete!"
echo ""
echo "To start the server:"
echo "  source venv/bin/activate"
echo "  python3 standalone/app.py"
echo ""
echo "Or use gunicorn for production:"
echo "  gunicorn -w 4 -b 0.0.0.0:8080 standalone.app:app"
