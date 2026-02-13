#!/bin/bash
# Setup script for router restart automation

set -e

echo "Setting up Router Restart Automation..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed"
    exit 1
fi

# Install Chrome/Chromium if not present
if ! command -v chromium &> /dev/null && ! command -v google-chrome &> /dev/null; then
    echo "Installing Chromium..."
    sudo apt-get update
    sudo apt-get install -y chromium-browser
fi

# Install ChromeDriver
echo "Installing ChromeDriver..."
sudo apt-get install -y chromium-chromedriver

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Make script executable
chmod +x router_restart.py

# Create log directory
sudo mkdir -p /var/log
sudo touch /var/log/router_restart.log
sudo chown $USER:$USER /var/log/router_restart.log

echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Test the script: python3 router_restart.py"
echo "2. Add to crontab: crontab -e"
echo "3. Add this line to run at 3 AM daily:"
echo "   0 3 * * * /path/to/router_restart.py"
echo ""
