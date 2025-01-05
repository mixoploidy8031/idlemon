import os
from PIL import Image, ImageTk

# Displays the Pokémon GIF on the canvas
def display_pokemon_gif(canvas, pokemon_name, is_shiny, gif_dir, current_encounter):

    if current_encounter != pokemon_name:
        return

    try:
        gif_type = "shiny" if is_shiny else "normal"
        gif_path = os.path.join(gif_dir, gif_type, f"{pokemon_name}.gif")
        
        if not os.path.exists(gif_path):
            raise FileNotFoundError(f"GIF not found: {gif_path}")

        image = Image.open(gif_path)
        frames = []

        # Extract frames for animated GIFs
        for frame in range(image.n_frames):
            image.seek(frame)
            frames.append(ImageTk.PhotoImage(image.copy()))

        def animate(frame_index=0):
            if current_encounter != pokemon_name:
                return
            canvas.delete("pokemon_gif")
            
            # Calculate the center of the canvas
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            center_x = canvas_width // 2
            center_y = (canvas_height * 5) // 6
            
            # Display the current frame of the Pokémon GIF
            canvas.create_image(center_x, center_y, image=frames[frame_index], tag="pokemon_gif")
            
            # Schedule the next frame
            canvas.after(50, animate, (frame_index + 1) % len(frames))

        animate()
    except Exception as e:
        print(f"Error displaying GIF for {pokemon_name}: {e}")
        canvas.delete("pokemon_gif")
        canvas.create_text(
            250, 400,
            text=f"Error: {pokemon_name} GIF missing!",
            fill="red",
            font=("Arial", 14)
        )
