# IdleMon for Linux

This is the Linux version of IdleMon, an automated shiny hunting simulator. For the Windows version, visit the main branch: https://github.com/mixoploidy8031/idlemon

## Installation

### System Requirements
- Linux (Ubuntu/Debian-based distributions)
- Display resolution: 500x500 minimum
- Audio output device (optional)

### Quick Install (Recommended)

1. Download and extract the latest release, or clone the repository:
```bash
git clone -b linux https://github.com/mixoploidy8031/idlemon.git
cd idlemon
```

2. Run the installation script:
```bash
sudo ./install_idlemon.sh
```

3. Start the application:
- From applications menu: Search for "IdleMon"
- From terminal: Type `IdleMon`

Note: You may need to log out and log back in for the PATH changes to take effect.

### Development Mode

If you want to run the application directly from source or contribute to development:

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

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. Run the application:
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

### Configuration

The game can be configured by editing `config.json`. 

For development mode, edit the file directly in the project root.
For installed version, edit `/usr/local/games/idlemon/config.json` (may require sudo).

```json
{
    "background_image": "assets/images/default_background.jpg",  # Path to background image
    "mute_audio": false                                         # Set to true to disable all sounds
}
```

#### Custom Background Images
You can use a custom background image by setting the `background_image` path:
- Use a relative path: `"background_image": "assets/images/my_background.jpg"`
- Or absolute path: `"background_image": "/home/user/pictures/my_background.jpg"`
- Supported formats: JPG, PNG
- If not found, falls back to default background

#### Audio Settings
- Set `mute_audio` to `true` to disable all sound effects
- Set `mute_audio` to `false` to enable sound effects

Note: After changing the config file in installed mode, fix permissions:
```bash
sudo chown $USER:$USER /usr/local/games/idlemon/config.json
```

### Uninstallation

You can uninstall using the provided script:
```bash
sudo ./uninstall_idlemon.sh
```

Or manually:
```bash
sudo rm -rf /usr/local/games/idlemon /usr/share/applications/idlemon.desktop /usr/local/games/IdleMon
```

To also remove user data:
```bash
rm -rf ~/.local/share/idlemon
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
