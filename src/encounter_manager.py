import random

from colorama import Fore, Style
from data_manager import save_shiny_count
from logger import logger

class EncounterManager:
    # Manages Pokemon encounters and shiny calculations
    def __init__(self, config):
        # Initialize the encounter manager
        # Args:
        #     config (dict): Configuration dictionary containing shiny rate and rarity weights
        self.shiny_rate = config["shiny_rate"]
        self.rarity_weights = config["rarity_weights"]

    def calculate_weights(self, pokemon_data):
        # Calculate encounter weights based on Pokemon rarity
        # Args:
        #     pokemon_data (dict): Dictionary mapping Pokemon names to their rarity
        # Returns:
        #     list: List of weights corresponding to each Pokemon's rarity
        return [self.rarity_weights.get(rarity, 0) for rarity in pokemon_data.values()]

    def shiny_pokemon(self):
        # Determine if an encountered Pokemon is shiny
        # Returns:
        #     bool: True if the Pokemon is shiny, False otherwise
        shiny_value = random.randint(1, self.shiny_rate)
        if shiny_value == 1:
            return True
        elif random.randint(1, self.shiny_rate // 5) == 1:
            print(Fore.MAGENTA + "You hear a shiny Pokémon nearby..." + Style.RESET_ALL)
        return False

    def handle_shiny_encounter(self, game_instance, pokemon_name, pokemon_rarity):
        # Handle a shiny Pokemon encounter by updating counters and logging the event
        # Args:
        #     game_instance: The game instance containing UI elements
        #     pokemon_name (str): Name of the encountered Pokemon
        #     pokemon_rarity (str): Rarity level of the encountered Pokemon
        try:
            # Update shiny counter and UI
            game_instance.total_shiny_found += 1
            game_instance.shiny_label.config(text=f"Shiny Pokémon Found: {game_instance.total_shiny_found}")
            save_shiny_count(game_instance.total_shiny_found)
            
            # Log the shiny encounter
            logger.log_shiny(pokemon_name, pokemon_rarity)
        except Exception as e:
            logger.log_error(f"Error handling shiny encounter: {str(e)}")
