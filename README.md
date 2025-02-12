# IdleMon - Automated Shiny Hunting Simulator

A Python-based simulator for encountering Pokémon with shiny hunting mechanics, featuring animated sprites, statistics tracking, and customizable settings.

![icon](assets/images/icon_png.png)

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Windows](#windows)
  - [Linux](#linux)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features

### Core Features
- **Encounter Simulation**
  - Real-time Pokémon encounters with rarity-based spawning
  - Animated sprites for both normal and shiny variants
  - Customizable encounter delay

### Shiny Hunting
- 1/2000 base shiny rate
- Shiny encounter tracking and statistics
- Special visual and audio effects for shinies
- Persistent shiny count storage

### User Interface
- Clean, modern interface with:
  - Real-time encounter counter
  - Elapsed time tracking
  - Total shinies found display
  - Animated Pokémon sprites
  - Custom background support

### Audio System
- Shiny encounter notification sounds
- Continue button sound effects
- Optional audio muting

### Data Management
- Secure hash verification for data files
- Automatic save data handling
- Cross-platform compatibility
- UTF-8 encoding support

## Requirements

### System Requirements
- Python 3.8 or later
- Display resolution: 500x500 minimum
- Audio output device (optional)

### Python Dependencies
```bash
# Install via pip
pip install -r requirements.txt

# Core dependencies
pygame==2.5.2      # Audio and sprite handling
Pillow==10.2.0     # Image processing
colorama==0.4.6    # Terminal output formatting
```

## Installation

### Windows
1. Download the latest release from the releases page
2. Extract the ZIP archive
3. Run `IdleMon.exe`

### Linux

#### System Dependencies
```bash
# Debian/Ubuntu
sudo apt-get install python3-tk python3-pip libsdl2-2.0-0 libsdl2-mixer-2.0-0

# Fedora/RHEL
sudo dnf install python3-tkinter python3-pip SDL2 SDL2_mixer

# Arch Linux
sudo pacman -S python-tkinter python-pip sdl2 sdl2_mixer
```

#### Option 1: Using the Release Package
1. Download and extract the latest release
2. Make scripts executable:
   ```bash
   chmod +x install_linux.sh uninstall_linux.sh
   ```
3. Install:
   ```bash
   sudo ./install_linux.sh
   ```

The installer will:
- Install to `/usr/local/games/idlemon`
- Create desktop entry in `/usr/share/applications`
- Set up permissions and PATH
- Create required directories

#### Option 2: Building from Source
1. Clone the repository:
   ```bash
   git clone https://github.com/mixoploidy8031/idlemon.git
   cd idlemon
   ```

2. Set up Python environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install pyinstaller
   ```

3. Build and install:
   ```bash
   pyinstaller main.spec
   sudo ./install_linux.sh
   ```

#### Uninstallation
Option 1: Using the script
```bash
sudo ./uninstall_linux.sh
```

Option 2: Manual removal
```bash
sudo rm -rf /usr/local/games/idlemon /usr/share/applications/idlemon.desktop /usr/local/games/IdleMon
sudo update-desktop-database
```

## Configuration

### Config File (config.json)
```json
{
    "encounter_delay": 2.5,
    "mute_audio": false,
    "background_image": "assets/images/custom_background.jpg",
    "shiny_rate": 2000,
    "rarity_weights": {
        "Very Common": 45,
        "Common": 30,
        "Semi-rare": 17,
        "Rare": 7,
        "Very Rare": 1
    }
}
```

### Customization Options
- **encounter_delay**: Time between encounters (seconds)
- **mute_audio**: Enable/disable sound effects
- **background_image**: Custom background path
- **shiny_rate**: Modify shiny encounter rate
- **rarity_weights**: Adjust Pokémon spawn rates

## Usage Guide

### Basic Usage
1. Launch IdleMon via:
   - Desktop shortcut
   - Start menu
   - Terminal command: `IdleMon`

2. The simulator will:
   - Start automatic encounters
   - Display Pokémon sprites
   - Track statistics
   - Save progress automatically

### Shiny Encounters
When a shiny appears:
1. Special animation plays
2. Sound effect triggers (if enabled)
3. Counter updates
4. Continue button appears

### Statistics Tracking
The interface shows:
- Current encounter count
- Total shinies found
- Session time elapsed
- Pokémon details (name, rarity)

## Project Structure
```
idlemon/
├── src/                    # Source code
│   ├── main.py            # Application entry point
│   ├── config_loader.py   # Configuration management
│   ├── data_manager.py    # Data handling
│   ├── encounter_manager.py# Encounter logic
│   ├── gui_elements.py    # UI components
│   └── logger.py          # Logging system
├── assets/                 # Game resources
│   ├── gifs/              # Pokémon sprites
│   ├── sounds/            # Audio files
│   ├── data/              # Game data
│   └── images/            # UI images
├── logs/                   # Game logs
└── config.json            # User settings
```

## Troubleshooting

### Common Issues

#### Application Won't Start
- Check Python version: `python3 --version`
- Verify dependencies: `pip list`
- Check error logs: `logs/error.log`

#### Missing Graphics
- Verify assets directory structure
- Check file permissions
- Ensure GIF files are valid

#### Audio Issues
- Check system volume
- Verify SDL2 installation
- Check `mute_audio` setting

#### Linux-Specific
- Desktop entry issues:
  ```bash
  sudo update-desktop-database
  ```
- Permission problems:
  ```bash
  sudo chown -R $USER:$USER /usr/local/games/idlemon
  sudo chmod -R 755 /usr/local/games/idlemon
  ```

### Data Reset
To reset progress:
1. Navigate to `logs/`
2. Delete:
   - `shiny_count.bin`
   - `shinies_encountered.txt`
   - `error.log`

## License
This project is licensed under the MIT License.
