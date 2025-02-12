import json
import os
import sys
from pathlib import Path

def get_base_path():
    # Get the base path for the application, works both for dev and PyInstaller
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle (PyInstaller)
        exe_dir = Path(sys.executable).parent
        # Use _MEIPASS for reading resources, but exe_dir for writing data
        return {
            'runtime': Path(sys._MEIPASS),  # For reading resources
            'data': exe_dir  # For writing data files
        }
    else:
        # If running in development
        dev_path = Path(__file__).parent.parent
        return {
            'runtime': dev_path,
            'data': dev_path
        }

# Replace PROJECT_ROOT definition with:
PROJECT_ROOT = get_base_path()

# Pre-calculated hashes for Pokemon data files
POKEMON_DATA_HASHES = {
    "gen1": "bfe76e5d3b39b5a2a4f0faf0ed3a00d3a8775f7ee336df86fd562209cc5eb1b0",
    "gen2": "3679bef5ac839a7c288d4e1a07d79156c0ddb4b8a629ec32be53d0b12a8b5919",
    "gen3": "9c3a4d46e5ed8305a741af4dd538adb01b8dfced1f890f3c1b10063102f5d3d7",
    "gen4": "249b177d1110613155909c8dfdf9237b7d153fee79471f414dc1afdfda4604d1",
    "gen5": "1332dce2c35000475e1d3d3478dc51eb0fdad0946bcf4572f9bf8e11d4d63ab1"
}

DEFAULT_CONFIG = {
    "encounter_delay": 2.5, # Default is 2.5 seconds
    "rarity_weights": {
        "Very Common": 45, # Default is 40
        "Common": 30, # Default is 34
        "Semi-rare": 17, # Default is 20
        "Rare": 7, # Default is 5
        "Very Rare": 1 # Default is 1
    },
    "shiny_rate": 2000, # Default is 2000
    "mute_audio": False,  # Add default mute setting
    "shiny_count_file": "logs/shiny_count.bin",
    "pokemon_data_files": {  # Updated to support multiple generations
        "gen1": "assets/data/gen1_pokemon_names.txt",
        "gen2": "assets/data/gen2_pokemon_names.txt",
        "gen3": "assets/data/gen3_pokemon_names.txt",
        "gen4": "assets/data/gen4_pokemon_names.txt",
        "gen5": "assets/data/gen5_pokemon_names.txt"
    },
    "current_generation": "gen1",  # Add default generation setting
    "shinies_encounter_file": "logs/shinies_encountered.txt",
    "gif_directory": "assets/gifs",
    "background_image": "assets/images/default_background.jpg",
}

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = str(PROJECT_ROOT['data'] / config_file)
        # Update directory creation to include gen2-5 directories
        (PROJECT_ROOT['data'] / "logs").mkdir(exist_ok=True)
        (PROJECT_ROOT['data'] / "assets/data").mkdir(parents=True, exist_ok=True)
        for gen in range(1, 6):
            (PROJECT_ROOT['data'] / f"assets/gifs/gen{gen}/normal").mkdir(parents=True, exist_ok=True)
            (PROJECT_ROOT['data'] / f"assets/gifs/gen{gen}/shiny").mkdir(parents=True, exist_ok=True)
        (PROJECT_ROOT['data'] / "assets/images").mkdir(parents=True, exist_ok=True)
        (PROJECT_ROOT['data'] / "assets/sounds").mkdir(parents=True, exist_ok=True)
        self.config = self.load_config()

    def validate_pokemon_data(self, file_path):
        import hashlib
        
        gen = os.path.basename(file_path).split('_')[0]  # Extract gen1, gen2, etc.
        if not os.path.exists(file_path):
            print(f"Error: {file_path} not found. Please ensure all Pokemon data files are present.")
            sys.exit(1)
            
        # Read file in binary mode and normalize line endings to LF
        with open(file_path, "rb") as file:
            content = file.read()
            # Convert all line endings to LF
            content = content.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
            # Normalize whitespace while preserving line endings
            content = b'\n'.join(line.strip() for line in content.split(b'\n'))
            file_hash = hashlib.sha256(content).hexdigest()
            
        if file_hash != POKEMON_DATA_HASHES[gen]:
            print(f"Warning: {file_path} may have been modified. Hash verification failed.")
            print(f"Expected hash: {POKEMON_DATA_HASHES[gen]}")
            print(f"Actual hash: {file_hash}")
            sys.exit(1)  # Exit if hash verification fails
            
    def load_config(self):
        user_config = {}
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as file:
                    user_config = json.load(file)
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error loading config file: {e}. Using default settings.")
        
        # Merge defaults with user config
        config = {**DEFAULT_CONFIG, **user_config}
        
        # Convert relative paths to absolute paths if they're not already absolute
        path_keys = ["shiny_count_file", "shinies_encounter_file", "gif_directory"]
        for key in path_keys:
            if not os.path.isabs(config[key]):
                config[key] = str(PROJECT_ROOT['data'] / config[key])
        
        # Handle pokemon_data_files paths separately since it's a dictionary
        if not os.path.isabs(next(iter(config["pokemon_data_files"].values()))):
            config["pokemon_data_files"] = {
                gen: str(PROJECT_ROOT['data'] / path)
                for gen, path in config["pokemon_data_files"].items()
            }
        
        # Background image can be absolute or relative, handled in main.py
        
        # Validate all generation files
        for file_path in config["pokemon_data_files"].values():
            self.validate_pokemon_data(file_path)
            
        return config

# Helper functions to maintain backwards compatibility
def load_config():
    config_manager = ConfigManager()
    return config_manager.config

def check_file_exists(file_path):
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} does not exist.")
        return False
    return True
