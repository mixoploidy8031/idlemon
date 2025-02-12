#!/bin/bash

# Exit on error
set -e

# Check if script is run with sudo
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script with sudo:"
    echo "sudo $0"
    exit 1
fi

# Define installation paths
INSTALL_DIR="/usr/local/games/idlemon"
DESKTOP_FILE="/usr/share/applications/idlemon.desktop"
EXECUTABLE="IdleMon"

# Get the real user (not sudo user)
REAL_USER="${SUDO_USER:-$USER}"
REAL_HOME="/home/$REAL_USER"

echo "Installing IdleMon..."

# Create installation directory
mkdir -p "$INSTALL_DIR"

# First, copy the executable from the dist directory
if [ -f "dist/$EXECUTABLE" ]; then
    cp "dist/$EXECUTABLE" "$INSTALL_DIR/"
else
    echo "Error: Executable not found in dist directory. Please build the project first."
    exit 1
fi

# Copy all other files to installation directory
cp -r assets config.json "$INSTALL_DIR/"

# Create desktop entry
cat > "$DESKTOP_FILE" << EOL
[Desktop Entry]
Version=1.0
Name=IdleMon
Comment=Automated Shiny Hunting Simulator
Exec=$INSTALL_DIR/$EXECUTABLE
Icon=$INSTALL_DIR/assets/images/icon_png.png
Terminal=false
Type=Application
Categories=Game;
Keywords=Pokemon;Game;Shiny;
StartupNotify=true
EOL

# Make the executable actually executable
chmod +x "$INSTALL_DIR/$EXECUTABLE"

# Set correct ownership and permissions
chown -R "$REAL_USER:$REAL_USER" "$INSTALL_DIR"
chmod -R 755 "$INSTALL_DIR"
chmod 644 "$DESKTOP_FILE"

# Create logs directory with correct permissions
mkdir -p "$INSTALL_DIR/logs"
chown "$REAL_USER:$REAL_USER" "$INSTALL_DIR/logs"
chmod 755 "$INSTALL_DIR/logs"

# Create symbolic link in /usr/local/bin
ln -sf "$INSTALL_DIR/$EXECUTABLE" "/usr/local/games/$EXECUTABLE"

# Update desktop database
update-desktop-database

# Add /usr/local/games to PATH if not already there
PROFILE_FILE="$REAL_HOME/.profile"
if ! grep -q "/usr/local/games" "$PROFILE_FILE" 2>/dev/null; then
    echo 'export PATH="/usr/local/games:$PATH"' >> "$PROFILE_FILE"
    chown "$REAL_USER:$REAL_USER" "$PROFILE_FILE"
fi

echo "Installation complete!"
echo "You can now run IdleMon from your applications menu or by typing 'IdleMon' in the terminal."
echo "Note: You may need to log out and back in for the PATH changes to take effect."
echo
echo "Installation directory: $INSTALL_DIR"
echo "Desktop entry: $DESKTOP_FILE"
echo
echo "To uninstall, run: sudo rm -rf $INSTALL_DIR $DESKTOP_FILE /usr/local/games/$EXECUTABLE" 