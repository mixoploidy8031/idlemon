import os
import base64
from config_loader import load_config

# Load configuration
config = load_config()
shiny_count_file = config["shiny_count_file"]

# Load shiny count from file using base64 decoding
def load_shiny_count():
    if os.path.exists(shiny_count_file):
        with open(shiny_count_file, "r") as file:
            try:
                encoded = file.read().strip()
                return int(base64.b64decode(encoded).decode("utf-8"))
            except (ValueError, base64.binascii.Error):
                print(f"Warning: {shiny_count_file} is corrupted or altered. Resetting shiny count to 0.")
    else:
        print(f"Warning: {shiny_count_file} is missing. Creating a new file with shiny count reset to 0.")
    
    save_shiny_count(0)
    return 0

# Save shiny count to file using base64 encoding
def save_shiny_count(count):
    encoded = base64.b64encode(str(count).encode("utf-8")).decode("utf-8")
    with open(shiny_count_file, "w") as file:
        file.write(encoded) 

# Load Pokémon data from a file.
def load_pokemon_data(file_path):
    pokemon_data = {}
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                try:
                    name, rarity = line.strip().split(',')
                    pokemon_data[name] = rarity
                except ValueError:
                    print(f"Invalid entry in {file_path}: {line.strip()}")
    else:
        print(f"Error: Pokémon data file '{file_path}' not found.")
    return pokemon_data
