# IdleMon - Automated Shiny Hunting Simulator

A Python-based simulator for encountering Pokémon with shiny hunting mechanics, featuring animated sprites, statistics tracking, and customizable settings.

![icon](assets/images/icon_png.png)

## Features

- Real-time Pokémon encounters with rarity-based spawning
- Animated sprites for both normal and shiny variants
- 1/2000 base shiny rate with visual and audio notifications
- Statistics tracking (encounters, shinies found, time elapsed)
- Modern UI with custom backgrounds
- Persistent progress saving

![screenshot of shiny gyrados encounter](assets/images/screenshot_gyra.png)

## Installation

### System Requirements
- Linux (Ubuntu/Debian-based distributions)
- Python 3.8 or later
- Display resolution: 500x500 minimum
- Audio output device (optional)

### Quick Install (Recommended)

1. Install system dependencies:
```bash
sudo apt-get install python3-pip python3-venv python3-tk python3-pygame python3-pil python3-colorama
```

2. Clone and enter the repository:
```bash
git clone -b linux https://github.com/mixoploidy8031/idlemon.git
cd idlemon
```

3. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install Python dependencies and build:
```bash
pip install -r requirements.txt pyinstaller
pyinstaller main.spec
```

5. Install the application:
```bash
sudo ./install_linux.sh
```

6. Start the application:
- From applications menu: Search for "IdleMon"
- From terminal: Type `IdleMon`

Note: You may need to log out and log back in for the PATH changes to take effect.

### Development Mode

If you want to run the application directly from source:

1. Follow steps 1-3 from the Quick Install section
2. Run the application:
```bash
python src/main.py
```

### Data Storage Locations

The application stores data differently depending on how it's run:

#### When Installed (Quick Install)
- All user data is stored in `~/.local/share/idlemon/`
  - Logs: `~/.local/share/idlemon/logs/error.log`
  - Shiny encounters: `~/.local/share/idlemon/logs/shinies_encountered.txt`
  - Shiny count: `~/.local/share/idlemon/logs/shiny_count.bin`

#### When Running from Source (Development Mode)
- All data is stored in the local `logs` directory
  - Logs: `logs/error.log`
  - Shiny encounters: `logs/shinies_encountered.txt`
  - Shiny count: `logs/shiny_count.bin`

### Uninstallation
```bash
sudo rm -rf /usr/local/games/idlemon /usr/share/applications/idlemon.desktop /usr/local/games/IdleMon
```

Note: This will not remove user data. To remove all user data, also delete:
```bash
rm -rf ~/.local/share/idlemon
```

## Configuration

The game can be configured by editing `config.json`. 

For development mode, edit the file directly in the project root.
For installed version, edit `/usr/local/games/idlemon/config.json` (may require sudo).

```json
{
    "encounter_delay": 2.5,        # Time between encounters in seconds
    "shiny_rate": 2000,           # 1 in X chance of finding a shiny
    "mute_audio": false,          # Set to true to disable all sounds
    "background_image": "assets/images/default_background.jpg",  # Path to background image
    "rarity_weights": {           # Spawn rates for different rarities
        "Very Common": 45,        # 45% chance
        "Common": 30,            # 30% chance
        "Semi-rare": 17,         # 17% chance
        "Rare": 7,              # 7% chance
        "Very Rare": 1          # 1% chance
    }
}
```

### Background Image
You can use a custom background image by setting the `background_image` path in `config.json`:
- Use a relative path from the game directory: `"background_image": "assets/images/my_background.jpg"`
- Or use an absolute path: `"background_image": "/home/user/pictures/my_background.jpg"`
- Supported formats: JPG, PNG
- If the image is not found, it will fall back to the default background

Note: After changing the config file in installed mode, you may need to fix permissions:
```bash
sudo chown $USER:$USER /usr/local/games/idlemon/config.json
```

## Troubleshooting

### Common Issues

1. **Application won't start**
   - Verify system dependencies are installed
   - Check error logs (location depends on installation method)
   - For installed version: `~/.local/share/idlemon/logs/error.log`
   - For development mode: `logs/error.log`

2. **Missing graphics/audio**
   - Ensure all assets were copied during installation
   - Check file permissions in `/usr/local/games/idlemon`

3. **Permission issues**
   ```bash
   sudo chown -R $USER:$USER /usr/local/games/idlemon
   sudo chmod -R 755 /usr/local/games/idlemon
   ```

4. **Lost progress/statistics**
   - Check the appropriate logs directory based on your installation method
   - Verify file permissions in the logs directory
   - For installed version: `chmod -R 755 ~/.local/share/idlemon`
   - For development mode: `chmod -R 755 logs`

## License
This project is licensed under the MIT License.
