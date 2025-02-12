import os
import logging
from pathlib import Path
from config_loader import get_base_path
import sys

class Logger:
    def __init__(self):
        base_path = get_base_path()
        
        # If running from source (not PyInstaller), use local logs directory
        if not getattr(sys, 'frozen', False):
            self.logs_dir = base_path['data'] / "logs"
        else:
            # If running installed version, use XDG_DATA_HOME
            xdg_data_home = os.environ.get('XDG_DATA_HOME', os.path.expanduser('~/.local/share'))
            self.logs_dir = Path(xdg_data_home) / "idlemon/logs"
            
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # Configure error logger
        self.error_logger = logging.getLogger('error_logger')
        self.error_logger.setLevel(logging.ERROR)
        error_handler = logging.FileHandler(self.logs_dir / 'error.log')
        error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.error_logger.addHandler(error_handler)

        # Initialize shiny encounters file
        self.shiny_log_path = self.logs_dir / 'shinies_encountered.txt'
        self.shiny_encounters = self._load_shiny_encounters()
        
        print(f"Using logs directory: {self.logs_dir}")  # Help users know where logs are stored

    def _load_shiny_encounters(self):
        encounters = {}
        if self.shiny_log_path.exists():
            try:
                with open(self.shiny_log_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            name, rarity, count = [x.strip() for x in line.split('|')]
                            encounters[name] = {'rarity': rarity, 'count': int(count)}
                        except ValueError:
                            self.error_logger.error(f"Invalid line in shiny log: {line.strip()}")
            except Exception as e:
                self.error_logger.error(f"Error loading shiny encounters: {str(e)}")
        return encounters

    def log_error(self, message):
        self.error_logger.error(message)
        print(f"Error logged to: {self.logs_dir / 'error.log'}")

    def log_shiny(self, pokemon_name, rarity):
        if pokemon_name in self.shiny_encounters:
            self.shiny_encounters[pokemon_name]['count'] += 1
        else:
            self.shiny_encounters[pokemon_name] = {'rarity': rarity, 'count': 1}
        
        try:
            with open(self.shiny_log_path, 'w', encoding='utf-8') as f:
                for name, data in sorted(self.shiny_encounters.items()):
                    f.write(f"{name} | {data['rarity']} | {data['count']}\n")
            return True
        except Exception as e:
            self.error_logger.error(f"Error writing to shiny log: {str(e)}")
            return False

logger = Logger() 