import os
import base64
from config_loader import load_config
from logger import logger

# Load configuration
config = load_config()
shiny_count_file = config["shiny_count_file"]

class DataManager:
    def __init__(self, config):
        self.shiny_count_file = config["shiny_count_file"]
        self.pokemon_data_file = config["pokemon_data_file"]

    def load_shiny_count(self):
        if os.path.exists(self.shiny_count_file):
            with open(self.shiny_count_file, "r") as file:
                try:
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
        encoded = base64.b64encode(str(count).encode("utf-8")).decode("utf-8")
        with open(self.shiny_count_file, "w") as file:
            file.write(encoded)

    def load_pokemon_data(self):
        pokemon_data = {}
        if os.path.exists(self.pokemon_data_file):
            with open(self.pokemon_data_file, "r", encoding="utf-8") as file:
                for line in file:
                    try:
                        name, rarity = line.strip().split(',')
                        pokemon_data[name] = rarity
                    except ValueError:
                        logger.log_error(f"Invalid entry in {self.pokemon_data_file}: {line.strip()}")
        return pokemon_data
