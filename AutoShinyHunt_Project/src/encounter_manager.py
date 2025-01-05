import random
from data_manager import save_shiny_count

# Calculate weights based on rarity for encounter probabilities
def calculate_weights(pokemon_data, rarity_weights):
    return [rarity_weights.get(rarity, 0) for rarity in pokemon_data.values()]

# Determines if the current Pokémon is shiny
def shiny_pokemon(shiny_rate):
    return random.randint(1, shiny_rate) == 1

# Updates shiny count and label for a shiny encounter.
def handle_shiny_encounter(total_shiny_found, shiny_label, pokemon_name, pokemon_rarity):
    total_shiny_found += 1
    shiny_label.config(text=f"Shiny Pokémon Found: {total_shiny_found}")
    save_shiny_count(total_shiny_found)
    return total_shiny_found
