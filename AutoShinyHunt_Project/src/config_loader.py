import json
import os

DEFAULT_CONFIG = {
    "encounter_delay": 3.0,
    "rarity_weights": {
        "Very Common": 40,
        "Common": 34,
        "Semi-rare": 20,
        "Rare": 5,
        "Very Rare": 1
    },
    "shiny_rate": 1500,
    "shiny_count_file": "shiny_count.txt",
    "pokemon_data_file": "gen1_pokemon_names.txt"
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

# Checks if the given file exists. Raises an error if it doesn't
def check_file_exists(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Required file not found: {filepath}")
    return True

# Validate and repair Pokémon data file
def validate_pokemon_data(file_path):
    default_lines = [line.strip() for line in DEFAULT_POKEMON_DATA.strip().split("\n")]

    # Check if file exists
    if not os.path.exists(file_path):
        print(f"{file_path} not found. Creating a new file with default data.")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("\n".join(default_lines) + "\n")  # Write with a clean structure
        return

    # Read existing file lines
    with open(file_path, "r", encoding="utf-8") as file:
        existing_lines = [line.strip() for line in file.readlines()]

    # Replace if file is corrupted or altered
    if existing_lines != default_lines:
        print(f"{file_path} is corrupted or altered. Replacing with default data.")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("\n".join(default_lines) + "\n")  # Write cleanly

# Load configuration from a JSON file and validate Pokémon data
def load_config(config_file="config.json"):
    user_config = {}
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as file:
                user_config = json.load(file)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error loading config file: {e}. Using default settings.")
    
    # Merge user config with defaults
    config = {**DEFAULT_CONFIG, **user_config}
    
    # Validate Pokémon data file
    validate_pokemon_data(config["pokemon_data_file"])

    return config
