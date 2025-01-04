import random
import time
import threading
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from colorama import Fore, Style

# Start of the adventure
print(Fore.CYAN + "You start walking around the Kanto region..." + Style.RESET_ALL)

# Function to load Pokémon names and their rarity from the file
def load_pokemon_data():
    pokemon_data = {}
    with open("gen1_pokemon_names.txt", "r", encoding ="utf-8") as file:
        for line in file:
            name, rarity = line.strip().split(',')
            pokemon_data[name] = rarity
    return pokemon_data

# Function to calculate the encounter rate based on rarity
def calculate_weights(pokemon_data):
    rarity_map = {
        "Very Common": 100,
        "Common": 85,
        "Semi-rare": 67.5,
        "Rare": 33.3,
        "Very Rare": 12.5,
    }
    weights = [rarity_map.get(rarity, 0) for rarity in pokemon_data.values()]
    return weights

# Simulates shiny encounter
def shiny_pokemon():
    shiny_value = random.randint(1, 8192) # Default rate is 1/8192
    if shiny_value == 1: # If the value is 1, it's a shiny
        return True # Shiny Pokémon found
    else:
        # Small chance to hear nearby shiny if not found yet
        if random.randint(1, 819) == 1:
            print(Fore.MAGENTA + "You hear a shiny Pokémon nearby..." + Style.RESET_ALL)
        return False # Print nothing 

# Function to display the Pokémon GIF in the Tkinter window
def display_pokemon_gif(pokemon_name, is_shiny=False):
    global current_encounter
    if current_encounter != pokemon_name:
        return # Skip if this is not the current encounter

    try:
        # Determine the correct file path based on shiny status
        gif_type = "shiny" if is_shiny else "normal"
        gif_path = f"C:/Users/googl/Documents/PythonScripts/PokeShinyHunt_v1/gen1_gifs/{gif_type}/{pokemon_name}.gif"
        image = Image.open(gif_path)
        frames = []
        
        # Extract frames for animated GIFs
        for frame in range(0, image.n_frames):
            image.seek(frame)
            frames.append(ImageTk.PhotoImage(image.copy()))
            
        # Cycle though the frames to animate
        def animate(frame_index=0):
            if current_encounter != pokemon_name:
                return # Stop animation if the encounter has changed
            canvas.delete("all")
            canvas.create_image(100, 100, image=frames[frame_index])
            root.after(50, animate, (frame_index + 1) % len(frames))
            
        animate()
    except Exception as e:
        print(f"Error loading {pokemon_name}: {e}")

# Start the encounter loop
def start_encounter():
    global current_encounter, total_encounters, total_shiny_found
    pokemon_data = load_pokemon_data() # Load Pokémon names and rarities
    pokemon_list = list(pokemon_data.keys())
    weights = calculate_weights(pokemon_data)
    
    start_time = time.time()
    while True:
        time.sleep(3.0) # Delay between encounters (1.0 = 1 second)
        total_encounters += 1
        encounter_label.config(text=f"Encounters: {total_encounters}") # Update encounter count in GUI
        
        # Select a Pokémon based on weighted probability
        pokemon_name = random.choices(pokemon_list, weights=weights, k=1)[0]
        pokemon_rarity = pokemon_data[pokemon_name]
        current_encounter = pokemon_name
            
        # Perform shiny check and display Pokémon
        is_shiny = shiny_pokemon()
        display_pokemon_gif(pokemon_name, is_shiny=is_shiny)
        info_label.config(text=f"{pokemon_name} - {pokemon_rarity}")
    
        # Break if shiny is found
        if is_shiny:
            total_shiny_found += 1
            shiny_label.config(text=f"Shiny Pokémon Found: {total_shiny_found}")
            print(Fore.YELLOW + f"Congrats!!! You found a shiny {pokemon_name}!" + Style.RESET_ALL)
            break  
        else:
            print(f"You encountered a wild {pokemon_name}!")

        elapsed_time = time.time() - start_time
        stats_label.config(text=f"Time Elapsed: {int(elapsed_time)} seconds")
 
# Start encounter simulation
def start_encounter_thread():
    threading.Thread(target=start_encounter, daemon=True).start()

# Initialize the Tkinter window
root = tk.Tk()
root.title("Pokémon Auto-Hunt")

# Canvas for Pokémon GIF
canvas = tk.Canvas(root, width=200, height=200)
canvas.pack()

# Encounter info label
info_label = tk.Label(root, text="Encounter information will appear here.", font=("Arial", 10))
info_label.pack()

# Encounter count label
encounter_label = tk.Label(root, text="Encounters: 0", font=("Arial", 10))
encounter_label.pack()

# Shiny Pokémon stats label
shiny_label = tk.Label(root, text="Shiny Pokémon Found: 0", font=("Arial", 10))
shiny_label.pack()

# Session stats label
stats_label = tk.Label(root, text="Time Elapsed: 0 seconds", font=("Arial", 10))
stats_label.pack()

# Global variable to track the current encounter
current_encounter = None
total_encounters = 0
total_shiny_found = 0

# Start encounter simulation
start_encounter_thread()

# Run the Tkinter event loop
root.mainloop()