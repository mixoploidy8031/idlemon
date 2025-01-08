# Pokémon Hunting Simulator

This project simulates encountering Pokémon with a chance of finding shiny Pokémon. It features animated GIFs for Pokémon encounters, shiny tracking, and customization options through a configuration file.

---

## Features
- **Encounter simulation:** Displays Pokémon with their respective rarities.
- **Shiny tracking:** Counts the total number of shiny Pokémon found.
- **GIF animations:** Shows normal and shiny Pokémon as animated GIFs.
- **Customizable settings:** Allows customization of the GIF directory and background using a JSON configuration file.

---

## Requirements
- Python 3.8 or later
- Required libraries: `Pillow`, `random`, `time`, `os`, `base64`, `pygame`, `tkinter`

Install the dependencies:
```bash
pip install pillow pygame
```

---

## Usage
1. Clone the repository and navigate to the project directory.
2. Run the `main.py` file to start the simulator:
   ```bash
   python main.py
   ```

---

## Configuration
The simulator uses a JSON file (`config.json`) to define key settings. Below are the customizable options and their descriptions:

### Example `config.json`
```json
{
    "gif_directory": "path/to/gif/directory",
    "background_image": "path/to/background/image",
}
```

### Customizing the Configuration
- **`gif_directory`:** Specifies the directory containing Pokémon GIFs. Subdirectories for `normal` and `shiny` Pokémon are required.
  - Example:
    ```
    gen1_gifs/
    ├── normal/
    │   ├── pikachu.gif
    │   └── charmander.gif
    └── shiny/
        ├── pikachu.gif
        └── charmander.gif
    ```

- **`background_image`:** Path to the background image displayed in the simulator. Replace with the desired image path.
  - Example:
    ```json
    "background_image": "assets/backgrounds/forest.png"
    ```

- **`shiny_count_file`:** Path to the file that stores the total number of shiny Pokémon found.  
  ⚠ **WARNING:** Do not delete or modify the `shiny_count_file`. Any changes to this file will result in the shiny count resetting to `0` and may cause unintended behavior in the program.

- **`pokemon_data_file`:** Path to the .txt file containing Pokémon data with name and rarity.
  - Example .txt format:
    ```
    pikachu,common
    charmander,rare
    bulbasaur,common
    ```

---

## How to Update the Config
1. Open the `config.json` file in any text editor.
2. Edit the values for the settings you want to change.
3. Save the file, and restart the simulator for changes to take effect.

---

## Troubleshooting
- **Missing GIFs:** Ensure the directory structure matches the example, and all Pokémon have corresponding `normal` and `shiny` GIFs.
- **Shiny count reset:** If the `shiny_count.txt` file is missing, deleted, or modified, the shiny count will reset to `0`. To avoid this, do not alter the file manually.

---

## License
This project is licensed under the MIT License.

