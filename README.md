# IdleMon - Automated Shiny Hunting Simulator

This project simulates encountering Pokémon with a chance of finding shiny Pokémon. It features animated GIFs for Pokémon encounters, shiny tracking, encounter statistics, and customization options.

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

---

![Screenshot 2025-01-11 015653](https://github.com/user-attachments/assets/6939a1db-e5e2-43cb-8a5f-755b7087ad3a)
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
2. Open a terminal in the root directory of idlemon
3. Run the following command to package as an executable:
   ```bash
   pyinstaller src/main.spec
   ```
   Alternatively, you can just run the simulator directly:
   ```bash
   python src/main.py
   ```

Option 2: Run executable
1. Download the latest release
2. Extract the zip file
3. Navigate to the `src` folder
4. Run IdleMon.exe from the `src` folder
5. Alternatively, create a shortcut to IdleMon.exe and place the shortcut in a location of your choosing

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
│   │   ├── normal/
│   │   │   └── pokemon.gif
│   │   └── shiny/
│   │       └── pokemon.gif
│   ├── sounds/
│   │   ├── shiny_sound1.wav
│   │   └── continue_sound1.wav
│   ├── data/
│   │   └── gen1_pokemon_names.txt
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
- **Missing GIFs:** Ensure GIF files exist in both normal/shiny directories
- **Animation Issues:** Verify GIF files are properly formatted
- **Sound Problems:** Check that sound files exist in the assets/sounds directory
- **Background Image:** Ensure the specified path exists and is accessible
- **config.json:** Ensure the config.json file is correctly formatted and all paths are valid

---

## License
This project is licensed under the MIT License.
