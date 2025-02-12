import json
import os
import sys
from pathlib import Path

def get_base_path():
    # Get the base path for the application, works both for dev and PyInstaller
    # Returns:
    #     dict: Contains two paths:
    #         'runtime': Path for reading resources (uses _MEIPASS in PyInstaller)
    #         'data': Path for writing data files (uses executable directory)
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle (PyInstaller)
        exe_dir = Path(sys.executable).parent
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

# Project root path based on execution context
PROJECT_ROOT = get_base_path()

# Pre-calculated hashes for Pokemon data files
# Format: generation -> SHA-256 hash
POKEMON_DATA_HASHES = {
    "gen1": "bfe76e5d3b39b5a2a4f0faf0ed3a00d3a8775f7ee336df86fd562209cc5eb1b0",
    "gen2": "3679bef5ac839a7c288d4e1a07d79156c0ddb4b8a629ec32be53d0b12a8b5919",
    "gen3": "9c3a4d46e5ed8305a741af4dd538adb01b8dfced1f890f3c1b10063102f5d3d7",
    "gen4": "249b177d1110613155909c8dfdf9237b7d153fee79471f414dc1afdfda4604d1",
    "gen5": "1332dce2c35000475e1d3d3478dc51eb0fdad0946bcf4572f9bf8e11d4d63ab1"
}

# Default configuration settings
DEFAULT_CONFIG = {
    "encounter_delay": 2.5,  # Delay between encounters in seconds
    "rarity_weights": {
        "Very Common": 45,  # 45% chance
        "Common": 30,      # 30% chance
        "Semi-rare": 17,   # 17% chance
        "Rare": 7,         # 7% chance
        "Very Rare": 1     # 1% chance
    },
    "shiny_rate": 2000,    # 1/2000 chance of shiny
    "mute_audio": False,   # Audio enabled by default
    "shiny_count_file": "logs/shiny_count.bin",
    "pokemon_data_files": {  # Paths to Pokemon data files for each generation
        "gen1": "assets/data/gen1_pokemon_names.txt",
        "gen2": "assets/data/gen2_pokemon_names.txt",
        "gen3": "assets/data/gen3_pokemon_names.txt",
        "gen4": "assets/data/gen4_pokemon_names.txt",
        "gen5": "assets/data/gen5_pokemon_names.txt"
    },
    "current_generation": "gen1",  # Default to generation 1
    "shinies_encounter_file": "logs/shinies_encountered.txt",
    "gif_directory": "assets/gifs",
    "background_image": "assets/images/default_background.jpg",
}

class ConfigManager:
    # Manages configuration loading and validation
    def __init__(self, config_file="config.json"):
        # Initialize configuration manager
        # Args:
        #     config_file (str): Path to configuration file, relative to project root
        self.config_file = str(PROJECT_ROOT['data'] / config_file)
        
        # Create necessary directories
        (PROJECT_ROOT['data'] / "logs").mkdir(exist_ok=True)
        (PROJECT_ROOT['data'] / "assets/data").mkdir(parents=True, exist_ok=True)
        
        # Create generation-specific directories
        for gen in range(1, 6):
            (PROJECT_ROOT['data'] / f"assets/gifs/gen{gen}/normal").mkdir(parents=True, exist_ok=True)
            (PROJECT_ROOT['data'] / f"assets/gifs/gen{gen}/shiny").mkdir(parents=True, exist_ok=True)
            
        # Create other asset directories
        (PROJECT_ROOT['data'] / "assets/images").mkdir(parents=True, exist_ok=True)
        (PROJECT_ROOT['data'] / "assets/sounds").mkdir(parents=True, exist_ok=True)
        
        self.config = self.load_config()

    def validate_pokemon_data(self, file_path):
        # Validate Pokemon data file against stored hash
        # Args:
        #     file_path (str): Path to the Pokemon data file
        # Returns:
        #     bool: True if validation passes, False otherwise
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
        # Load and validate configuration from file
        # Returns:
        #     dict: Merged configuration (user config + defaults)
        user_config = {}
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as file:
                    user_config = json.load(file)
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error loading config file: {e}. Using default settings.")
        
        # Merge defaults with user config
        config = {**DEFAULT_CONFIG, **user_config}
        
        # Convert relative paths to absolute paths
        path_keys = ["shiny_count_file", "shinies_encounter_file", "gif_directory"]
        for key in path_keys:
            if not os.path.isabs(config[key]):
                config[key] = str(PROJECT_ROOT['data'] / config[key])
        
        # Handle pokemon_data_files paths separately
        if not os.path.isabs(next(iter(config["pokemon_data_files"].values()))):
            config["pokemon_data_files"] = {
                gen: str(PROJECT_ROOT['data'] / path)
                for gen, path in config["pokemon_data_files"].items()
            }
        
        # Validate all generation files
        for file_path in config["pokemon_data_files"].values():
            self.validate_pokemon_data(file_path)
            
        return config

# Helper functions for backward compatibility

def load_config():
    # Load configuration using ConfigManager
    # Returns:
    #     dict: Complete configuration dictionary
    config_manager = ConfigManager()
    return config_manager.config

def check_file_exists(file_path):
    # Check if a file exists and log warning if it doesn't
    # Args:
    #     file_path (str): Path to file to check
    # Returns:
    #     bool: True if file exists, False otherwise
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} does not exist.")
        return False
    return True
