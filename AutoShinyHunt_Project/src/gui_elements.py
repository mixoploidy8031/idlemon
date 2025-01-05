import tkinter as tk

# Adds a label with black background to canvas
def create_label_with_background(canvas, text, x, y, width, height, font=("Arial", 10)):
    rectangle = canvas.create_rectangle(
        x, y, x + width, y + height,
        fill="black",
        outline=""
    )
    label = tk.Label(canvas.master, text=text, font=font, bg="black", fg="white")
    label_window = canvas.create_window(x + 5, y + height // 2, anchor="w", window=label)
    return label, rectangle
