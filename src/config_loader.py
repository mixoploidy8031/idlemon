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

DEFAULT_CONFIG = {
    "encounter_delay": 2.5, # Default is 2.5 seconds
    "rarity_weights": {
        "Very Common": 40, # Default is 40
        "Common": 34, # Default is 34
        "Semi-rare": 20, # Default is 20
        "Rare": 5, # Default is 5
        "Very Rare": 1 # Default is 1
    },
    "shiny_rate": 2000, # Default is 2000
    "mute_audio": False,  # Add default mute setting
    "shiny_count_file": "logs/shiny_count.bin",
    "pokemon_data_file": "assets/data/gen1_pokemon_names.txt",
    "shinies_encounter_file": "logs/shinies_encountered.txt",
    "gif_directory": "assets/gifs",
    "background_image": "assets/images/default_background.jpg",
}

# Default Pokémon data
DEFAULT_POKEMON_DATA = """
Abra,Semi-rare
Aerodactyl,Very Rare
Alakazam,Semi-rare
Arbok,Semi-rare
Arcanine,Very Rare
Articuno,Very Rare
Beedrill,Semi-rare
Bellsprout,Common
Blastoise,Very Rare
Bulbasaur,Semi-rare
Butterfree,Semi-rare
Caterpie,Very Common
Chansey,Semi-rare
Charizard,Very Rare
Charmander,Semi-rare
Charmeleon,Rare
Clefable,Rare
Clefairy,Common
Cloyster,Semi-rare
Cubone,Common
Dewgong,Semi-rare
Diglett,Common
Ditto,Semi-rare
Dodrio,Semi-rare
Doduo,Common
Dragonair,Rare
Dragonite,Very Rare
Dratini,Semi-rare
Drowzee,Semi-rare
Dugtrio,Semi-rare
Eevee,Semi-rare
Ekans,Common
Electabuzz,Semi-rare
Electrode,Semi-rare
Exeggcute,Common
Exeggutor,Semi-rare
Farfetch'd,Semi-rare
Fearow,Semi-rare
Flareon,Semi-rare
Gastly,Semi-rare
Gengar,Semi-rare
Geodude,Common
Gloom,Common
Golbat,Semi-rare
Goldeen,Common
Golduck,Semi-rare
Golem,Very Rare
Graveler,Semi-rare
Grimer,Common
Growlithe,Common
Gyarados,Rare
Haunter,Semi-rare
Hitmonchan,Semi-rare
Hitmonlee,Semi-rare
Horsea,Common
Hypno,Semi-rare
Ivysaur,Rare
Jigglypuff,Common
Jolteon,Semi-rare
Jynx,Semi-rare
Kabuto,Semi-rare
Kabutops,Semi-rare
Kadabra,Semi-rare
Kakuna,Common
Kangaskhan,Very Rare
Kingler,Semi-rare
Koffing,Common
Krabby,Common
Lapras,Semi-rare
Lickitung,Semi-rare
Machamp,Rare
Machoke,Semi-rare
Machop,Common
Magikarp,Very Common
Magmar,Semi-rare
Magnemite,Common
Magneton,Semi-rare
Mankey,Common
Marowak,Semi-rare
Meowth,Common
Metapod,Common
Mew,Very Rare
Mewtwo,Very Rare
Moltres,Very Rare
Mr. Mime,Semi-rare
Muk,Semi-rare
Nidoking,Semi-rare
Nidoqueen,Semi-rare
Nidoran♀,Common
Nidoran♂,Common
Nidorina,Common
Nidorino,Semi-rare
Ninetales,Semi-rare
Oddish,Common
Omanyte,Semi-rare
Omastar,Semi-rare
Onix,Common
Paras,Common
Parasect,Semi-rare
Persian,Semi-rare
Pidgeot,Semi-rare
Pidgeotto,Common
Pidgey,Very Common
Pikachu,Semi-rare
Pinsir,Semi-rare
Poliwag,Common
Poliwhirl,Semi-rare
Poliwrath,Semi-rare
Ponyta,Common
Porygon,Rare
Primeape,Semi-rare
Psyduck,Common
Raichu,Semi-rare
Rapidash,Semi-rare
Raticate,Common
Rattata,Very Common
Rhydon,Semi-rare
Rhyhorn,Common
Sandshrew,Common
Sandslash,Semi-rare
Scyther,Semi-rare
Seadra,Semi-rare
Seaking,Common
Seel,Common
Shellder,Common
Slowbro,Semi-rare
Slowpoke,Common
Snorlax,Very Rare
Spearow,Common
Squirtle,Semi-rare
Starmie,Semi-rare
Staryu,Common
Tangela,Semi-rare
Tauros,Common
Tentacool,Common
Tentacruel,Semi-rare
Vaporeon,Semi-rare
Venomoth,Semi-rare
Venonat,Common
Venusaur,Very Rare
Victreebel,Semi-rare
Vileplume,Semi-rare
Voltorb,Common
Vulpix,Common
Wartortle,Rare
Weedle,Very Common
Weepinbell,Common
Weezing,Semi-rare
Wigglytuff,Semi-rare
Zapdos,Very Rare
Zubat,Common
"""

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = str(PROJECT_ROOT['data'] / config_file)
        # Create necessary directories relative to project root
        (PROJECT_ROOT['data'] / "logs").mkdir(exist_ok=True)
        (PROJECT_ROOT['data'] / "assets/data").mkdir(parents=True, exist_ok=True)
        (PROJECT_ROOT['data'] / "assets/gifs/normal").mkdir(parents=True, exist_ok=True)
        (PROJECT_ROOT['data'] / "assets/gifs/shiny").mkdir(parents=True, exist_ok=True)
        (PROJECT_ROOT['data'] / "assets/images").mkdir(parents=True, exist_ok=True)
        (PROJECT_ROOT['data'] / "assets/sounds").mkdir(parents=True, exist_ok=True)
        self.config = self.load_config()

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
        path_keys = ["shiny_count_file", "pokemon_data_file", "shinies_encounter_file", "gif_directory"]
        for key in path_keys:
            if not os.path.isabs(config[key]):
                config[key] = str(PROJECT_ROOT['data'] / config[key])
        
        # Background image can be absolute or relative, handled in main.py
        
        self.validate_pokemon_data(config["pokemon_data_file"])
        return config

    def validate_pokemon_data(self, file_path):
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        default_lines = [line.strip() for line in DEFAULT_POKEMON_DATA.strip().split("\n")]
        
        if not os.path.exists(file_path):
            print(f"{file_path} not found. Creating with default data.")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("\n".join(default_lines) + "\n")
            return

        with open(file_path, "r", encoding="utf-8") as file:
            existing_lines = [line.strip() for line in file.readlines()]

        if existing_lines != default_lines:
            print(f"{file_path} is corrupted or altered. Replacing with default data.")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("\n".join(default_lines) + "\n")

# Helper functions to maintain backwards compatibility
def load_config():
    config_manager = ConfigManager()
    return config_manager.config

def check_file_exists(file_path):
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} does not exist.")
        return False
    return True
