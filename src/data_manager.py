import os
import sys
import base64
from pathlib import Path
from config_loader import load_config, get_base_path, POKEMON_DATA_HASHES
from logger import logger

# Load configuration
config = load_config()

class DataManager:
    # Manages data loading, saving, and validation for the application
    def __init__(self, config):
        # Initialize the data manager
        # Args:
        #     config (dict): Configuration dictionary containing file paths and settings
        base_path = get_base_path()
        
        # If running from source (not PyInstaller), use local logs directory
        if not getattr(sys, 'frozen', False):
            data_dir = base_path['data']
        else:
            # If running installed version, use XDG_DATA_HOME
            xdg_data_home = os.environ.get('XDG_DATA_HOME', os.path.expanduser('~/.local/share'))
            data_dir = Path(xdg_data_home) / "idlemon"
            
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Use data directory for files that need to be written to
        self.shiny_count_file = data_dir / "logs/shiny_count.bin"
        self.shiny_count_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Use runtime path for read-only files
        self.pokemon_data_files = {
            gen: base_path['runtime'] / path
            for gen, path in config["pokemon_data_files"].items()
        }
        self.pokemon_data_cache = None
        
        print(f"Using data directory: {data_dir}")  # Help users know where data is stored

    def load_shiny_count(self):
        # Load the total number of shiny Pokemon encountered
        # Returns:
        #     int: Number of shiny Pokemon found, 0 if file doesn't exist or is corrupted
        if self.shiny_count_file.exists():
            try:
                with open(self.shiny_count_file, "r") as file:
                    encoded = file.read().strip()
                    return int(base64.b64decode(encoded).decode("utf-8"))
            except (ValueError, base64.binascii.Error) as e:
                logger.log_error(f"Error loading shiny count: {str(e)}")
                print(f"Warning: {self.shiny_count_file} is corrupted. Resetting to 0.")
        else:
            logger.log_error(f"Shiny count file missing: {self.shiny_count_file}")
            print(f"Warning: {self.shiny_count_file} is missing. Creating new file.")
        
        self.save_shiny_count(0)
        return 0

    def save_shiny_count(self, count):
        # Save the total number of shiny Pokemon encountered
        # Args:
        #     count (int): Number of shiny Pokemon to save
        try:
            encoded = base64.b64encode(str(count).encode("utf-8")).decode("utf-8")
            with open(self.shiny_count_file, "w") as file:
                file.write(encoded)
        except Exception as e:
            logger.log_error(f"Error saving shiny count: {str(e)}")

    def validate_pokemon_data(self, gen, file_path):
        # Validate Pokemon data file against stored hash
        # Args:
        #     gen (str): Generation identifier (e.g., 'gen1')
        #     file_path (str): Path to the Pokemon data file
        # Returns:
        #     bool: True if validation passes, False otherwise
        import hashlib
        
        if not os.path.exists(file_path):
            logger.log_error(f"Error: {file_path} not found.")
            return False
            
        # Read file in binary mode and normalize line endings to LF
        with open(file_path, "rb") as file:
            content = file.read()
            # Convert all line endings to LF
            content = content.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
            # Normalize whitespace while preserving line endings
            content = b'\n'.join(line.strip() for line in content.split(b'\n'))
            file_hash = hashlib.sha256(content).hexdigest()
            
        if file_hash != POKEMON_DATA_HASHES.get(gen, ""):
            logger.log_error(f"Warning: {file_path} may have been modified. Hash verification failed.")
            return False
        return True

    def load_pokemon_data(self):
        # Load Pokemon data from all generation files into one combined pool
        # Returns:
        #     dict: Combined Pokemon data mapping names to rarities
        
        # Return cached data if available
        if self.pokemon_data_cache is not None:
            return self.pokemon_data_cache
        
        pokemon_data = {}
        
        # Load and validate each generation's data
        for gen, file_path in self.pokemon_data_files.items():
            if not self.validate_pokemon_data(gen, file_path):
                logger.log_error(f"Data validation failed for {gen}")
                continue
                
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    for line in file:
                        try:
                            name, rarity = line.strip().split(',')
                            pokemon_data[name] = rarity
                        except ValueError:
                            logger.log_error(f"Invalid entry in {file_path}: {line.strip()}")
            except Exception as e:
                logger.log_error(f"Error loading Pokemon data for {gen}: {str(e)}")
            
        # Cache the combined data
        self.pokemon_data_cache = pokemon_data
        return pokemon_data
