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

### Quick Install

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

### Uninstallation
```bash
sudo rm -rf /usr/local/games/idlemon /usr/share/applications/idlemon.desktop /usr/local/games/IdleMon
```

## Configuration

The game can be configured by editing `config.json`:

```json
{
    "encounter_delay": 2.5,
    "mute_audio": false,
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

## Troubleshooting

### Common Issues

1. **Application won't start**
   - Verify system dependencies are installed
   - Check error logs in `~/.local/share/idlemon/logs/error.log`

2. **Missing graphics/audio**
   - Ensure all assets were copied during installation
   - Check file permissions in `/usr/local/games/idlemon`

3. **Permission issues**
   ```bash
   sudo chown -R $USER:$USER /usr/local/games/idlemon
   sudo chmod -R 755 /usr/local/games/idlemon
   ```

## License
This project is licensed under the MIT License.
