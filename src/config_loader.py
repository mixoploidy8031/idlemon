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
    "gen1": "bb1fd5dbb801d1e8f453d39eedc85f20fb96c804613041b236581e4037645b5f",
    "gen2": "6bac78b82268154f307cbdff766e2d71c67f48881bd296f5f1d1ac6af556b5c3",
    "gen3": "edc5d92ae40dd6d8cc7205537d58b570fede40970ba2cfd8bb9e7ab3241d21cb",
    "gen4": "56e5512eff1684bf4fac1d512d5ab8fd9fe49c1058260f85e3a43a57fbd8b8eb",
    "gen5": "35f7fbd7e12604d46517389f8d1133f06e67d93b3dbe4fc6b894f26b658c0f73"
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
            
        with open(file_path, "rb") as file:
            file_hash = hashlib.sha256(file.read()).hexdigest()
            
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
