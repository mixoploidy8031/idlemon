import os
import random
import time
import threading
import base64
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from colorama import Fore, Style
from config_loader import load_config, check_file_exists
from pokemon_display import display_pokemon_gif
from data_manager import load_shiny_count, save_shiny_count, load_pokemon_data

# Load configuration
config = load_config()

# Extract user-configurable values
gif_directory = config["gif_directory"]
background_image = config["background_image"]

# Extract internal defaults
shiny_count_file = config["shiny_count_file"]
pokemon_data_file = config["pokemon_data_file"]
encounter_delay = config["encounter_delay"]
rarity_weights = config["rarity_weights"]
shiny_rate = config["shiny_rate"]

# Validate required files
check_file_exists(shiny_count_file)
check_file_exists(pokemon_data_file)
check_file_exists(background_image)

# Update shiny count and save it
def update_shiny_count():
    global total_shiny_found
    total_shiny_found += 1
    shiny_label.config(text=f"Shiny Pokémon Found: {total_shiny_found}")
    save_shiny_count(total_shiny_found)

# Initialize shiny count from file
def initialize_shiny_count():
    global total_shiny_found
    total_shiny_found = load_shiny_count()
    shiny_label.config(text=f"Shiny Pokémon Found: {total_shiny_found}")

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

# Load Pokémon data
def initialize_pokemon_data():
    global pokemon_data
    pokemon_data = load_pokemon_data(config["pokemon_data_file"])

# Calculate encounter weights based on rarity
def calculate_weights(pokemon_data):
    weights = [rarity_weights.get(rarity, 0) for rarity in pokemon_data.values()]
    return weights

# Simulate shiny encounter
def shiny_pokemon():
    shiny_value = random.randint(1, shiny_rate)
    if shiny_value == 1:
        return True
    elif random.randint(1, shiny_rate // 5) == 1:
        print(Fore.MAGENTA + "You hear a shiny Pokémon nearby..." + Style.RESET_ALL)
    return False

# Display the Pokémon GIF
def display_pokemon_gif(pokemon_name, is_shiny=False):
    global current_encounter
    if current_encounter != pokemon_name:
        return

    try:
        gif_type = "shiny" if is_shiny else "normal"
        gif_path = os.path.join(gif_directory, gif_type, f"{pokemon_name}.gif")
        
        # Open the GIF
        image = Image.open(gif_path)
        frames = []
        
        # Extract frames for animated GIFs
        for frame in range(0, image.n_frames):
            image.seek(frame)
            frames.append(ImageTk.PhotoImage(image.copy()))

        # Cycle through the frames to animate
        def animate(frame_index=0):
            if current_encounter != pokemon_name:
                return  # Stop animation if the encounter has changed
            
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
    continue_button.place_forget()
    if not timer_running:
        timer_running = True
        threading.Thread(target=update_timer, daemon=True).start()
    start_encounter_thread()

# Start the encounter loop
def start_encounter():
    global current_encounter, total_encounters, shiny_found

    # Load Pokémon data
    pokemon_data = load_pokemon_data(config["pokemon_data_file"])
    if not pokemon_data:
        print("No Pokémon data available. Exiting encounter loop.")
        return
    
    # Extract Pokémon names and calculate weights
    pokemon_list = list(pokemon_data.keys())
    weights = calculate_weights(pokemon_data)

    # Encounter loop
    while not shiny_found:
        time.sleep(encounter_delay)
        total_encounters += 1
        encounter_label.config(text=f"Encounters: {total_encounters}")

        # Randomly select a Pokémon based on weights
        pokemon_name = random.choices(pokemon_list, weights=weights, k=1)[0]
        pokemon_rarity = pokemon_data[pokemon_name]
        current_encounter = pokemon_name

        # Determine if the encounter is shiny
        is_shiny = shiny_pokemon()

        # Display Pokémon gif
        display_pokemon_gif(pokemon_name, is_shiny=is_shiny)

        # Update info label for shiny or normal Pokémon
        if is_shiny:
            handle_shiny_encounter(pokemon_name, pokemon_rarity)
        else:
            info_label.config(
                text=f"{pokemon_name} - {pokemon_rarity}",
                fg="white"  # Reset color to white for normal Pokémon
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
root.minsize(500, 500)

# Load the background image
background_image_path = os.path.join(os.getcwd(), background_image)
if not check_file_exists(background_image_path):
    background_image_path = "default_background.jpg"  # Fallback
background_image = tk.PhotoImage(file=background_image_path)

# Get dimensions of the background image
background_width = background_image.width()
background_height = background_image.height()

# Set Tkinter window constraints
root.maxsize(background_width, background_height)
root.resizable(width=True, height=False)


# Canvas for GIF and background
canvas_width = 500
canvas_height = 500
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack(fill="both", expand=False)
canvas.create_image(0, 0, image=background_image, anchor="nw")

# Labels
info_label, info_bg = create_label_with_background(canvas, "Walking through the Kanto region...", 10, 10, 200, 20)
encounter_label, encounter_bg = create_label_with_background(canvas, "Encounters: 0", 10, 40, 200, 20)
shiny_label, shiny_bg = create_label_with_background(canvas, "Shiny Pokémon Found: 0", 10, 70, 200, 20)
stats_label, stats_bg = create_label_with_background(canvas, "Time Elapsed: 0 seconds", 10, 100, 200, 20)

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
continue_button.place_forget()

# Start timer and encounters
initialize_timer()
start_encounter_thread()

# Handle window close event and ensure timer running variable is set to false
def on_closing():
    global timer_running
    timer_running = False 
    root.destroy()  # Close the Tkinter window

# Register the on_closing function with the window close protocol
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the Tkinter event loop
root.mainloop()
