# IdleMon - Automated Shiny Hunting Simulator

This project simulates encountering Pokémon with a chance of finding shiny Pokémon. It features animated GIFs for Pokémon encounters, shiny tracking, encounter statistics, and customization options.

![icon](assets/images/icon_png.png)

---

## Features
- **Encounter simulation:** Displays Pokémon with their respective rarities
- **Shiny hunting:** Tracks total shinies found with a 1/2000 chance
- **Animated sprites:** Shows normal and shiny Pokémon as animated GIFs
- **Statistics tracking:** 
  - Real-time encounter counter (resets after continuing from a shiny)
  - Time elapsed tracker
  - Total shinies found counter
- **Sound effects:** 
  - Shiny encounter notification
  - Continue button confirmation
  - Optional muting through config
- **User-friendly customization:** Easily configure settings through a simple config.json file - no coding required!
  - Choose your own background image
  - Toggle sound effects on/off

![screenshot of shiny gyrados encounter](assets/images/screenshot_gyra.png)

---

## Requirements
- Python 3.8 or later
- Required libraries: `Pillow`, `pygame`, `tkinter`, `colorama`

Install dependencies:
```bash
pip install pillow pygame colorama
```

---

## Usage

Option 1: Run from source
1. Clone the repository
2. Run the simulator from the project root:
   ```bash
   python src/main.py
   ```

Option 2: Run executable
1. Download the latest release
2. Extract the zip file
3. Run IdleMon.exe

## Installation

### Windows
1. Download the latest release
2. Extract the zip file
3. Run IdleMon.exe

### Linux

#### Option 1: Using the Release Package
1. Download the latest release
2. Extract the archive
3. Open terminal in the extracted directory
4. Make the installation scripts executable:
   ```bash
   chmod +x install_linux.sh uninstall_linux.sh
   ```
5. Run the installation script with sudo:
   ```bash
   sudo ./install_linux.sh
   ```

The installation script will:
- Install the game to `/usr/local/games/idlemon`
- Create a desktop entry in `/usr/share/applications`
- Set up proper file permissions
- Add the game to your system PATH
- Create necessary directories for logs and data

After installation, you can:
- Launch IdleMon from your applications menu
- Run it from terminal with `IdleMon`
- Access your save data in `/usr/local/games/idlemon/logs`

#### Option 2: Building from Source
1. Install required packages:
   ```bash
   sudo apt-get install python3-tk python3-pip git
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/idlemon.git
   cd idlemon
   ```

3. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

5. Build the executable:
   ```bash
   pyinstaller main.spec
   ```

6. Run the installation script:
   ```bash
   sudo ./install_linux.sh
   ```

#### Uninstalling
To uninstall IdleMon, you have two options:

1. Using the uninstall script:
   ```bash
   sudo ./uninstall_linux.sh
   ```

2. Manual uninstallation:
   ```bash
   sudo rm -rf /usr/local/games/idlemon /usr/share/applications/idlemon.desktop /usr/local/games/IdleMon
   sudo update-desktop-database
   ```

After uninstalling, you may want to:
- Remove the PATH modification from `~/.profile` if you don't need it
- Delete any remaining configuration files in your home directory

#### Customizing the Installation
- The game is installed to `/usr/local/games/idlemon` by default
- The desktop entry is created in `/usr/share/applications/idlemon.desktop`
- You can customize the installation by:
  1. Editing the `install_linux.sh` script before running it
  2. Manually editing the desktop entry file:
     ```bash
     sudo nano /usr/share/applications/idlemon.desktop
     ```
  3. Creating a local desktop entry in `~/.local/share/applications/`

#### Running Without Installation
You can also run the game directly without installation:
1. Make the executable file executable:
   ```bash
   chmod +x IdleMon
   ```
2. Run the game:
   ```bash
   ./IdleMon
   ```

Note: Running without installation will still create necessary directories and save files relative to the executable's location.

#### Troubleshooting Linux Installation
- If the game icon doesn't appear in your applications menu:
  ```bash
  # Update desktop database
  sudo update-desktop-database
  ```
- If you get permission errors:
  ```bash
  # Fix ownership of the game directory
  sudo chown -R $USER:$USER /usr/local/games/idlemon
  # Fix permissions
  sudo chmod -R 755 /usr/local/games/idlemon
  ```
- If you get "command not found":
  ```bash
  # Add the games directory to your PATH
  echo 'export PATH="/usr/local/games:$PATH"' >> ~/.bashrc
  source ~/.bashrc
  ```
- If the game won't start:
  1. Check the error log: `/usr/local/games/idlemon/logs/error.log`
  2. Try running from terminal to see error messages
  3. Verify all dependencies are installed:
     ```bash
     ldd /usr/local/games/idlemon/IdleMon
     ```

---

## Configuration
The simulator uses a JSON file (`config.json`) for customization:

### Example `config.json`
```json
{
    "gif_directory": "assets/gifs",
    "background_image": "C:/Users/YourName/Pictures/custom_background.png",
    "mute_audio": false
}
```

Note: All paths in the config file should be relative to the project root directory.

### Key Settings
- **`gif_directory`:** Path to Pokémon GIFs (requires `normal` and `shiny` subdirectories)
- **`background_image`:** Path to background image. Can be:
  - Absolute path (e.g., "C:/Users/YourName/Pictures/custom_background.png")
  - Relative path from project root (e.g., "assets/images/custom_background.png")
  - Defaults to "assets/images/default_background.jpg" if not found
- **`mute_audio`:** Set to `true` to disable all sound effects (default: `false`)

### Directory Structure
```
project_root/
├── src/
│   ├── main.py
│   ├── config_loader.py
│   ├── data_manager.py
│   ├── encounter_manager.py
│   ├── gui_elements.py
│   └── logger.py
├── assets/
│   ├── gifs/
│   │   ├── gen1/
│   │   │   ├── normal/
│   │   │   └── shiny/
│   │   ├── gen2/
│   │   │   ├── normal/
│   │   │   └── shiny/
│   │   ├── gen3/
│   │   │   ├── normal/
│   │   │   └── shiny/
│   │   ├── gen4/
│   │   │   ├── normal/
│   │   │   └── shiny/
│   │   └── gen5/
│   │       ├── normal/
│   │       └── shiny/
│   ├── sounds/
│   │   ├── shiny_sound1.wav
│   │   └── continue_sound1.wav
│   ├── data/
│   │   ├── gen1_pokemon_names.txt
│   │   ├── gen2_pokemon_names.txt
│   │   ├── gen3_pokemon_names.txt
│   │   ├── gen4_pokemon_names.txt
│   │   └── gen5_pokemon_names.txt
│   └── images/
│       └── background.png
├── logs/
│   ├── shiny_count.bin
│   ├── shinies_encountered.txt
│   └── error.log
└── config.json
```

---

## Features Guide

### Encounter System
- Each encounter has a chance of being shiny (1/2000 by default)
- When a shiny is found:
  1. The encounter animation changes
  2. A sound plays (if not muted)
  3. The encounter count remains displayed
  4. A continue button appears
- After pressing continue:
  1. The encounter counter resets to 0
  2. A new hunting session begins

### Sound System
- Shiny encounters trigger a special sound effect
- Continue button plays a confirmation sound
- Optional muting through config.json

### Statistics Tracking
- Real-time encounter counter (resets after continuing from a shiny)
- Elapsed time tracker
- Total shiny Pokémon found
- Automatic data saving for shiny counts

### Resetting Progress
To reset your hunting progress, you can either:

Delete individual files:
1. Navigate to the `logs` directory
2. Delete these files:
   - `shiny_count.bin` (resets total shinies to 0)
   - `shinies_encountered.txt` (clears shiny encounter history)

OR

Simply delete the entire `logs` directory.

New files will be automatically created on next launch.

---

## Troubleshooting
- **Missing GIFs:** Ensure GIF files exist in the correct generation's normal/shiny directories
- **Animation Issues:** Verify GIF files are properly formatted
- **Sound Problems:** Check that sound files exist in the assets/sounds directory
- **Background Image:** Ensure the specified path exists and is accessible
- **config.json:** Ensure the config.json file is correctly formatted and all paths are valid

---

## License
This project is licensed under the MIT License.
