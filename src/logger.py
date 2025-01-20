import os
import logging
from datetime import datetime
from pathlib import Path
from config_loader import get_base_path

class LogManager:
    def __init__(self):
        base_path = get_base_path()
        # Use data path for writing logs
        self.logs_dir = base_path['data'] / "logs"
        self.logs_dir.mkdir(exist_ok=True)

        # Configure error logger
        self.error_logger = logging.getLogger('error_logger')
        self.error_logger.setLevel(logging.ERROR)
        error_handler = logging.FileHandler(self.logs_dir / 'error.log')
        error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.error_logger.addHandler(error_handler)

        # Initialize shiny encounters file
        self.shiny_log_path = self.logs_dir / 'shinies_encountered.txt'
        self.shiny_encounters = self._load_shiny_encounters()

    def _load_shiny_encounters(self):
        encounters = {}
        if os.path.exists(self.shiny_log_path):
            with open(self.shiny_log_path, 'r') as f:
                for line in f:
                    try:
                        name, rarity, count = line.strip().split(' | ')
                        encounters[name] = {'rarity': rarity, 'count': int(count)}
                    except ValueError:
                        self.error_logger.error(f"Invalid line in shiny log: {line.strip()}")
        return encounters

    def log_error(self, message):
        self.error_logger.error(message)

    def log_shiny(self, pokemon_name, rarity):
        if pokemon_name in self.shiny_encounters:
            self.shiny_encounters[pokemon_name]['count'] += 1
        else:
            self.shiny_encounters[pokemon_name] = {'rarity': rarity, 'count': 1}
        
        # Write updated encounters to file
        with open(self.shiny_log_path, 'w') as f:
            for name, data in sorted(self.shiny_encounters.items()):
                f.write(f"{name} | {data['rarity']} | {data['count']}\n")

# Create global logger instance
logger = LogManager() 