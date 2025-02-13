#!/bin/bash

# Exit on error
set -e

# Check if script is run with sudo
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script with sudo:"
    echo "sudo $0"
    exit 1
fi

# Define paths
INSTALL_DIR="/usr/local/games/idlemon"
DESKTOP_FILE="/usr/share/applications/idlemon.desktop"
EXECUTABLE="/usr/local/games/IdleMon"

echo "Uninstalling IdleMon..."

# Remove installation directory
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "Removed $INSTALL_DIR"
fi

# Remove desktop entry
if [ -f "$DESKTOP_FILE" ]; then
    rm -f "$DESKTOP_FILE"
    echo "Removed $DESKTOP_FILE"
fi

# Remove executable symlink
if [ -L "$EXECUTABLE" ]; then
    rm -f "$EXECUTABLE"
    echo "Removed $EXECUTABLE"
fi

# Update desktop database
update-desktop-database

echo "Uninstallation complete!"
echo
echo "Note: The PATH modification in ~/.profile (if any) was not removed."
echo "You can manually remove the line 'export PATH=\"/usr/local/games:\$PATH\"' if desired." 