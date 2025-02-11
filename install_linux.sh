#!/bin/bash

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Create installation directory
INSTALL_DIR="/usr/local/games/idlemon"
mkdir -p "$INSTALL_DIR"

# Copy files
echo "Copying files..."
cp -r dist/IdleMon/* "$INSTALL_DIR/"
cp idlemon.desktop "$INSTALL_DIR/"

# Make the game executable
chmod +x "$INSTALL_DIR/IdleMon"

# Create desktop entry
echo "Creating desktop entry..."
desktop_file="/usr/share/applications/idlemon.desktop"
cp idlemon.desktop "$desktop_file"

# Update desktop database
update-desktop-database /usr/share/applications/

echo "Installation complete!"
echo "You can now launch IdleMon from your applications menu or run it from terminal with 'IdleMon'" 