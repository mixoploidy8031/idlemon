import os
import random
import time
import threading
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from colorama import Fore, Style

# File to store the shiny Pokémon count
SHINY_COUNT_FILE = "shiny_count.txt"

# Load shiny count from txt file
def load_shiny_count():
    if os.path.exists(SHINY_COUNT_FILE):
        with open(SHINY_COUNT_FILE, "r") as file:
            try:
                return int(file.read().strip())
            except ValueError:
                return 0 # Default 0 if file corrupted
    return 0

# Save shiny count to txt file
def save_shiny_count(count):
    with open(SHINY_COUNT_FILE, "w") as file:
        file.write(str(count))

# Update shiny count and save it
def update_shiny_count():
    global total_shiny_found
    total_shiny_found += 1
    shiny_label.config(text=f"Shiny Pokémon Found: {total_shiny_found}")
    save_shiny_count(total_shiny_found) # Call save function
    print(Fore.YELLOW + f"Shiny Pokémon count updated: {total_shiny_found}" + Style.RESET_ALL)

# Initiaize shiny count from file
def initialize_shiny_count():
    global total_shiny_found
    total_shiny_found = load_shiny_count()
    shiny_label.config(text=f"Shiny Pokémon Found: {total_shiny_found}")
    print(Fore.GREEN + f"Loaded shiny Pokémon count: {total_shiny_found}" + Style.RESET_ALL)

# Handle shiny Pokémon encounter
def handle_shiny_encounter(pokemon_name, pokemon_rarity):
    global shiny_found, timer_running
    shiny_found = True
    info_label.config(
        text=f"{pokemon_name} - {pokemon_rarity} (Shiny!)",
        fg="gold"
    )
    print(Fore.YELLOW + f"Congrats!!! You found a shiny {pokemon_name}!" + Style.RESET_ALL)
    update_shiny_count()
    continue_button.place(relx=0.5, rely=0.5, anchor="center")
    timer_running = False
    
##########################
## BEGINNING OF PROGRAM ##
##########################



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

# Calculate the encounter rate based on rarity
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
    shiny_value = random.randint(1, 10) # Default rate is 1/8192
    if shiny_value == 1: # If the value is 1, it's a shiny
        return True # Shiny Pokémon found
    else:
        # Small chance to hear nearby shiny if not found yet
        if random.randint(1, 819) == 1:
            print(Fore.MAGENTA + "You hear a shiny Pokémon nearby..." + Style.RESET_ALL)
        return False # Print nothing 

# Display the Pokémon GIF in the Tkinter window
def display_pokemon_gif(pokemon_name, is_shiny=False):
    global current_encounter
    if current_encounter != pokemon_name:
        return # Skip if this is not the current encounter

    try:
        # Determine the correct file path based on shiny status
        gif_type = "shiny" if is_shiny else "normal"
        gif_path = f"C:/Users/googl/Documents/PythonScripts/PokemonAuto-Hunt_v0.1.0/AutoShinyHunt_Project/gen1_gifs/{gif_type}/{pokemon_name}.gif"
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
            
            # Clear only Pokémon GIF
            canvas.delete("pokemon_gif")
            
            # Calculate the center of the canvas
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            center_x = canvas_width // 2
            center_y = (canvas_height * 5) // 6
            
            # Add the current frame of the Pokémon GIF to the canvas
            canvas.create_image(center_x, center_y, image=frames[frame_index], tag="pokemon_gif")
            
            # Schedule next frame
            root.after(50, animate, (frame_index + 1) % len(frames))
            
        animate()
    except Exception as e:
        print(f"Error loading {pokemon_name}: {e}")

# Update the timer label
def update_timer():
    global elapsed_time, start_time, timer_running
    while timer_running:
        # Calculate elapsed time
        if start_time is not None:
            elapsed_time += time.time() - start_time
            start_time = time.time()
        minutes, seconds = divmod(int(elapsed_time), 60)
        stats_label.config(text=f"Time Elapsed: {minutes:02}:{seconds:02}")
        time.sleep(1)

# Handle the "Continue" button click
def continue_hunt():
    global shiny_found, start_time, timer_running
    shiny_found = False
    start_time = time.time()
    continue_button.place_forget() # Hides button
    if not timer_running:
        timer_running = True
        threading.Thread(target=update_timer, daemon=True).start()
    start_encounter_thread() # Restart encounter loop

# Start the encounter loop
def start_encounter():
    global current_encounter, total_encounters, shiny_found, timer_running, total_shiny_found
    pokemon_data = load_pokemon_data() # Load Pokémon names and rarities
    pokemon_list = list(pokemon_data.keys())
    weights = calculate_weights(pokemon_data)
    #start_time = time.time()
    
    while not shiny_found: # Stop loop when shiny is found
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
            handle_shiny_encounter(pokemon_name, pokemon_rarity)
        else:
            info_label.config(
                text=f"{pokemon_name} - {pokemon_rarity}",
                fg="white" # Set desired color for wild Pokémon
            )
            print(f"You encountered a wild {pokemon_name}!")
 
# Start encounter simulation
def start_encounter_thread():
    threading.Thread(target=start_encounter, daemon=True).start()

# Initialize the timer
def initialize_timer():
    global start_time, timer_running
    start_time = time.time()
    timer_running = True
    threading.Thread(target=update_timer, daemon=True).start()

# Add label with a semi-transparent background to the canvas
def create_label_with_background(canvas, text, x, y, width, height, font=("Arial", 10)):
    rectangle = canvas.create_rectangle(
        x, y, x + width, y + height,
        fill="black",
        outline=""
    )
    label = tk.Label(root, text=text, font=font, bg="black", fg="white")
    label_window = canvas.create_window(x + 5, y + height // 2, anchor="w", window=label)
    return label, rectangle

# Initialize global variables
current_encounter = None
total_encounters = 0
total_shiny_found = 0
shiny_found = False
elapsed_time = 0
start_time = None
timer_running = False

# Initialize the Tkinter window
root = tk.Tk()
root.title("Pokémon Auto-Hunt")
root.minsize(500, 500) # Set minimum size

# Load the background image
background_image = tk.PhotoImage(file="C:/Users/googl/Documents/PythonScripts/PokemonAuto-Hunt_v0.1.0/AutoShinyHunt_Project/assets/bkg1.jpg")

# Get dimensions of the background image
background_width = background_image.width()
background_height = background_image.height()

# Canvas for Pokémon GIF and background
canvas_width = 500
canvas_height = 500
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack(fill="both", expand=False)
canvas.create_image(0,0, image=background_image, anchor="nw")

# Set the window size and constraints
root.geometry(f"{canvas_width}x{canvas_height}")
root.minsize(canvas_width, canvas_height)
root.maxsize(background_width, background_height)
root.resizable(width=True, height=False)

# Labels
info_label, info_bg = create_label_with_background(canvas, "You start walking around the Kanto region...", 10, 10, 180, 20)
encounter_label, encounter_bg = create_label_with_background(canvas, "Encounters: 0", 10, 40, 180, 20)
shiny_label, shiny_bg = create_label_with_background(canvas, "Shiny Pokémon Found: 0", 10, 70, 180, 20)
stats_label, stats_bg = create_label_with_background(canvas, "Time Elapsed: 0 seconds", 10, 100, 180, 20)

initialize_shiny_count()

# "Continue" button
continue_button = tk.Button(
    root,
    text="Continue Hunt",
    command=continue_hunt,
    font=("Arial", 12),
    bg="green",
    fg="white"
)
continue_button.place_forget() # Hide the button initially

# Start timer and encounters
initialize_timer()
start_encounter_thread()

# Run the Tkinter event loop
root.mainloop()
